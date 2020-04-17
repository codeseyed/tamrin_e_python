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

# generating an array in process 0 then send it to process 1 for modification
if rank == 0:
    array = np.arange(1, 10, step=1, dtype=np.int)
    comm.send(array, dest=1, tag=1)
    
elif rank == 1:
    array = comm.recv(source=0, tag=1)
    array = [i*(rank+1) for i in array]
    
    
    
print(rank, array)

        
        

