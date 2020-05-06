#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 22:34:42 2020

@author: mojtaba
"""

from mpi4py import MPI
import numpy as np
from random import randint
from math import floor


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

# modifiying the integer based on its rank
modified_int = [floor(rank/random_int)]
print('modified integer for rank:', rank, 'is equal to:', modified_int)

# saving the generated data in a file
np.savetxt('data_'+ str(rank)+ '.txt', modified_int, fmt='%d')    