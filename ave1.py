#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 18:17:26 2020

@author: mojtaba
"""
from ave import convrg, big_matrix
from random import choice

thresh = 1        
while thresh > 0.0000001:
    big_matrix = convrg(big_matrix)
    inices = []
    for i in range(len(big_matrix)):
        for j in range(len(big_matrix[0])):
            inices.append((i,j))
            
    random_index1 = choice(inices)
    c = big_matrix[random_index1[0]][random_index1[1]]
    inices.remove(random_index1)
    
    random_index2 = choice(inices)
    d = big_matrix[random_index2[0]][random_index2[1]]
    
    thresh = abs(c-d)
    
print(big_matrix)