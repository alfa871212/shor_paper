import math
import csv
import sys,os
def sumLis(b):
    ret=0
    temp=0
    for i in range(0,len(b)-1):
        temp=1/(b[-(i+1)]+temp)
    ret = temp+b[0]
    return ret
    
        
def myCF(x_value,t_upper,N,a):
    if x_value<=0:
        print("Wrong x_value\n")
        return False

    T=math.pow(2,t_upper)
    x_over_T = x_value/T
    temp = x_over_T
    threshold = 1/(2*T)
    b=[]
    t=[]
    
    i=0
    while i>=0:
        appro=0
        b.append(math.floor(temp))
        t.append(temp-b[i])
        if t[i]==0:
            print("Found exact expansion!")
            print("The expansion is "+str(x_over_T)+'\n')
            r = b[i]
            return checkFactor(r,N,a)
                         
        temp = 1/t[i]
        appro = sumLis(b)
        print("This is {0} appro: {1}".format(i,appro))
        
        if abs(appro-x_over_T)<threshold:
            r = b[i]
            return checkFactor(r,N,a)
        i+=1
        if i > 10:
            print("Too many approximation! Go to the next case!")

   
def checkFactor(r,N,a):
    if r%2==0:
        exponential = math.pow(a,r/2)
        plus = int(exponential+1)
        minus = int(exponential-1)
        maxiter_2 = 15
        p_factor = math.gcd(plus,N)
        q_factor = math.gcd(minus,N)
        if p_factor==1 or p_factor==N or q_factor==1 or q_factor==N:
            print('Found just trivial factors, not good enough\n')
            return False                  
        else:
            print('The factors of {0} are {1} and {2}\n'.format(N,p_factor,q_factor))
            print('Found the desired factors!\n')               
            return True
    else:
        print("The estimated r is odd, try other cases!\n")


def modInverse(a, m) : 
    a = a % m; 
    for x in range(1, m) : 
        if ((a * x) % m == 1) : 
            return x 
    return 1
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
def factorize_res(filename,a,n,N,type):
    print("Dealing with {0}".format(filename))
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        #data=sorted(data,key=lambda x : int(x[1]),reverse=True)
    #print(data)
    failed = True
    success_lis=[]
    for i in range(0,len(data)):#len(counts_result)):

        measure_res = data[i]
        res_key = data[i][0]
        
        x_value = int(res_key,2)
   
        if type==1:
            frac = x_value/math.pow(2,2*n)
        else:
            frac = x_value/math.pow(2,2*n)
        print("Analysing result {0}, which in decimal is {1}. Analyzing fraction: {2} \n".format(measure_res[0],int(x_value),frac))
        
        success =myCF(x_value,int(2*n),int(N),int(a))
   
               
        if success:
            failed = False
            success_lis.append((N,a,measure_res[0]))
            break
        else:
            print("The probability is too small, this should be trivial case!")
            break
    if type==1:
        put = 'seq'
    else:
        put = 'nor'
    with open(f'./{a}_succ_{put}.csv','w') as out:
        w = csv.writer(out, delimiter='\t')        # override for tab delimiter
        w.writerows(success_lis)  
    if failed:
        print("Factorization failed!")
        return 0
