#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:58:52 2020

@author: mojtaba
"""

from mpi4py import MPI
import numpy as np


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

size_of_array = 100000
if rank == 0:
    group_of_arr = np.empty((size, size_of_array), dtype='i')
    group_of_arr.T[:,:] = range(size)
 
else:
    group_of_arr = None

print(rank, group_of_arr)

our_array = np.empty(size_of_array, dtype='i')

# distributing data to all ranks
comm.Scatter(group_of_arr, our_array, root=0)

#defining buffers
nest_arr = np.empty(size_of_array, dtype='i')
prev_arr = np.empty(size_of_array, dtype='i')

if rank == 0:
    
    comm.Sendrecv(our_array, dest=1, sendtag=1, recvbuf=nest_arr, source=1, recvtag=0)
    ave_arr = (our_array + nest_arr)/2
       
    
elif rank < size -1:
    comm.Sendrecv(our_array, dest=rank+1, sendtag=rank+1, recvbuf=nest_arr, source=rank+1, recvtag=rank)
    comm.Sendrecv(our_array, dest=rank-1, sendtag=rank-1, recvbuf=prev_arr, source=rank-1, recvtag=rank)
    ave_arr = (our_array + prev_arr + nest_arr)/3
    
else:
    comm.Sendrecv(our_array, dest=size-2, sendtag=rank-1, recvbuf=prev_arr, source=size-2, recvtag=rank)
    ave_arr = (our_array + prev_arr)/2

print(rank, ave_arr)   
average = np.zeros(size_of_array, dtype=float) 
comm.Reduce(ave_arr, average, op=MPI.SUM, root=0)
gather = np.zeros((size,size_of_array), dtype=float)
comm.Gather(ave_arr, gather, root=0)
# broadcats average to all ranks
if rank ==0:
    print(rank,average, gather)
#average = comm.bcast(average, root=0)


#print(rank, average)
    #ave_average = sum(average)/len(average)
    #print(ave_average)
    

 

