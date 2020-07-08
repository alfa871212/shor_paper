import qiskit as qk
qk.IBMQ.load_account()
import time
import matplotlib.pyplot as plt
import os
import argparse

def local_sim(qc, figname='local_sim.pdf', printresult=True, shots=1024):
    print('Local simulation started.')
    backend = qk.Aer.get_backend('qasm_simulator') 
    job_sim = qk.execute(qc, backend,shots=shots)
    sim_result = job_sim.result()
    print('Simulation finished.')
    measurement_result = sim_result.get_counts(qc)

    if printresult:
        print('Simulation result:', measurement_result)
        qk.visualization.plot_histogram(measurement_result).savefig('./results'+figname)
        print('Simulation plotted and saved locally.')

    return measurement_result

def quantumComputerExp(qc, backend=None, shots=8192, 
        mode='least_busy', verbose=True, loopexp=1, printresult=True,
        layout=None, optimize=None, note=None, accuracy_func=None):

    timestart = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    shorttime = time.strftime("%Y%m%d%H%M%S",time.localtime())

    if loopexp < 1:
        raise ValueError('Number of loop mus be larger or equal to 1.')

    if loopexp > 1:
        indent = '    |   '
    else: 
        indent = ''

    overall_result = {}

    neatfilename = os.path.splitext(os.path.split(__main__.__file__)[1])[0]

    if verbose:
        print('Experiment started.')
        print('Loading account...')
    account = qk.IBMQ.load_account()
    ntu_provider = qk.IBMQ.get_provider(hub='ibm-q-hub-ntu', group='ntu-internal',
            project='default')
    if verbose:
        print('Account loaded')

    if backend != None:
        _backend = ntu_provider.get_backend(backend)

    elif mode == 'least_busy':
        if verbose:
            print('Finding backend...')
        _backend = qk.providers.ibmq.least_busy(ntu_provider.backends(filters=lambda x:
            x.configuration().n_qubits >= qc.qregs[0].size and
            not x.configuration().simulator and 
            x.status().operational==True))

    elif mode == 'simulate':
        _backend = account.get_backend('ibmq_qasm_simulator') 

    else:
        raise ValueError('Invalid experiment mode')

    with open(f'log_expdata_{neatfilename}.log', 'a') as f:
        if loopexp > 1:
            f.write('Loop job start:\n')

        for i in range(1, loopexp+1):

            if loopexp > 1:
                print(f'    Loop {i}:')

            try:
                if verbose:
                    print(indent+'Using backend:', _backend)
                    print(indent+f'Job {i} started.')
                job = qk.execute(qc, backend=_backend, shots=shots, initial_layout=layout,
                        optimization_level=optimize)
                if verbose:
                    qk.tools.monitor.job_monitor(job)
                    print(indent+'done')
                result = job.result()
                result_count = result.get_counts()

                if printresult and (loopexp==1):
                    print(indent+'Result:', result_count)
                    _title = 'file: {f}, backend: {be}, qreg size: {qs}, shots:{sh}'.format(
                            f=__main__.__file__, be=_backend._configuration.backend_name,
                            qs=qc.qregs[0].size, sh=shots)
                    if note != None:
                        _title += f' {note}'

                    figname =  f'./results/{shorttime}_expresult_{neatfilename}'
                    if note != None:
                        figname += f'_{note}'
                    qk.visualization.plot_histogram(result_count, title=_title).savefig(
                            f'{figname}.pdf')
                    if accuracy_func != None:
                        print(indent+'Accuracy:', accuracy_func(result_count))

                # sort result
                bitlen = qc.cregs[0].size
                result_list = [('{b:0{l}b}'.format(b=i, l=bitlen), 
                    result_count.get('{b:0{l}b}'.format(b=i, l=bitlen), 0)) for i in range(2**bitlen)]
                
                if verbose:
                    print(indent+'writing log')
                    f.write(f'{indent}\n')
                    if loopexp == 1:
                        f.write(indent+'Record start\n')
                    else:
                        f.write(indent+f'Record start (partial job {i}/{loopexp})\n')
                    f.write(indent+'file: '+__main__.__file__+'\n')
                    f.write(indent+'Time stamp: '+time.strftime(
                        "%Y-%m-%d %H:%M:%S",time.localtime())+'\n')
                    if note != None:
                        f.write(f'Note: {note}\n')
                    f.write(indent+'Backend: '+_backend._configuration.backend_name+'\n')
                    f.write(indent+'Qubits: '+str(_backend._configuration.n_qubits)+'\n')
                    f.write(indent+'Basis gates: '+', '.join(
                        _backend._configuration.basis_gates)+'\n')
                    f.write(indent+'Shots: '+str(shots)+'\n')
                    f.write(indent+'Max shots: '+str(_backend._configuration.max_shots)+'\n')
                    f.write(indent+'creg size: '+str(qc.cregs[0].size)+'\n')
                    f.write(indent+'qreg size: '+str(qc.qregs[0].size)+'\n')
                    f.write(f'{indent}\n')
                    for b, c in result_list:
                        f.write(indent+b+': '+str(c)+'\n')
                    f.write(f'{indent}\n')
                    f.write(indent+'Record end\n')
                    f.write(f'{indent}\n')

                if loopexp > 1:
                    for key in result_count:
                        overall_result[key] = overall_result.get(key, 0) + result_count[key]

            except Exception as e:
                print(indent+'Job {i} failed.')
                print(indent+str(e))
                f.write(indent+'Job {i} failed.')
                f.write(indent+str(e))

        if loopexp > 1:
            if printresult:
                print('Result:', overall_result)
                qk.visualization.plot_histogram(result_count).savefig(
                        f'./results/{shorttime}_expresult_{neatfilename}.pdf')
                if accuracy_func != None:
                    print(indent+'Accuracy:', accuracy_func(overall_result))
            if verbose:
                print('writing log')

            bitlen = qc.cregs[0].size
            overall_result_list = [('{b:0{l}b}'.format(b=i, l=bitlen), 
                overall_result.get(
                    '{b:0{l}b}'.format(b=i, l=bitlen), 0)) for i in range(2**bitlen)]

            f.write('\n')
            f.write('Overall record start\n')
            f.write('file: '+__main__.__file__+'\n')
            f.write('Time start: '+timestart+'\n')
            f.write('Time end: '+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())+'\n')
            f.write('Backend: '+_backend._configuration.backend_name+'\n')
            f.write('Qubits: '+str(_backend._configuration.n_qubits)+'\n')
            f.write('Basis gates: '+', '.join(_backend._configuration.basis_gates)+'\n')
            f.write(f'Loop: {loopexp}\n')
            f.write('Total shots: '+str(shots*loopexp)+'\n')
            f.write('Max shots: '+str(_backend._configuration.max_shots)+'\n')
            f.write('creg size: '+str(qc.cregs[0].size)+'\n')
            f.write('qreg size: '+str(qc.qregs[0].size)+'\n')
            f.write('\n')
            for b, c in overall_result_list:
                f.write(b+': '+str(c)+'\n')
            f.write('\n')
            f.write('Overall record end\n')
            f.write('\n')
    
    if verbose:
        print('returning result')
    return result_count


def sort_by_key(result):
    bitlen = len(next(iter(result.keys())))
    sorted_result = [('{n:0{b}b}'.format(n=i, b=bitlen), 
        result.get('{n:0{b}b}'.format(n=i, b=bitlen), 0)) 
        for i in range(2**bitlen)]
    return sorted_result

def sort_by_prob(result):
    return sorted([(k, result[k]) for k in result.keys()], key=lambda x: x[1], 
            reverse=True)

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
            raise Exception("No matched backend!")

    sim_res = qk.execute(cir,backend,shots=8192,optimization_level=3)
    
    qk.tools.job_monitor(sim_res)
    sim_result=sim_res.result()
    job_uid = sim_res.job_id()
        
    counts_result = sim_result.get_counts(cir)
    
    #print(counts_result)
    return counts_result

def process_command():
    parser = argparse.ArgumentParser()
    method = parser.add_mutually_exclusive_group()
    method.add_argument('--simulation','--sim','-s',metavar='local/ibmq')
    method.add_argument('--real','-r',action='store_true')
    
    parser.add_argument('--output','-o',action='store_true')
    parser.add_argument('--draw','-d',action='store_true')
    parser.add_argument('--log','-l',action='store_true')
    return parser.parse_args()
