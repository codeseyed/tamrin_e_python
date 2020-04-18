#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 10:54:53 2020

@author: mojtaba
"""

from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def arraygen(array):
    return [i*(rank+5) for i in array] 

# generating an array in process 0 then send it to process 1 for modification
if rank == 0:
    array = np.arange(1, 10, step=1, dtype=np.int)
    array_new = arraygen(array)
    comm.send(array_new, dest=1, tag=1)
    array_newer = comm.recv(source=1, tag=2)
    
    
elif rank == 1:
    array_new = comm.recv(source=0, tag=1)
    array_newer = arraygen(array_new)
    comm.send(array_newer, dest=0, tag=2)
    
    
print(array_new, array_newer)  
#array = [i*(rank+5) for i in array]   
#print(rank, array, new)

        
        

