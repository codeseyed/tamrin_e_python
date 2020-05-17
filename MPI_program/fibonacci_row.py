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


# defining neighbors
nbrs = [rank-1, rank+1]
nbrs = [i for i in nbrs if i >=0 and i < m]
rows = np.zeros((len(nbrs)+1, len(row_values)), dtype=float)



thres = 0.00001
diff = 2.0
while diff > thres:
    


    

# communications
    rows[0] = row_values
    
    for i,j in enumerate(nbrs):
        rows[i+1] = comm.sendrecv(row_values, dest=j, sendtag=rank+j, source=j, recvtag=rank+j)
    
        
        
   
        
        

    
# computations 
    new_row = np.zeros(len(row_values), dtype=float)
    if rank == 0 or rank == m-1:
        for i in range(len(new_row)):
            if i ==0:
                num = rows[0][i] + rows[0][i+1] + rows[1][i] 
                count = 3
            elif i < len(new_row)-1:
                num = rows[0][i-1] + rows[0][i] + rows[0][i+1] + rows[1][i]
                count = 4
            else:
                num = rows[0][i] + rows[0][i-1] + rows[1][i]
                count = 3
            new_row[i] = num/count   
    else:
        for i in range(len(new_row)):
            if i ==0:
                num = rows[0][i] + rows[0][i+1] + rows[1][i] + rows[2][i]
                count = 4
            elif i < len(new_row)-1:
                num = rows[0][i-1] + rows[0][i] + rows[0][i+1] + rows[1][i] + rows[2][i]
                count = 5
            else:
                num = rows[0][i] + rows[0][i-1] + rows[1][i] + rows[2][i]
                count = 4
            new_row[i] = num/count   
        

    
        
    

   
    diff_array = abs(new_row - row_values)
    
    diff_array = comm.allreduce(diff_array, op=MPI.SUM)
    diff = sum(diff_array)
    
    
    row_values = new_row
    



averaged_matrix = comm.gather(new_row, root=0)    

    





# reshaping final matrix in rank =0
if rank ==0:
    
    print('our initial matrix was:''\n',inital_matrix,'\n'
          'our final averaged matrix is:''\n',averaged_matrix)




    


            
            
        
    
        
        
        
        
    
    
    
    
    
    
    
    
    
