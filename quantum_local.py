from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)

simulator = Aer.get_backend("qasm_simulator")

compiled_qc = transpile(qc, simulator)

job = simulator.run(compiled_qc, shots=1000)
result = job.result()
counts = result.get_counts(qc)

print("측정 결과:", counts)
