
import time
import random
import statistics
import csv
import os.path
import math

from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import QiskitError, execute, Aer
from myAlgo import shorNormal
#from qiskit_qcgpu_provider import QCGPUProvider


# Benchmarking functions
qiskit_backend = Aer.get_backend('qasm_simulator')
coupling_map = qiskit_backend.configuration().coupling_map
qcgpu_backend = QCGPUProvider(coupling_map).get_backend('qasm_simulator')
#qiskit_backend = Aer.get_backend('statevector_simulator')
#qcgpu_backend = QCGPUProvider().get_backend('statevector_simulator')


def bench_qiskit(qc):
    beg = time.time()
    job_sim = execute(qc, qiskit_backend)
    sim_result = job_sim.result()
    print(sim_result.get_counts())
    end = time.time()
    print(end-beg)
    return


def bench_qcgpu(qc):
    beg = time.time()
    job_sim = execute(qc, qcgpu_backend)
    sim_result = job_sim.result()
    print(sim_result.get_counts())
    end = time.time()
    print(end-beg)
    return


def benchmark():
    functions = bench_qcgpu, bench_qiskit
    qc = shorNormal(55, 21)
    bench_qiskit(qc)
    os.environ['PYOPENCL_CTX'] = '0:1'
    bench_qcgpu(qc)
    os.environ['PYOPENCL_CTX'] = '0:0'
    bench_qcgpu(qc)


if __name__ == '__main__':
    benchmark()
