from qiskit import QuantumCircuit, transpile
from settings import get_available_backend, wait_for_queue

backend = get_available_backend()
backend = wait_for_queue(backend)

# --- 이 아래에 코드를 작성하여 테스트하면 됩니다. ---

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

compiled_qc = transpile(qc, backend)
job = backend.run(compiled_qc, shots=1000)
result = job.result()
counts = result.get_counts(qc)

print("측정 결과:", counts)
