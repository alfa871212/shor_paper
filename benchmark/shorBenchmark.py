import matplotlib.pyplot as plt

import simulation as sim
from myAlgo import shorNormal

qc_lis = []
qc_lis.append(shorNormal(15, 4))
qc_lis.append(shorNormal(21, 8))
qc_lis.append(shorNormal(33, 10))
qc_lis.append(shorNormal(35, 6))
qc_lis.append(shorNormal(39, 14))
N_lis = [15, 21, 33, 35, 39]
gt_lis = []
ct_lis = []
for i in range(5):
    gt_lis.append(sim.gpuSim(qc_lis[i]))
    ct_lis.append(sim.cpuSim(qc_lis[i]))

plt.plot(N_lis, gt_lis, label='GPU')
plt.plot(N_lis, ct_lis, label='CPU')
plt.legend()
plt.savefig('shorbenchmark.png')
