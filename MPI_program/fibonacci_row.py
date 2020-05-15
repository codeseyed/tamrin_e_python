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
    
    
     
else:
    inital_matrix = None
    
# scattering among ranks
row_values = comm.scatter(inital_matrix, root=0)




thres = 0.1
diff = 2.0
while diff > thres:
    

# communications
    if rank == 0:
        nest_row = comm.sendrecv(row_values, dest=rank+1, sendtag=rank, source=rank+1, recvtag=rank+1)
        
        
    elif rank < m-1:
        pre_row = comm.sendrecv(row_values, dest=rank-1, sendtag=rank, source=rank-1, recvtag=rank-1)
        nest_row = comm.sendrecv(row_values, dest=rank+1, sendtag=rank, source=rank+1, recvtag=rank+1)
        
    else:
        pre_row = comm.sendrecv(row_values, dest=rank-1, sendtag=rank, source=rank-1, recvtag=rank-1)
        
        

    
# computations 
    new_row = np.zeros(len(row_values), dtype=float)

    for i in range(len(new_row)):
        if i ==0:
            num = row_values[i] + row_values[i+1] 
            count = 2
        elif i < len(new_row)-1:
            num = row_values[i-1] + row_values[i] + row_values[i+1]
            count = 3
        else:
            num = row_values[i] + row_values[i-1]
            count = 2
        new_row[i] = num/count   
    
    if rank == 0:
        final_row = (new_row + nest_row)/2
    elif rank < m-1:
        final_row = (new_row + nest_row + pre_row)/3
    else:
        final_row = (new_row + pre_row)/2
        
    

    
    diff_array = abs(final_row - row_values)
    diff_array = comm.allreduce(diff_array, op=MPI.SUM)
    diff = sum(diff_array)
    
    row_values = final_row
    



averaged_matrix = comm.gather(final_row, root=0)    

    





# reshaping final matrix in rank =0
if rank ==0:
    
    print('our initial matrix was:''\n',inital_matrix,'\n'
          'our final averaged matrix is:''\n',averaged_matrix)




    


            
            
        
    
        
        
        
        
    
    
    
    
    
    
    
    
    
