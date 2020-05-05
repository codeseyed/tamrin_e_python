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

size_of_array = 10**6
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
    req0 = comm.Isend(our_array, dest=1, tag=1)
    req0.wait();

    req1 = comm.Irecv(nest_arr, source=1, tag=0)
    req1.wait()

    ave_arr = (our_array + nest_arr)/2
       
elif rank < size -1:
    req1 = comm.Isend(our_array, dest=rank-1, tag=rank-1)
    req2 = comm.Isend(our_array, dest=rank+1, tag=rank+1)
    req1.wait()
    req2.wait()

    req0 = comm.Irecv(prev_arr, source=rank-1, tag=rank)
    req3 = comm.Irecv(nest_arr, source=rank+1, tag=rank)
    req0.wait()
    req3.wait()
    
    ave_arr = (our_array + prev_arr + nest_arr)/3
    
else:
    req3 = comm.Isend(our_array, dest=size-2, tag=rank-1)
    req3.wait()

    req2 = comm.Irecv(prev_arr, source=size-2, tag=rank)
    req2.wait()

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
    

 

