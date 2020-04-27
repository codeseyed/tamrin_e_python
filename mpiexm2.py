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
    group_of_arr = []
    for i in range(size):
        samp_arr = np.full(10, i, dtype=int)
        group_of_arr.append(samp_arr)

# distributing data to all ranks
our_array = comm.scatter(group_of_arr, root=0)

if rank == 0:
    comm.send(our_array, dest=1, tag=1)
    nest_arr = comm.recv(source=1, tag=0)
    ave_arr = (our_array + nest_arr)/2
       
    
elif rank < size -1:
    comm.send(our_array, dest=rank+1, tag=rank+1)
    comm.send(our_array, dest=rank-1, tag=rank-1)
    prev_arr = comm.recv(source=rank-1, tag=rank)
    nest_arr = comm.recv(source=rank+1, tag=rank)
    ave_arr = (our_array + prev_arr + nest_arr)/3
    
else:
    comm.send(our_array, dest=size-2, tag=rank-1)
    prev_arr = comm.recv(source=size-2, tag=rank)
    ave_arr = (our_array + prev_arr)/2

print(rank, ave_arr)    
#average = comm.allgather(ave_arr)
#average = comm.gather(ave_arr, root=0)

#print(average)
    #ave_average = sum(average)/len(average)
    #print(ave_average)
    

 

