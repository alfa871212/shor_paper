import qiskit as qk
qk.IBMQ.load_account()
import time
import matplotlib.pyplot as plt
import os
import argparse

def sort_by_key(result):
    bitlen = len(next(iter(result.keys())))
    sorted_result = [('{n:0{b}b}'.format(n=i, b=bitlen), 
        result.get('{n:0{b}b}'.format(n=i, b=bitlen), 0)) 
        for i in range(2**bitlen)]
    return sorted_result

def sort_by_prob(result):
    return sorted([(k, result[k]) for k in result.keys()], key=lambda x: x[1], 
            reverse=True)
def ind_mySim(cir):
    provider = qk.IBMQ.get_provider('ibm-q-hub-ntu')
    backend =qk.Aer.get_backend('qasm_simulator')
    #backend = provider.get_backend('ibmq_qasm_simulator')

    sim_res = qk.execute(cir,backend,shots=1,optimization_level=1)
    qk.tools.job_monitor(sim_res)
    sim_result=sim_res.result()
    counts=sim_result.get_counts()
    
    return counts
def mySim(cir,args,method='qasm'):
    
    provider = qk.IBMQ.get_provider('ibm-q-hub-ntu')
    sim_type = method+'_simulator'
    
    if args.real:
        backend = provider.get_backend('ibmq_cambridge')   
    else:     
        if args.simulation=='local':
            backend = qk.Aer.get_backend(sim_type)
        elif args.simulation=='ibmq':
            backend = provider.get_backend('ibmq_qasm_simulator')
        else:
            print("Choose default backend...local.")
            backend = qk.Aer.get_backend(sim_type)

    try:
        sim_res = qk.execute(cir,backend,shots=8192,optimization_level=3)
        
        qk.tools.job_monitor(sim_res)
        sim_result=sim_res.result()
        job_uid = sim_res.job_id()
            
        counts_result = sim_result.get_counts(cir)
    except Exception as e:
        print(e)
        if e==Exception('IBMQJobFailureError'):
            print(sim_res.error_message())
    
    #print(counts_result)
    return counts_result

def process_command():
    parser = argparse.ArgumentParser()
    method = parser.add_mutually_exclusive_group()
    method.add_argument('--simulation','--sim','-s',metavar='local/ibmq')
    method.add_argument('--real','-r',action='store_true')

    gate = parser.add_mutually_exclusive_group(required=True)
    gate.add_argument('--adder',nargs=3,type=int,metavar=('a','b','n'))
    gate.add_argument('--phimod',nargs=4,type=int,metavar=('n','b','a','N'))
    gate.add_argument('--cmult',nargs=5,type=int,metavar=('n','x','b','a','N'))
    gate.add_argument('--cu',nargs=4,type=int,metavar=('n','x','a','N'))
    gate.add_argument('--nor',nargs=2,type=int,metavar=('N','a'))
    gate.add_argument('--seq',nargs=2,type=int,metavar=('N','a'))

    #parser.add_argument('--test','-t',required=True, metavar='gate/algo')
    parser.add_argument('--output','-o',action='store_true')
    parser.add_argument('--draw','-d',action='store_true')
    parser.add_argument('--log','-l',action='store_true')
    #parser.add_argument('--parameter','--para','-p',required=True,metavar='parameter')
    return parser.parse_args()
