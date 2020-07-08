from myAlgo import *
import simulation as sim
import matplotlib.pyplot as plt
if __name__=="__main__":
    args = sim.process_command()
    #test_adder(1,3,3,args)
    #modadder_latex()
    #adder_latex(0,0,4)
    #cmult_latex()
    '''
    for i in range(3):
        test_adder_appro(3,3,3,i,args)
    '''
    #test_ccphiMOD(3,3,3,5,args,False,True)
    #test_adder(3,3,3,args)
    #gate=cmult_a_mod_N(n=4,a=4,b=5,N=9,print_qc=True)
    #print(gate.num_qubits)
    #testCMULT(n=4,x=2,b=7,a=9,N=9,print_qc=True)
    #shorSequential(N=15,a=4,save_fig=True)
    #testCMULT(n=2,x=3,b=5,a=3,N=4,args=args,save_fig=True)
    #CMULTexp_latex(n=2,x=3,b=5,a=3,N=4,args=args,save_fig=True)
    #cu_latex()
    #test_cu(n=2,x=3,a=5,N=4,args=args)
    #shor_normal_latex(2)

    
    #shorNormal(N=15,a=4,args=args)
    
    for i in range(2,15):
        if math.gcd(i,15)==1:
            #qc=shorNormal_circuit(N=15,a=i,args=args)
            #res=sim.mySim(qc,args)
            #plot_histogram(res,title=f'N = 15, a = {i}').savefig(f'./normal/result/{N}_{i}_res.png')
            #leg.append(str(i))
            #shorNormal(N=15,a=i,args=args)
            shorSequential(N=15,a=i,args=args)
    #plot_histogram(res,legend=leg,color=colour).savefig('./all.png')
    
    #shorSequential(N=15,a=2,args=args)
    #$shor_normal_latex(2)
    #shorNormal(15,4)