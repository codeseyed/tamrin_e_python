#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 19:11:54 2020

@author: gongotar
"""
import numpy as np
import random as rnd
import matplotlib.pyplot as plt

#rnd.seed(1)

def randomarray(n,m):
    array = np.zeros((n,m))
    for i in range(len(array)):
        for j in range(len(array[i])):  
            array[i][j] = rnd.choice(np.arange(0,20, dtype=np.int)) #assignign random number between 0 to 10 to each of matrix elements 
    return array

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

def dffer(random_matrix, averaged_matrix):
    difference = np.zeros(random_matrix.shape)
    for i in range(len(random_matrix)):
        for j in range(len(random_matrix[0])):
            difference[i][j] = abs(random_matrix[i][j] - averaged_matrix[i][j])
    return difference


# generate n * m 2D array with random numbers
n = 8
m = 8
random_matrix = randomarray(n, m)

# store it in file
np.savetxt('random_matrix.csv', random_matrix, delimiter=',', fmt='%d')

# compute average of each cell with its neighbours until converge
matrix_prev = random_matrix
matrix_next = neigh_average(matrix_prev)
differ = dffer(matrix_prev, matrix_next)
while sum(sum(differ)) > n*m: #check whether convergance is achieved!
    matrix_prev = matrix_next
    matrix_next = neigh_average(matrix_prev)
    differ = dffer(matrix_prev, matrix_next)

    
print(matrix_next)           
    
# load the first array from file
B = np.loadtxt('random_matrix.csv', delimiter=',')

# compute the difference between the first array and converged array

#differ = random_matrix - averaged_matrix
#differ = dffer(random_matrix, matrix_next)

# plot the converged array
x = range(n)
y = range(m)
X, Y = np.meshgrid(x, y)
ax = plt.axes(projection='3d')

ax.plot_surface(X, Y, differ)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
