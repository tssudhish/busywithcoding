# -*- coding: utf-8 -*-
"""
Created on Sun May 24 09:40:14 2020

@author: Sudhish Kumar
"""

from random import choice
def get_sum_of_numbers(input_number, number_of_splits):
    seq=range(1,input_number)
    while True:
        num_list=[]
        seq_set=set(seq)
        for i in range(0,number_of_splits):
            # print(seq_set)
            num_list.append(choice(list(seq_set)))
            try:
                seq_set.remove((num_list[-1]))
            except:
                return False
        # print(num_list)
        if sum(num_list) == input_number:
            break
    return num_list
trial_list=[]
trial_sol=[]
minnum=27
for trial in range(1,1000):
    print("Trial Number: {}".format(trial))
    l2=l3=l4=l5=[]
    for num in range(15,minnum):
        # print("Looking for num {}".format(num))
        icounter = 100
        counter=0
        found=False
        while counter<icounter:
            two,three,four,five=2,3,4,5
            l2=get_sum_of_numbers(num,two)
            l3=get_sum_of_numbers(num,three)
            l4=get_sum_of_numbers(num,four)
            l5=get_sum_of_numbers(num,five)
            num_uniq=len(set(l2+l3+l4+l5))
            # print(num_uniq)
            total=len(l2)+len(l3)+len(l4)+len(l5)
            # print(total)
            if num_uniq==total:
                found=True
                break
            counter+=1
        if found:
            print("Solution found afer iteration = {}".format(num))
            if minnum>=num:
                minnum=min(minnum,num)
                list_of_list=[l2,l3,l4,l5]
                print("Number: {}\n {}\n".format(minnum, list_of_list))
                
                trial_list.append(minnum)
                trial_sol.append(list_of_list)
            break
        
        





       
        
        
        
        
        


