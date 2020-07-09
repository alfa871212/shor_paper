import argparse
import math
def sumLis(b):
    ret=0
    temp=0
    for i in range(0,len(b)-1):
        temp=1/(b[-(i+1)]+temp)
    ret = temp+b[0]
    return ret
    
        
def myCF(x_value,t_upper,N,a,args):
    if args.verbose:
        print(f'The result = {x_value}')
        if x_value <= 0:
            print("The result is not suitable. ")
            return False
        T=math.pow(2,t_upper)
        threshold = 1/(2*T)
        x_over_T = x_value/T
        temp = x_over_T
        print(f'Analyzing fraction {x_value/T}')
        print(f'CF threshold = {T}')
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