#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:46:08 2020

@author: mojtaba
"""
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

if rank==0:
    group = np.zeros((size, 8), dtype='i')
    for i in range(len(group)):
        for j in range(len(group[i])):
            group[i][j] = i+j
else:
    group = None

#scattering arrays among ranks  
array = np.empty(8, dtype='i')
comm.Scatter(group, array, root=0)

print(array)

# reduce and satter array among ranks
recvdata = np.zeros(2, dtype='i')
comm.Reduce_scatter_block(array, recvdata, op=MPI.SUM)
print(recvdata)


recvcounts = (1,2,3,2)
recvdata_new = np.zeros(recvcounts[rank], dtype='i')

comm.Reduce_scatter(array,recvdata_new, recvcounts, op=MPI.MAX)


# eventually a bunch of point-to-point comm
if rank == 0:
    recvbuff = comm.sendrecv(recvdata_new, dest=1, sendtag=0, source=1, recvtag=1)
   
elif rank ==1:
    recvbuff = comm.sendrecv(recvdata, dest=0, sendtag=1, source=0, recvtag=0)
    
else:
    recvbuff = None


print(rank, recvdata, recvdata_new, recvbuff)    



    
    
    
    
    






