# A general implementation of Shor's algorithm in IBMQ

Following the order of https://arxiv.org/abs/quant-ph/0205095, I construct the Shor's circuit from the basic gates.

## Getting Started
For the access of the real quantum devices, you are recommended to register an IBMQ account.


### Prerequisites

You should install qiskit (Anaconda environment preferred) to run my code on your machine or using https://quantum-computing.ibm.com/ instead.

```
pip install qiskit 
```
## Structure
* [shor.py](https://github.com/alfa871212/shor_paper/blob/master/shor.py) is the main program.
* [gateSet.py](https://github.com/alfa871212/shor_paper/blob/master/gateSet.py) implements the gates needed in Shor's algorithm.
* [myAlgo.py](https://github.com/alfa871212/shor_paper/blob/master/myAlgo.py) implements the test of gates and algorithm.
* [simulation.py](https://github.com/alfa871212/shor_paper/blob/master/simulation.py) implements the simulation function and argparse in the main program.
* [CF.py](https://github.com/alfa871212/shor_paper/blob/master/CF.py) implements the continuous fraction algorithm and factorize the given N and a.
* [factorize.py](https://github.com/alfa871212/shor_paper/blob/master/factorize.py) implements the factorizing main program.

In this repo, I would separate the Shor's algorithm into two parts. First is the circuit experient which would generate results in /normal/result/ or /sequential/result/ depending on the circuit mode. Then run the factorizing part for the factorization.
## Run
In [shor.py](https://github.com/alfa871212/shor_paper/blob/master/shor.py), the execution flag is listed below
```
python shor.py [-h] [--simulation local/ibmq | --real]
               (--adder a b n | --phimod n b a N | --cmult n x b a N | --cu n x a N | --nor N a | --seq N a)
               [--output] [--draw] [--log]

```
Flag explanation:
Backend selection:
```
[-s|-r] select the backend to simulate the circuit, default is local simulator
```
Test selection:
```
--adder adder test 
--phimod modular adder test 
--cmult multiplier test 
--cu CU test
--nor Normal Shor's algorithm
--seq Sequential Shor's algorithm
```
Result selection:
```
--output plot the result histogram
--draw export a png file of circuit
--log redirect the stdout to file
```
For example, adder test with a=2 b=3 n=3, we want to do the a+b in n-bit number.
```
python shor.py -s local --adder 2 2 3 
```

In [factorize.py](https://github.com/alfa871212/shor_paper/blob/master/factorize.py),
```
factorize.py [-h] [--type seq/nor] [--individual res len N a | --file N a] [--log]
```
Result selection:
```
--indiv just give the result and N,a 
--file visit result csv file
```
Type selection (--file required):
```
--type choose the type of circuit, it should directly visit corresponding directory.
```
Logfile selection:
```
--log redirect log to file
```
For example, I want to individually factorize the result 10100000 for 8 bit number with N=15 a=4.
```
python factorize.py --indiv 10100000 8 15 4
```
Or, I want to factorize a given csv file sequential/result/15_4.csv.
```
python factorize.py --file 15 4 --type seq
```
