# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 12:02:18 2020

@author: ok
"""
import numpy as np
from random import choice


# function to make a random n*m matrix  
def sys_linear(n,m,p):
    A = [0]*p
    for i in range(len(A)):
        A[i] = choice(range(100))
    B = np.reshape(A, (n,m))
     
    return B

# function to make a random vector with elements between 0 to 99 
def const(m):
    b = [0]*m
    for i in range(len(b)):
        b[i] = choice(range(100))
    return b
# function to take a matrix and make the average of elements and write the into a new matrix
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

# a function to calculate the forbenius norm of a given matrix
def recurese(big_matrix_1):
    forbenius = 0
    for i in range(len(big_matrix_1)):
        for j in range(len(big_matrix_1[0])):
            forbenius += (big_matrix_1[i][j])**2
    
    return forbenius
# finally, this part of code takes the random matrices and vectors as the input
#of systems of linear equations and combines the resultant vectos into a new matrix     
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

# this part of the code import big_matrix and at each of iteration campute the absolute difference 
#between two random elements and set it as convergance criteria
thresh = 1        
while thresh > 0.0000001:
    big_matrix = convrg(big_matrix)
    inices = []
    for i in range(len(big_matrix)):
        for j in range(len(big_matrix[0])):
            inices.append((i,j))
            
    random_index1 = choice(inices) #selecting a random element from big_matrix
    c = big_matrix[random_index1[0]][random_index1[1]]
    inices.remove(random_index1)
    
    random_index2 = choice(inices)
    d = big_matrix[random_index2[0]][random_index2[1]]
    
    thresh = abs(c-d)
    
print(big_matrix)

np.savetxt('big_matrix.csv', big_matrix, delimiter=',')


