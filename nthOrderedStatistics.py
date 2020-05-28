# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 21:25:03 2019

@author: Sudhish Kumar
"""
# ordered statistics

def nthOrderedElement(inputArr, orderNumber):
    orderedVal=inputArr[orderNumber-1]
    for idx,elem in enumerate(inputArr):
        if (orderedVal>elem and idx>(orderNumber-1)) or \
        (orderedVal<elem and idx<(orderNumber-1)):
            orderedVal=elem
    return orderedVal
    pass

inputArr=[3,2,15,6,10,21,15]
i = int(input("Enter the nth Order you want:"))

print("-"*50)
print("nthOrderedElement(inputArr, " + str(i) +") = " + str(nthOrderedElement(inputArr, i)))
print("-"*50)