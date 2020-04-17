#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 19:11:54 2020

@author: gongotar
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time


def generatearray(n,m):
    h= 1
    vector = np.arange(m*n*h, step=h, dtype=np.float)
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

def dffer(init_matrix, averaged_matrix):
    difference = np.zeros(init_matrix.shape)
    for i in range(len(init_matrix)):
        for j in range(len(init_matrix[0])):
            difference[i][j] = abs(init_matrix[i][j] - averaged_matrix[i][j])
    return difference

# set a timer to measure the speed of the program
start_time = time.time()
# generate n * m 2D array with random numbers
n = 4
m = 4
init_matrix = generatearray(n, m)
print(init_matrix)

# store it in file
np.savetxt('init_matrix.csv', init_matrix, delimiter=',', fmt='%d')

# compute average of each cell with its neighbours until converge
matrix_prev = init_matrix
matrix_next = neigh_average(matrix_prev)
print(matrix_next)
differ = dffer(matrix_prev, matrix_next)
thresh = 0.01
while sum(sum(differ)) > thresh: #check whether convergance is achieved!

    matrix_prev = matrix_next
    matrix_next = neigh_average(matrix_prev)
    differ = dffer(matrix_prev, matrix_next)
    print(differ)
 
    print(matrix_next)           
    
# load the first array from file
B = np.loadtxt('random_matrix.csv', delimiter=',')

# compute the difference between the first array and converged array

#differ = random_matrix - averaged_matrix
#differ = dffer(random_matrix, matrix_next)

# plot the converged array
print(differ)
#differ = dffer(init_matrix, matrix_next)

x = range(m)
y = range(n)
X, Y = np.meshgrid(x, y)


ax = plt.axes(projection='3d')
#ax.scatter(X, Y, differ)
ax.plot_surface(X, Y, differ)
#ax.plot_surface(X, Y, init_matrix)


#ax.view_init(60,35)
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
# printing the time consumed by the program
print("--- %s seconds ---" % (time.time() - start_time))