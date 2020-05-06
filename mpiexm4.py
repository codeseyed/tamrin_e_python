#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 22:34:42 2020

@author: mojtaba
"""

from mpi4py import MPI
import numpy as np
from random import randint


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# generating a random number between 1 and a in rank = 0

if rank ==0:
    a = 3
    random_int = randint(1,a)
    print(random_int)
else:
    random_int = None

random_int = comm.bcast(random_int, root=0)

refer_array = np.repeat(np.arange(size, dtype='i'), random_int)

modified_int = [refer_array[rank]]

print(rank, modified_int)

# gather integers of each rank into a vector
group_int = comm.gather(modified_int, root=0)


# store it in a file
if rank ==0:
    np.savetxt('group.csv', group_int, delimiter=',', fmt='%d')
    