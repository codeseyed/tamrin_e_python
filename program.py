#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 19:11:54 2020

@author: gongotar
"""
import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#rnd.seed(1)

def randomarray(n,m):
    h= 1
    vector = np.arange(m*n, step=h, dtype=np.int)
    random_matrix = np.reshape(vector, (n,m))
    return random_matrix

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
n = 50
m = 50
random_matrix = randomarray(n, m)

# store it in file
np.savetxt('random_matrix.csv', random_matrix, delimiter=',', fmt='%d')

# compute average of each cell with its neighbours until converge
matrix_prev = random_matrix
matrix_next = neigh_average(matrix_prev)
differ = dffer(matrix_prev, matrix_next)
while sum(sum(differ)) > m*n: #check whether convergance is achieved!
    matrix_prev = matrix_next
    matrix_next = neigh_average(matrix_prev)
    differ = dffer(matrix_prev, matrix_next)
print(sum(sum(differ)))
 
print(matrix_next)           
    
# load the first array from file
B = np.loadtxt('random_matrix.csv', delimiter=',')

# compute the difference between the first array and converged array

#differ = random_matrix - averaged_matrix
#differ = dffer(random_matrix, matrix_next)

# plot the converged array
print(differ)
x = range(m)
y = range(n)
X, Y = np.meshgrid(x, y)


ax = plt.axes(projection='3d')
#ax.scatter(X, Y, differ)
ax.plot_surface(X, Y, differ)
ax.plot_surface(X, Y, matrix_prev)


ax.view_init(60,35)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
