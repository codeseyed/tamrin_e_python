#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 17:58:52 2020

@author: mojtaba
"""

from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


if rank == 0:
    our_integer = 100
    comm.send(our_integer, dest=1, tag=1)
    our_integer = comm.recv(source=size-1, tag=size+1)
elif rank < size -1:
    our_integer = comm.recv(source=rank-1, tag=rank)
    our_integer += rank
    comm.send(our_integer, dest=rank+1, tag=rank+1)
else:
    our_integer = comm.recv(source=size-2, tag=size-1)
    our_integer += rank
    comm.send(our_integer, dest=0, tag=size+1)
        
        
print(rank, our_integer)