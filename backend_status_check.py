from dotenv import load_dotenv
import os
from qiskit_ibm_runtime import QiskitRuntimeService

load_dotenv()
api_token = os.getenv("API_TOKEN")

if not api_token:
    raise ValueError(
        "API_TOKEN이 .env 파일에 설정되지 않았습니다. IBM Quantum API 키를 추가해주세요."
    )

QiskitRuntimeService.save_account(
    channel="ibm_quantum", token=api_token, overwrite=True
)
service = QiskitRuntimeService()


def get_backends_with_queue():
    backends = service.backends()
    if not backends:
        return []
    return [(backend.name, backend.status().pending_jobs) for backend in backends]


def list_available_backends_with_queue():
    print("[사용 가능한 백엔드 목록]")
    backends = get_backends_with_queue()
    if not backends:
        print("사용 가능한 백엔드가 없습니다.")
    else:
        for backend_name, pending_jobs in backends:
            print(f"{backend_name} (대기열에 대기 중인 사용자 수: {pending_jobs})")


if __name__ == "__main__":
    list_available_backends_with_queue()
