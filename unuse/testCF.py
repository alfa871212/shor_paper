from CF import *
import csv


path = ['./normal/result/','./sequential/result/']
N = 15 
n = math.ceil(math.log(N,2))
for i in range(2,15):
    for j in range(2):
        if math.gcd(N,i)==1:
            filename = path[j]+f'15_{i}.csv'
            factorize_res(filename,i,n,N,j)