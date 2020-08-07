from qiskit.circuit.library import QFT
from qiskit import QuantumRegister, QuantumCircuit
from qiskit.visualization import plot_histogram
import simulation as sim
import argparse
import matplotlib.pyplot as plt
args = sim.process_command()
x = []
gt_lis = []
ct_lis = []
for i in range(2, 30):
    x.append(i)
    qr = QuantumRegister(i)
    qc = QuantumCircuit(qr)
    gate = QFT(i)
    qc.append(gate, qargs=qr[:])
    qc.measure_all()
    gt_lis.append(sim.gpuSim(qc))
    ct_lis.append(sim.cpuSim(qc))

plt.plot(x, gt_lis)
plt.plot(x, ct_lis)
plt.legend()
plt.savefig('qftbenchmark.png')
