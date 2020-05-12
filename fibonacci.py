#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 19:53:03 2020

@author: mojtaba
"""

from mpi4py import MPI
import numpy as np


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# defining size of the 2D array
m = 8
n = 8


if rank == 0:
    def fibo_array(tul):
        fibo_array = np.zeros(tul, dtype='i')
        fibo_array[0] = fibo_array[1] =1
    
        for i in range(len(fibo_array)-2):
            fibo_array[i+2] = fibo_array[i] + fibo_array[i+1]
        return fibo_array    


    def generatearray(n,m):
    
        initial_matrix = np.zeros((m,n), dtype='i')
        initial_matrix[:,0] = fibo_array(m)
        initial_matrix[0,:] = fibo_array(n)
    
        for i in range(1,len(initial_matrix)):
            for j in range(1,len(initial_matrix[i])):
                initial_matrix[i][j] = initial_matrix[i-1][j] + initial_matrix[i][j-1] + initial_matrix[i-1][j-1]
               
        return initial_matrix
    inital_matrix = generatearray(m,n)
    
    # vectorizing the 2d array
    vector = np.reshape(inital_matrix, m*n)
     
else:
    vector = None

cell_value = comm.scatter(vector, root=0)



# define the neighbors
neighbors = [rank-1, rank+1, rank-n, rank+n]
neighbors = [nr for nr in neighbors if nr >= 0 and nr < m*n]



if rank % n == 0 and rank != 0:
    neighbors.remove(neighbors[0])
    
elif (rank+1) % n ==0 and rank != m*n-1:
    neighbors.remove(neighbors[1])
else:
    None
    
        
    

    
#print(rank, neighbors)
    
ndata = np.zeros(len(neighbors))

thres = 0.1
diff = 2.0

while (diff > thres):

  for i,nr in enumerate(neighbors):
    ndata[i] = comm.sendrecv(cell_value, dest=nr, sendtag=rank+nr, source=nr, recvtag=rank+nr)
  
  new_cell_value = (sum(ndata)+cell_value)/(len(ndata)+1)
  my_diff = abs(cell_value - new_cell_value)
  diff = comm.allreduce(my_diff, op = MPI.SUM)
  cell_value = new_cell_value

# collect them in a final array

final_array = comm.gather(new_cell_value, root=0)

# reshaping final matrix in rank =0
if rank ==0:
    averaged_matrix = np.reshape(final_array, (m,n))
    print('our initial matrix was:''\n',inital_matrix,'\n'
          'our final averaged matrix is:''\n',averaged_matrix)




    


            
            
        
    
        
        
        
        
    
    
    
    
    
    
    
    
    
