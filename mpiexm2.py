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
    our_integer = np.cos(rank)
    comm.send(our_integer, dest=1, tag=1)
    nest_int = comm.recv(source=1, tag=0)
    ave_int = (our_integer + nest_int)/2

    
        
    
elif rank < size -1:
    our_integer = np.cos(rank)
    comm.send(our_integer, dest=rank+1, tag=rank+1)
    comm.send(our_integer, dest=rank-1, tag=rank-1)
    prev_int = comm.recv(source=rank-1, tag=rank)
    nest_int = comm.recv(source=rank+1, tag=rank)
    ave_int = (our_integer + prev_int + nest_int)/3
    
else:
    our_integer = np.cos(rank)
    comm.send(our_integer, dest=size-2, tag=rank-1)
    prev_int = comm.recv(source=size-2, tag=rank)
    ave_int = (our_integer + prev_int)/2
    
average = comm.gather(ave_int, root=0)
print(rank,average)

if rank == 0:
    print(average)
    ave_average = sum(average)/len(average)
    print(ave_average)
    

 

