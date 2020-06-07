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
import functions as fun

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# defining size of the 2D array
m = 50
n = 20

if rank == 0:
                
    # generating a list contains the possible matrix shapes in each rank        
    num = fun.comm_num(m,n,size)
    # count the number of communication for each construction
    count = fun.comm_counter(m,n,num)
    count = list(count)

    for min_index in range(len(count)):
        if count[min_index] == min(count):
            optimum_shape = num[min_index]
            break
                    
    inital_matrix = fun.generatearray(m,n)
    print('our initial matrix was:''\n',inital_matrix,'\n')
    
    
    # reshape the array to make it ready for scattering
    inital_matrix = fun.split_init_matrix(inital_matrix, optimum_shape, m, n, size)
   
else:
    inital_matrix = None
    optimum_shape = None

optimum_shape = comm.bcast(optimum_shape, root=0)
# new dimension for matrix categorized by the number of ranks   
reshaped_row_num = int(m/optimum_shape[0])
reshaped_col_num = int(n/optimum_shape[1])

# Buffers
row_values = np.empty(int(m*n/size), dtype=float)
down_row = np.zeros(optimum_shape[1], dtype=float)
up_row = np.zeros(optimum_shape[1], dtype=float)
right_row = np.zeros(optimum_shape[0], dtype=float)
left_row = np.zeros(optimum_shape[0], dtype=float)
buffers = [left_row, right_row, up_row, down_row]
#gathered = np.zeros(reshaped_row_num*reshaped_col_num)

# defining the neighbors
neighbors = [rank-1, rank+1, rank-reshaped_col_num, rank+reshaped_col_num]

# scattering among ranks
comm.Scatter(inital_matrix, row_values, root=0)

thres = 0.1
diff = 2.0
while diff > thres:

# defining part of arrays in each rank that should be communicated and collect them in an array     
    right_side_arr = row_values[-1::-optimum_shape[1]]
    communicated_arrays = [np.array(row_values[0::optimum_shape[1]]), np.array(right_side_arr[::-1]) , np.array(row_values[:optimum_shape[1]]), np.array(row_values[-optimum_shape[1]:])]

# zipping each part of communicated arrays with buffers and assocated neighbors   
    ziped_array = zip(neighbors, buffers, communicated_arrays)

# removing the wrong neighbors and concomitant zipped array and buffer 
    ziped_array = [nr for nr in ziped_array if nr[0] >= 0 and nr[0] < reshaped_row_num*reshaped_col_num]

# adding the condition when we just have two ranks and/or columns are not splitted   
    if reshaped_col_num == 1:
        ziped_array.remove(ziped_array[0])

# removing the wrong neighbors and concomitant zipped array and buffer        
    elif rank % reshaped_col_num == 0 and rank != 0:
        ziped_array.remove(ziped_array[0])
    
    elif (rank+1) % reshaped_col_num ==0 and rank != reshaped_row_num*reshaped_col_num -1:
        ziped_array.remove(ziped_array[1])
    
# communications    
    for i,j,k in ziped_array:
        comm.Sendrecv(k, dest=i, sendtag=rank, recvbuf=j, source=i, recvtag=i)
 
# computations
    reshape = np.reshape(row_values, optimum_shape)
    
    avgelements = np.zeros((len(reshape), len(reshape[0])), dtype=float)
    for i in range(len(reshape)):
# defining upper and downer rows within each rank array     
        urow = fun.get_up_row(reshape, rank, i, up_row, reshaped_col_num)
        drow = fun.get_down_row(reshape, rank, i, down_row, reshaped_col_num, reshaped_row_num)
                 
# averaging the array assigned to each rank
        sumelements = reshape[i]+urow+drow
        sumelements[0:-1] = sumelements[0:-1]+reshape[i][1:]
        sumelements[1:]=sumelements[1:]+reshape[i][0:-1]
    
        for j in range(len(sumelements)):
            rval = fun.get_right_value(sumelements, rank, j,i, right_row, reshaped_col_num)
            lval = fun.get_lefter_value(sumelements, rank, j, i, left_row, reshaped_col_num)
            sumelements[j] = sumelements[j] + rval + lval
            indexcount = fun.get_index_count(i,j,rank, sumelements, reshape, reshaped_col_num, reshaped_row_num)
            avgelements[i,j] = sumelements[j]/indexcount

# defining the convergance criteia           
    diff_array = abs(reshape - avgelements)
    diff_value = sum(sum(diff_array))
    diff = comm.allreduce(diff_value, op=MPI.SUM)
    
    new_values = np.reshape(avgelements, len(row_values))
    row_values = new_values
    

# gathering converged sliced matrices from all ranks
gathered = comm.gather(avgelements, root=0)  
  
# reshaping final matrix in rank = 0
if rank ==0:
    inital_matrix = fun.forming_final_matrix(gathered, inital_matrix, optimum_shape, m, n, reshaped_col_num)
    print(#'our initial matrix was:''\n',inital_matrix,'\n'
          'our final averaged matrix is:''\n',inital_matrix)