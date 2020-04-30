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

sendbuf = None
if rank == 0:
    sendbuf = [[1,2,3,4], [1,2,3,4],[1,2,3,4], [1,2,3,4]]
#recvbuf = np.empty(4, dtype='i')
recvbuf = comm.scatter(sendbuf, root=0)
print(rank, recvbuf)

