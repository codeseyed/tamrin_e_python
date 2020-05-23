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

averaged_matrix = np.zeros((size,int(m*n/size)), dtype=float)
num = np.full(size+1, 1, dtype='i')
num[0] = 0
num[size] = 0

    
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
    
  
        
    
    new_values = np.zeros(len(row_values), dtype=float)
    reshape = np.reshape(row_values, (int(len(row_values)/n), n))
    for i in range(len(reshape)):
        for j in range(len(reshape[i])):
            count = 1
            value = reshape[i][j]
            
            if i == 0:
                    value += reshape[i+1][j] + prev_row[j]*num[rank]
                    count += 1 + num[rank]*1
            elif i < len(reshape) -1:
                    value += reshape[i-1][j] + reshape[i+1][j]
                    count += 2
            else:
                    value += reshape[i-1][j] + nest_row[j]*num[rank+1]
                    count += 1 + num[rank+1]*1
    
        
            if j == 0:
                    value += reshape[i][j+1]
                    count +=1
            elif j < n-1:
                    value += reshape[i][j-1] + reshape[i][j+1]
                    count +=2
            else:
                    value += reshape[i][j-1]
                    count += 1
            new_values[n*i + j] = value/count
    
                
                
            
        
        
        
        
                
    
        
    
                

    
    
    diff_array = abs(row_values - new_values)
    diff_value = sum(diff_array)
    diff = comm.allreduce(diff_value, op=MPI.SUM)
    
    
   
    
    
    row_values = new_values
    
    
    
    
    



comm.Gather(new_values, averaged_matrix, root=0)
    

    





# reshaping final matrix in rank =0
if rank ==0:
    
    averaged_matrix = np.reshape(averaged_matrix, (m,n))
    
    print('our initial matrix was:''\n',inital_matrix,'\n'
          'our final averaged matrix is:''\n',averaged_matrix)




    


            
            
        
    
        
        
        
        
    
    
    
    
    
    
    
    
    
