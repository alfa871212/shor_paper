from myAlgo import shorNormal
import simulation as sim
args=sim.process_command()
qc = shorNormal(15,4)
sim.mySim(qc,args)
sim.gpuSim(qc)