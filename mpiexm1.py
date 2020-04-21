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





# distributign the process
if rank == 0:
    data1 = np.arange(1, 10, step=1, dtype=np.int)
    comm.send(data1, dest=1, tag=1)
    data2_0 = arraygen(data1)
    comm.send(data2_0, dest=1, tag=2)
    data2_1 = comm.recv(source=1, tag=3)
    
    
    
    
elif rank == 1:
    data1 = comm.recv(source=0, tag=1)
    data2_1 = arraygen(data1)
    data2_0 = comm.recv(source=0, tag=2)
    comm.send(data2_1, dest=0, tag=3)

print(rank, data1, data2_0, data2_1)
  



        
        

