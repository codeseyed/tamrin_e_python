# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 12:02:18 2020

@author: ok
"""
import numpy as np
from random import choice
from itertools import permutations, combinations


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

iteration = 5
solution = []
for i in range(iteration):
    B = sys_linear(4,4,16)
    b = const(4)
    x = np.linalg.solve(B,b)
    solution.append(x)
big_matrix = np.zeros((len(solution), len(solution[0])))

for i in range(len(big_matrix)):
    for j in range(len(big_matrix[0])):
        big_matrix[i][j] = solution[i][j]

def convrg(big_matrix):
    big_matrix_1 = np.zeros((len(big_matrix), len(big_matrix[0])))
    for i in range(len(big_matrix)):
        for j in range(len(big_matrix[0])):
            if i == 0 and j == 0:
                big_matrix_1[i][j] = (big_matrix[i][j+1] + big_matrix[i+1][j])/2
            if i == 0 and j != 0 and j != len(big_matrix[0]) - 1:
                big_matrix_1[i][j] = (big_matrix[i][j-1] + big_matrix[i][j+1] + big_matrix[i+1][j])/3
            if i == 0 and j == len(big_matrix[0]) - 1:
                big_matrix_1[i][j] = (big_matrix[i][j-1] + big_matrix[i+1][j])/2
            if i != 0 and j == 0:
                big_matrix_1[i][j] = (big_matrix[i+1][j] + big_matrix[i-1][j] + big_matrix[i][j+1])/3
            if i == len(big_matrix) -1 and j == 0:
                big_matrix_1[i][j] = (big_matrix[i-1][j] + big_matrix[i][j+1])/2
            if i == len(big_matrix) -1 and j != 0 and j != len(big_matrix[0])-1:
                big_matrix_1[i][j] = (big_matrix[i][j-1] + big_matrix[i-1][j]) + big_matrix[i][j+1]/3
            if i != 0 and i !=len(big_matrix) -1 and  j == len(big_matrix[0])-1:
                big_matrix_1[i][j] = (big_matrix[i][j-1] + big_matrix[i+1][j] + big_matrix[i-1][j])/3
            else:
                big_matrix_1[i][j] = (big_matrix[i+1][j] + big_matrix[i-1][j] + big_matrix[i][j+1] + big_matrix[i][j-1])/4
    return big_matrix_1

print(convrg(big_matrix))
    


