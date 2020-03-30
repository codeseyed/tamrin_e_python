# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 12:02:18 2020

@author: ok
"""
import numpy as np
from random import choice



def sys_linear(n,m,p):
    A = [0]*p
    for i in range(len(A)):
        A[i] = choice(range(100))
    B = np.reshape(A, (n,m))
     
    return B

def const(m):
    b = [0]*m
    for i in range(len(b)):
        b[i] = choice(range(100))
    return b

def convrg(big_matrix):
    big_matrix_1 = np.zeros((len(big_matrix), len(big_matrix[0])))
    for i in range(len(big_matrix)):
        
        for j in range(len(big_matrix[0])):

            total_sum = big_matrix[i][j]
            num = 0

            if i == 0:
                total_sum = big_matrix[i+1][j]
                num += 1
            elif i < len(big_matrix) - 1:
                total_sum = big_matrix[i-1][j] + big_matrix[i+1][j]
                num += 2
            else:
                total_sum = big_matrix[i-1][j]
                num+= 1
                

            if j == 0:
                total_sum += big_matrix[i][j+1]
                num += 1
            elif j < len(big_matrix[0]) - 1:
                total_sum += big_matrix[i][j-1] + big_matrix[i][j+1]
                num += 2
            else:
                total_sum += big_matrix[i][j-1]
                num += 1
                
            big_matrix_1[i][j] = total_sum/num

    return big_matrix_1

def recurese(big_matrix_1):
    forbenius = 0
    for i in range(len(big_matrix_1)):
        for j in range(len(big_matrix_1[0])):
            forbenius += (big_matrix_1[i][j])**2
    
    return forbenius
    
iteration = 5
solution = []
for i in range(iteration):
    B = sys_linear(4,4,16)
    b = const(4)
    x = np.linalg.solve(B,b)
    solution.append(abs(x))
big_matrix = np.zeros((len(solution), len(solution[0])))

for i in range(len(big_matrix)):
    for j in range(len(big_matrix[0])):
        big_matrix[i][j] = solution[i][j]


    


