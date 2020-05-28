# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 20:45:07 2019

@author: Sudhish Kumar
"""

# Fibonacci Series as a recursive function
def Fibonacci(n):
    if n==1:
        return 1
    elif n<=0:
        return 0
    return Fibonacci(n-1) + Fibonacci(n-2)
#
print("-"*50)
print("\t".join([str(Fibonacci(x)) for x in range(0,10)]))
print("-"*50)
