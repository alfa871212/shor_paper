import matplotlib.pyplot as plt
from qiskit import QuantumRegister, QuantumCircuit
from qiskit.circuit.library import QFT

import simulation as sim

# args = sim.process_command()
x = []
gt_lis = []
ct_lis = []
for i in range(1, 29):
    x.append(i)
    qr = QuantumRegister(i)
    qc = QuantumCircuit(qr)
    gate = QFT(i)
    qc.append(gate, qargs=qr[:])
    qc.measure_all()
    gt_lis.append(sim.gpuSim(qc))
    ct_lis.append(sim.cpuSim(qc))

plt.plot(x, gt_lis, label='GPU')
plt.plot(x, ct_lis, label='CPU')
plt.legend()
plt.savefig('qftbenchmark.png')
