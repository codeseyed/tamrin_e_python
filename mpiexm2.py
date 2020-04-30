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


if rank == 0:
    group_of_arr = np.empty((size, 10), dtype='i')
    group_of_arr.T[:,:] = range(size)
    
else:
    group_of_arr = None

print(rank, group_of_arr)

our_array = np.empty(10, dtype='i')

# distributing data to all ranks
comm.Scatter(group_of_arr, our_array, root=0)

if rank == 0:
    comm.Send(our_array, dest=1, tag=1)
    nest_arr = np.empty(10, dtype='i')
    comm.Recv(nest_arr, source=1, tag=0)
    ave_arr = (our_array + nest_arr)/2
       
    
elif rank < size -1:
    comm.Send(our_array, dest=rank+1, tag=rank+1)
    comm.Send(our_array, dest=rank-1, tag=rank-1)
    nest_arr = np.empty(10, dtype='i')
    prev_arr = np.empty(10, dtype='i')
    comm.Recv(prev_arr, source=rank-1, tag=rank)
    comm.Recv(nest_arr, source=rank+1, tag=rank)
    ave_arr = (our_array + prev_arr + nest_arr)/3
    
else:
    comm.Send(our_array, dest=size-2, tag=rank-1)
    prev_arr = np.empty(10, dtype='i')
    comm.Recv(prev_arr, source=size-2, tag=rank)
    ave_arr = (our_array + prev_arr)/2

print(rank, ave_arr)   
average = np.zeros(10, dtype=float) 
comm.Reduce(ave_arr, average, op=MPI.SUM, root=0)
gather = np.zeros((size,10), dtype=float)
comm.Gather(ave_arr, gather, root=0)
# broadcats average to all ranks
if rank ==0:
    print(rank,average, gather)
#average = comm.bcast(average, root=0)


#print(rank, average)
    #ave_average = sum(average)/len(average)
    #print(ave_average)
    

 

