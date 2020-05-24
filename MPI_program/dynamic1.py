#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 20:50:06 2020

@author: mojtaba
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  7 19:53:03 2020

@author: mojtaba
"""

from mpi4py import MPI
import numpy as np


def get_prev_row(rows, rank, i, prev_rank_row):
    if rank == 0 and i == 0:
        prev_rank_row = np.zeros(len(nest_row), dtype=float)
    elif i == 0:
        prev_rank_row = prev_row
    else:
        prev_rank_row = rows[i-1]
    return prev_rank_row
            
  

def get_next_row(rows, rank, i, next_rank_row):
    if (rank == size-1) and i == (len(rows) -1):
        next_rank_row = np.zeros(len(prev_row), dtype=float)
    elif i == (len(rows - 1)):
        next_rank_row = nest_row
    else:
        next_rank_row = rows[i+1]
    return next_rank_row
  

def get_index_count(i,j,rank, rows, array):

    if rank == 0:
        if i == 0:
            if j == 0 or j == len(rows)-1:
                count = 3
            else:
                count = 4
            
        else:
            if j == 0 or j == len(rows)-1:
                count = 4
            else:
                count = 5
    elif rank == size -1:
        if i == len(array)-1:
            if j == 0 or j == len(rows)-1:
                count = 3
            else:
                count = 4
        else:
            if j == 0 or j == len(rows)-1:
                count = 4
            else:
                count = 5
    else:
        if j == 0 or j == len(rows)-1:
                count = 4
        else:
                count = 5
    return count
        
        
 
  


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# defining size of the 2D array
m = 8
n = 8


if rank == 0:
    def fibo_array(tul):
        fibo_array = np.zeros(tul, dtype=float)
        fibo_array[0] = fibo_array[1] =1
    
        for i in range(len(fibo_array)-2):
            fibo_array[i+2] = fibo_array[i] + fibo_array[i+1]
        return fibo_array    


    def generatearray(n,m):
    
        initial_matrix = np.zeros((m,n), dtype=float)
        initial_matrix[:,0] = fibo_array(m)
        initial_matrix[0,:] = fibo_array(n)
    
        for i in range(1,len(initial_matrix)):
            for j in range(1,len(initial_matrix[i])):
                initial_matrix[i][j] = initial_matrix[i-1][j] + initial_matrix[i][j-1] + initial_matrix[i-1][j-1]
               
        return initial_matrix
    inital_matrix = generatearray(m,n)
    
    inital_matrix = np.reshape(inital_matrix, (size,int(m*n/size)))
    
     
else:
    inital_matrix = None
   


# Buffers
row_values = np.empty(int(m*n/size), dtype=float)
nest_row = np.zeros(n, dtype=float)
prev_row = np.zeros(n, dtype=float)

 
# scattering among ranks
comm.Scatter(inital_matrix, row_values, root=0)


thres = 0.1
diff = 2.0
while diff > thres:

# communications
    if rank ==0:
        comm.Sendrecv(row_values[-n:], dest=rank+1, sendtag=rank, recvbuf=nest_row, source=rank+1, recvtag=rank+1)
        
    elif rank < size-1:
        comm.Sendrecv(row_values[-n:], dest=rank+1, sendtag=rank, recvbuf = nest_row, source=rank+1, recvtag=rank+1)
        comm.Sendrecv(row_values[:n], dest=rank-1, sendtag=rank, recvbuf=prev_row, source=rank-1, recvtag=rank-1)
        
    else:
        comm.Sendrecv(row_values[:n], dest=rank-1, sendtag=rank, recvbuf=prev_row, source=rank-1, recvtag=rank-1)

 
# computations
    reshape = np.reshape(row_values, (int(len(row_values)/n), n))
    avgelements = np.zeros((len(reshape), len(reshape[0])), dtype=float)
    for i in range(len(reshape)):
      
        nrow = get_next_row(reshape, rank, i, nest_row)
        prow = get_prev_row(reshape, rank, i, prev_row)        

        rsumelements = reshape[i]+nrow+prow
        
        zero = np.zeros(1, dtype=float)
        sumelements = rsumelements + np.concatenate((reshape[i][1:], zero), axis=None) + np.concatenate((zero, reshape[i][:-1]), axis=None)
        
        for j in range(len(sumelements)):
            indexcount = get_index_count(i,j,rank, sumelements, reshape)
            avgelements[i,j] = sumelements[j]/indexcount
      
    diff_array = abs(reshape - avgelements)
    diff_value = sum(sum(diff_array))
    diff = comm.allreduce(diff_value, op=MPI.SUM)
    
    new_values = np.reshape(avgelements, len(row_values))
    
    row_values = new_values
    
if rank == 0:
    averaged_matrix = np.zeros((size,int(m*n/size)), dtype=float)
else:
    averaged_matrix = None

comm.Gather(new_values, averaged_matrix, root=0)
    
# reshaping final matrix in rank =0
if rank ==0:
    
    averaged_matrix = np.reshape(averaged_matrix, (m,n))
    
    print('our initial matrix was:''\n',inital_matrix,'\n'
          'our final averaged matrix is:''\n',averaged_matrix)




    


            
            
        
    
        
        
        
        
    
    
    
    
    
    
    
    
    
