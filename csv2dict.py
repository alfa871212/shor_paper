import csv
from qiskit.visualization import plot_histogram
import argparse
import math


def process_command():
    parser = argparse.ArgumentParser()
    method = parser.add_mutually_exclusive_group(required=True)
    method.add_argument('--normal', '--nor', action='store_true')
    method.add_argument('--sequential', '--seq', action='store_true')
    parser.add_argument('-N', metavar='N', type=str, required=True)

    method2 = parser.add_mutually_exclusive_group(required=True)
    method2.add_argument('-a', metavar='a', type=str)

    method2.add_argument('--all', action='store_true')
    return parser.parse_args()


def plot_from_csv(path, N, a):
    filename = path+N+'_'+str(a)+'.csv'
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = dict(list(reader))
    # print(data)
    plot_histogram(data, figsize=(10, 10), title=f'N={N} a={a} result(Nor)').savefig(
        path+f'/{N}_{a}_res.png')


if __name__ == "__main__":
    args = process_command()
    if args.normal:
        path = './normal/result/'
    elif args.sequential:
        path = './sequential/result/'
    else:
        raise Exception("Type not defined")
    N = args.N
    if args.all:
        for i in range(2, int(N)):
            if math.gcd(i, int(N)) == 1:
                plot_from_csv(path, N, i)
    else:
        plot_from_csv(path, N, args.a)
