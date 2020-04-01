#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 19:11:54 2020

@author: gongotar
"""
import numpy as np
from random import choice
import matplotlib.pyplot as plt

# generate n * m 2D array with random numbers
def randomarray(n,m):
    array = np.zeros((n,m))
    for i in range(len(array)):
        for j in range(len(array[i])):  
            array[i][j] = choice(np.arange(0,20, dtype=np.int)) #assignign random number between 0 to 10 to each of matrix elements 
    return array
# store it in file
random_matrix = randomarray(8,8)
print(random_matrix)
np.savetxt('random_matrix.csv', random_matrix, delimiter=',', fmt='%d')
# compute average of each cell with its neighbours until converge
def neigh_average(random_matrix):
    averaged_matrix = np.zeros((len(random_matrix),len(random_matrix[0]))) #producing n*m zero matrix
    for i in range(len(random_matrix)):
        for j in range(len(random_matrix[i])):
            count = 0
            if i == 0:
                sum_of_elements = random_matrix[i+1][j]
                count += 1
            elif i < len(random_matrix) -1:
                sum_of_elements = random_matrix[i-1][j] + random_matrix[i+1][j]
                count += 2
            else:
                sum_of_elements = random_matrix[i-1][j]
                count += 1
            
            if j == 0:
                sum_of_elements += random_matrix[i][j+1]
                count += 1
            elif j < len(random_matrix) -1:
                sum_of_elements += random_matrix[i][j-1] + random_matrix[i][j+1]
                count += 2
            else:
                sum_of_elements += random_matrix[i][j-1]
                count += 1
                
            averaged_matrix[i][j] = sum_of_elements/count #averagin each element with its neighbours
                
    return averaged_matrix

averaged_matrix = neigh_average(random_matrix)
print(averaged_matrix)


while averaged_matrix[0][0] != averaged_matrix[1][1]: #check whether convergance is achived!
    averaged_matrix = neigh_average(averaged_matrix)
    
    
print(averaged_matrix)           
    
# load the first array from file
B = np.loadtxt('random_matrix.csv', delimiter=',')
print(B)
# compute the difference between the first array and converged array
def dffer(random_matrix, averaged_matrix):
    difference = np.zeros((len(random_matrix), len(random_matrix[0])))
    for i in range(len(random_matrix)):
        for j in range(len(random_matrix[0])):
            difference[i][j] = abs(random_matrix[i][j] - averaged_matrix[i][j])
    return difference
differ = dffer(random_matrix, averaged_matrix)
# plot the converged array
plt.plot(np.arange(1, len(random_matrix[0])+1), random_matrix[0], 'r--')
plt.plot(np.arange(1, len(random_matrix[0])+1), averaged_matrix[0], '--')
plt.plot(np.arange(1, len(random_matrix[0])+1), differ[0])
plt.show()