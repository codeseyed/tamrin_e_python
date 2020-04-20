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

# generating an array between 1 to 10
array = np.arange(1, 10, step=1, dtype=np.int)

# modifying the array based on the rank
array_new = arraygen(array)
array_newer = arraygen(array)

# distributign the process
if rank == 0:
    comm.send(array, dest=1, tag=1)
    comm.send(array_new, dest=1, tag=3)
    array_newer = comm.recv(source=1, tag=2)
    
    
    
elif rank == 1:
    array = comm.recv(source=0, tag=1)
    array_new = comm.recv(source=0, tag=3) 
    comm.send(array_newer, dest=0, tag=2)

print(rank, array, array_new, array_newer)
  



        
        

