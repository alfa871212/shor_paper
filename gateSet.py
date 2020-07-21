from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister
from qiskit.circuit.library import QFT, U1Gate, IGate
from qiskit.visualization import circuit_drawer, plot_histogram
import math
import numpy as np
import sys
import csv
import simulation as sim
from qiskit.aqua.utils.controlled_circuit import get_controlled_circuit
from sympy import mod_inverse
def myQFT(n,inverse=False):
    qr = QuantumRegister(n)
    gate = QFT(n, inverse=inverse, do_swaps=False).to_gate()
    gate.name = 'QFT'
    return gate


def myAQFT(n, appro, inverse=False):
    qr = QuantumRegister(n)
    gate = QFT(n, inverse=inverse, do_swaps=False,
               approximation_degree=appro).to_gate()
    gate.name = 'QFT'
    return gate


def adder_appro(a, b, n, appro):  # a+b in fourier space
    a_bin = bin(int(a))[2:].zfill(n)
    b_bin = bin(int(b))[2:].zfill(n)

    qr = QuantumRegister(2*n)
    cr = ClassicalRegister(n)
    qc = QuantumCircuit(qr, cr)
    for i in range(n):
        if a_bin[i] == '1':
            qc.x(i)

    for i in range(n):
        if b_bin[i] == '1':
            qc.x(n+i)

    qc.append(myAQFT(n, appro), qargs=qr[n:n*2])
    for i in range(1, n+1):
        for j in range(n-i+1):
            if a_bin[i+j-1] == '1':
                qc.cu1(2*math.pi/(2**i), i+j-1, n+j)
    qc.append(myAQFT(n, appro, inverse=True), qargs=qr[n: 2*n])

    for i in range(n):
        qc.measure(i+n, n-i-1)

    return qc


def adder(a, b, n):  # a+b in fourier space
    a_bin = bin(int(a))[2:].zfill(n)
    b_bin = bin(int(b))[2:].zfill(n)

    qr = QuantumRegister(2*n)
    cr = ClassicalRegister(n)
    qc = QuantumCircuit(qr, cr)
    for i in range(n):
        if a_bin[i] == '1':
            qc.x(i)
    for i in range(n):
        if b_bin[i] == '1':
            qc.x(n+i)

    qc.append(myQFT(n), qargs=qr[n:n*2])
    for i in range(1, n+1):
        for j in range(n-i+1):
            if a_bin[i+j-1] == '1':
                qc.cu1(2*math.pi/(2**i), i+j-1, n+j)

    qc.append(myQFT(n, inverse=True), qargs=qr[n: 2*n])

    for i in range(n):
        qc.measure(i+n, n-i-1)
    # circuit_drawer(qc,output='mpl',filename='./report/adder_prevent.png')

    return qc


def c_phase(num):
    qc = QuantumCircuit(1)
    ret = qc.to_gate()
    ret.name = f'{num}'
    return ret


def adder_latex(a, b, n):
    qr_a = QuantumRegister(n, name='a')
    qr_b = QuantumRegister(n, name='b')
    qc = QuantumCircuit(qr_a, qr_b)
    qc.append(QFT(n), qargs=qr_b[:])
    for i in range(0, n):
        for j in range(0, n-i):
            qc.append(c_phase(j+1).control(), qargs=[qr_a[j]]+[qr_b[i]])
        qc.barrier()
    qc.append(QFT(n, inverse=True), qargs=qr_b[:])
    circuit_drawer(qc, output='latex_source',
                   filename='./latex/test.tex', plot_barriers=False)


def gate_add(n, num):
    qc = QuantumCircuit(n)
    ret = qc.to_gate()
    ret.name = f'\phi ADD({num})'
    return ret


def modadder_latex():
    ctrl = QuantumRegister(2, name='ctrl')
    qr_b = QuantumRegister(3, name='b')
    ancilla_0 = QuantumRegister(1, name="anc")
    qc = QuantumCircuit(ctrl, qr_b, ancilla_0)
    two = gate_add(3, 'a').control(2)
    one = gate_add(3, 'N').control(1)
    no = gate_add(3, 'N')
    qc.append(QFT(3), qargs=qr_b[:])
    qc.append(two, qargs=ctrl[:]+qr_b[:])
    qc.append(no.inverse(), qargs=qr_b[:])
    qc.append(QFT(3, inverse=True), qargs=qr_b[:])
    qc.cx(qr_b[2], ancilla_0)
    qc.append(QFT(3), qargs=qr_b[:])
    qc.append(one, qargs=ancilla_0[:]+qr_b[:])
    qc.append(two, qargs=ctrl[:]+qr_b[:])
    qc.append(QFT(3, inverse=True), qargs=qr_b[:])
    qc.x(qr_b[2])
    qc.cx(qr_b[2], ancilla_0)
    qc.x(qr_b[2])
    qc.append(QFT(3), qargs=qr_b[:])
    qc.append(two, qargs=ctrl[:]+qr_b[:])
    circuit_drawer(qc, output='latex_source', filename='./report/mod.png')


def phiADD(bitlen, a):
    a_bin = bin(int(a))[2:].zfill(bitlen)
    qr = QuantumRegister(bitlen)
    qc = QuantumCircuit(qr)
    for i in range(1, bitlen+1):
        for j in range(bitlen-i+1):
            if a_bin[i+j-1] == '1':
                qc.u1(2*math.pi/(2**i), qr[j])
    qc.name = f'phiADD{a}'
    return qc


def ctrl_phiADD(bitlen, a):
    gate = phiADD(bitlen, a).to_gate().control(1)
    gate.name = f'cphiADD{a}'
    return gate


def cc_phiADD(bitlen, a):
    gate = phiADD(bitlen, a).to_gate().control(2)
    gate.name = f'ccphiADD{a}'
    return gate


def ccphiADDmodN(n, a, b, N, print_qc=False, save_fig=False):

    if a % N != 0:
        a = a % N  # make sure a<N and a!=0
    else:
        a = N

    bitlen = n+1
    qr_ctrl = QuantumRegister(2, name='ctrl')
    qr_phi = QuantumRegister(bitlen, name='phi')
    qr_ancilla = QuantumRegister(1, name='ancilla')

    qc = QuantumCircuit(qr_ctrl, qr_phi, qr_ancilla)

    # gates preparetion
    cc_phi_add_a = cc_phiADD(bitlen, a)
    cc_phi_add_a_inv = cc_phiADD(bitlen, a).inverse()

    phi_add_N = phiADD(bitlen, N).to_gate()
    phi_add_N_inv = phi_add_N.inverse()

    phi_add_control = ctrl_phiADD(bitlen, N)

    qft_gate = myQFT(bitlen, inverse=False)
    iqft_gate = myQFT(bitlen, inverse=True)

    qc.append(cc_phi_add_a, qargs=qr_ctrl[:]+qr_phi[:])
    qc.append(phi_add_N_inv, qargs=qr_phi[:])
    qc.append(iqft_gate, qargs=qr_phi[:])
    qc.cx(qr_phi[0], qr_ancilla)
    qc.append(qft_gate, qargs=qr_phi[:])
    qc.append(phi_add_control, qargs=qr_ancilla[:]+qr_phi[:])
    qc.append(cc_phi_add_a_inv, qargs=qr_ctrl[:]+qr_phi[:])
    qc.append(iqft_gate, qargs=qr_phi[:])
    qc.x(qr_phi[0])
    qc.cx(qr_phi[0], qr_ancilla)
    qc.x(qr_phi[0])
    qc.append(qft_gate, qargs=qr_phi[:])
    qc.append(cc_phi_add_a, qargs=qr_ctrl[:]+qr_phi[:])
    if print_qc:
        print(qc)
    if save_fig:
        filename = f'./report/ccphiADD{a}MOD{N}_{b}.png'
        circuit_drawer(qc, scale=1.4, filename=filename, output='mpl', style={
                       'fontsize': 20}, plot_barriers=False)
        # qc.draw(output='mpl').savefig(filename)
    gate = qc.to_gate()
    gate.name = f'ccphiADD{a}MOD{N}'

    return gate


def ccgate_latex(n, pow):
    qc = QuantumCircuit(n)
    ret = qc.to_gate()
    ret.name = f'\phiADD2^{pow}aMOD(N)'
    return ret


def cmult_latex():
    ctrl = QuantumRegister(1, name='ctrl')
    x = QuantumRegister(3, name='x')
    b = QuantumRegister(4, name='b')
    qc = QuantumCircuit(ctrl, x, b)
    qc.append(QFT(4), qargs=b[:])
    for i in range(3):
        gate = ccgate_latex(4, i).control(2)
        qc.append(gate, qargs=ctrl[:]+[x[i]]+b[:])
    qc.append(QFT(4, inverse=True), qargs=b[:])
    circuit_drawer(qc, output='latex_source', filename='./latex/cmult.tex')
    print(qc)


def cmult_a_mod_N(n, a, b, N, print_qc=False, save_fig=False):
    bitlen = n+1
    qr_c = QuantumRegister(1, name='c')
    qr_x = QuantumRegister(n, name='x')
    qr_b = QuantumRegister(bitlen, name='b')
    qr_ancilla = QuantumRegister(1, name='ancilla')
    qc = QuantumCircuit(qr_c, qr_x, qr_b, qr_ancilla)

    qft = myQFT(bitlen, inverse=False)
    iqft = myQFT(bitlen, inverse=True)

    qc.append(qft, qargs=qr_b[:])
    for i in range(n):
        gate = ccphiADDmodN(n, (2**i)*a, b, N)
        qc.append(gate, qargs=qr_c[:]+[qr_x[n-1-i]]+qr_b[:]+[qr_ancilla[0]])
    qc.append(iqft, qargs=qr_b[:])
    if print_qc:
        print(qc)
    if save_fig:
        circuit_drawer(qc, scale=0.7, output='mpl',
                       filename='./report/cmult.png')

    gate = qc.to_gate()
    gate.name = f'cMULT{a}MOD{N}'
    return gate


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, N):
    g, x, y = egcd(a, N)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % N


def cu_a(n, a, N, print_qc=False, save_fig=False):
    bitlen = n+1
    qr_c =QuantumRegister(1,name='c')
    qr_x = QuantumRegister(n,name='x')
    qr_b_0=QuantumRegister(bitlen+1,name='b0')
    qc = QuantumCircuit(qr_c,qr_x,qr_b_0)
    a=a%N
    ainv=modinv(a,N)
    #ainv = mod_inverse(a,N)
    ainv=ainv%N
    gate = cmult_a_mod_N(n,a,0,N,print_qc=False)
    invgate = cmult_a_mod_N(n,ainv,0,N,print_qc=False).inverse()
    qc.append(gate,qargs=qr_c[:]+qr_x[:]+qr_b_0[:])
    for i in range(n):
        qc.cswap(qr_c, qr_x[i], qr_b_0[i+1])
    qc.append(invgate, qargs=qr_c[:]+qr_x[:]+qr_b_0[:])
    if print_qc:
        print(qc)
    if save_fig:
        circuit_drawer(qc, output='mpl', scale=0.8,
                       filename='./report/cua.png')
    gate = qc.to_gate()
    gate.name = f'cu{a}mod{N}'
    return gate


def cu_latex_gate(inv):
    qr = QuantumRegister(2)
    qc = QuantumCircuit(qr)
    ret = qc.to_gate()
    if not inv:
        ret.name = 'cMULT(a)MODN'
    else:
        ret.name = 'cMULT(ainv)MODN'
    return ret


def cu_latex():
    ctrl = QuantumRegister(1, name='ctrl')
    x = QuantumRegister(1, name='x')
    zero = QuantumRegister(1, name='zero')
    qc = QuantumCircuit(ctrl, x, zero)
    gate = cu_latex_gate(False).control()
    inv = cu_latex_gate(True).control()
    qc.append(gate, qargs=ctrl[:]+x[:]+zero[:])
    qc.cswap(ctrl, x, zero)
    qc.append(inv, qargs=ctrl[:]+x[:]+zero[:])
    circuit_drawer(qc, output='latex_source', filename='./latex/cu.tex')


def shor_gate_latex(n, i):
    qc = QuantumCircuit(n)
    ret = qc.to_gate()
    ret.name = f'Ua{i}'
    return ret


def shor_normal_latex(n):
    up = QuantumRegister(2*n, name='up')
    down = QuantumRegister(n, name='down')
    down_b = QuantumRegister(n, name='b')
    ancilla = QuantumRegister(2, name='ancilla')
    qc = QuantumCircuit(up, down, down_b, ancilla)
    qc.x(down[n-1])
    for i in range(2*n):
        qc.append(shor_gate_latex(2*n+2, i).control(),
                  qargs=[up[i]]+down[:]+down_b[:]+ancilla[:])
    qc.append(QFT(2*n, inverse=True), qargs=up[:])
    print(qc)
    circuit_drawer(qc, output='latex_source', filename='./latex/normal.tex')


def r_gate_latex(i):
    qc = QuantumCircuit(1)
    ret = qc.to_gate()
    ret.name = f'R{i}'
    return ret


def shor_seq_latex(n):
    ctrl = QuantumRegister(1, name='ctrl')
    down = QuantumRegister(n, name='x')
    down_b = QuantumRegister(n+1, name='b')
    ancilla = QuantumRegister(1, name='ancilla')
    qc = QuantumCircuit(ctrl, down, down_b, ancilla)
    cr_lis = []
    for i in range(0, 2*n):
        cr = ClassicalRegister(1)
        qc.add_register(cr)
        cr_lis.append(cr)
    qc.x(down[n-1])
    for i in range(2*n):
        qc.x(ctrl).c_if(cr_lis[i], 1)
        qc.h(ctrl)

        qc.append(shor_gate_latex(2*n+2, i).control(),
                  qargs=ctrl[:]+down[:]+down_b[:]+ancilla[:])
        qc.h(ctrl)
        # qc.measure(ctrl,i)
        qc.measure(ctrl, cr_lis[i])
        gate = r_gate_latex(i)
        qc.append(gate, qargs=ctrl[:])
    print(qc)
    circuit_drawer(qc, output='latex_source', filename='./latex/seq.tex')


def myR(i, neighbor_range, cr_lis):
    qr = QuantumRegister(1)
    qc = QuantumCircuit(qr)
    for j in neighbor_range:
        theta = math.pi/float(2**(j+1))
        gate = U1Gate(theta, i+(j+1)).c_if(cr_lis[i], 1)
        qc.append(gate, qargs=qr[:])
    gate = qc.to_gate()
    gate.name = f'R_{i}'
    return gate
