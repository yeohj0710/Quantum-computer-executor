from dotenv import load_dotenv
import os
import time
from qiskit_ibm_runtime import QiskitRuntimeService

load_dotenv()

api_token = os.getenv("API_TOKEN")
instance = os.getenv("INSTANCE")
backend_name = os.getenv("BACKEND")

QiskitRuntimeService.save_account(
    channel="ibm_quantum", token=api_token, overwrite=True
)
service = QiskitRuntimeService(instance=instance if instance else None)


def get_available_backend():
    global backend_name
    if not backend_name:
        print("환경 변수 'BACKEND'가 설정되지 않았습니다.")
        print("사용 가능한 백엔드 목록:")
        backends = service.backends()
        if not backends:
            raise ValueError("사용 가능한 백엔드가 없습니다.")
        for backend in backends:
            print(f"- {backend.name}")
        backend_name = backends[0].name
        print(f"사용 가능한 백엔드 중 첫 번째를 선택합니다: {backend_name}")

    try:
        backend = service.backend(backend_name)
        print(f"선택된 backend: {backend_name}")
        status = backend.status()
        print(f"대기열에 대기 중인 사용자 수: {status.pending_jobs}")
        print(f"backend 상태: {'사용 가능' if status.operational else '사용 불가'}")
        return backend
    except Exception as e:
        print(
            f"환경 변수에 설정된 backend '{backend_name}'를 사용할 수 없습니다. 오류: {e}"
        )
        raise ValueError("유효한 백엔드를 찾을 수 없습니다.")


def wait_for_queue(backend):
    status = backend.status()
    pending_jobs = status.pending_jobs
    print(f"현재 대기열에 대기 중인 사용자 수: {pending_jobs}")
    while pending_jobs > 0:
        time.sleep(5)
        status = backend.status()
        if status.pending_jobs < pending_jobs:
            pending_jobs = status.pending_jobs
            print(f"대기열에 대기 중인 사용자 수: {pending_jobs}")
    return backend
