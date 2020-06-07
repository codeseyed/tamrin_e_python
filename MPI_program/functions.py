#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 21:30:24 2020

@author: mojtaba
"""
import numpy as np



def get_up_row(reshape, rank, i, up_row, reshaped_col_num):
    if 0 <= rank < reshaped_col_num and i == 0:
        upper_row = np.zeros(len(up_row), dtype=float)
    elif i == 0:
        upper_row = up_row
    else:
        upper_row = reshape[i-1]
    return upper_row
            
  

def get_down_row(reshape, rank, i, down_row, reshaped_col_num, reshaped_row_num):
    if (reshaped_row_num -1)*reshaped_col_num <= rank <= (reshaped_row_num*reshaped_col_num -1) and i == (len(reshape) -1):
        downer_row = np.zeros(len(down_row), dtype=float)
    elif i == (len(reshape) - 1):
        downer_row = down_row
    else:
        downer_row = reshape[i+1]
    return downer_row

def get_right_value(sumelements, rank, j,i, right_row, reshaped_col_num):
    if (rank+1)%reshaped_col_num !=0 and j == (len(sumelements)-1):
        righter_value = right_row[i]
    else:
        righter_value = 0
    return righter_value

def get_lefter_value(sumelements, rank, j,i, left_row, reshaped_col_num):
    if (rank)%reshaped_col_num != 0 and j == 0:
        lefter_value = left_row[i]
    else:
        lefter_value = 0
    return lefter_value
  

def get_index_count(i,j,rank, sumelements, reshape, reshaped_col_num, reshaped_row_num):

    if rank == 0:
        if i == 0:
            if j == 0:
                count = 3
            elif reshaped_col_num ==1 and j == len(sumelements)-1:
                count = 3
            else:
                count = 4
        else:
            if j == 0:
                count = 4
            elif reshaped_col_num ==1 and j == len(sumelements)-1:
                count = 4
            else:
                count = 5
    elif 0 <rank< reshaped_col_num -1:
        if i == 0:
            count = 4
        else:
            count = 5
    elif rank == reshaped_col_num -1:
        if i == 0:
            if j == len(sumelements)-1:
                count = 3
            else:
                count = 4
        else:
            if j == len(sumelements)-1:
                count = 4
            else:
                count = 5
    elif rank == (reshaped_row_num -1)*reshaped_col_num:
        if j == 0:
            if i == len(reshape)-1:
                count = 3
            else:
                count = 4
        elif j == len(sumelements) -1 and reshaped_col_num == 1:
            if i == len(reshape)-1:
                count = 3
            else:
                count = 4
        else:
            if i == len(reshape)-1:
                count = 4
            else:
                count = 5
    elif rank == (reshaped_row_num*reshaped_col_num -1):
        if i == len(reshape)-1:
            if j == len(sumelements)-1:
                count = 3
            else:
                count = 4
        else:
            if j == len(sumelements)-1:
                count = 4
            else:
                count = 5
        
    elif rank % reshaped_col_num == 0:
        if j == 0:
            count = 4
        else:
            count = 5
    elif (rank+1) % reshaped_col_num == 0:
        if j == len(sumelements)-1:
            count = 4
        else:
            count = 5
    elif (reshaped_row_num -1)*reshaped_col_num <= rank <= (reshaped_row_num*reshaped_col_num -1):
        if i == len(reshape)-1:
            count = 4
        else:
            count = 5
    else:
        count = 5
    return count

def fibo_array(tul):
        fibo_array = np.zeros(tul, dtype=float)
        fibo_array[0] = fibo_array[1] =1
    
        for i in range(len(fibo_array)-2):
            fibo_array[i+2] = fibo_array[i] + fibo_array[i+1]
        return fibo_array    


def generatearray(m,n):
    
        initial_matrix = np.zeros((m,n), dtype=float)
        initial_matrix[:,0] = fibo_array(m)
        initial_matrix[0,:] = fibo_array(n)
    
        for i in range(1,len(initial_matrix)):
            for j in range(1,len(initial_matrix[i])):
                initial_matrix[i][j] = initial_matrix[i-1][j] + initial_matrix[i][j-1] + initial_matrix[i-1][j-1]
               
        return initial_matrix
    # m is the number of rows in our data matrix
    # n is the number og columns in our data matrix
def divisor_finder(number):
        numbers = []
        numbr = []
        i = 1
        while i <= np.sqrt(number):
            if number % i == 0:
                if number/i != i:
                    numbers.append(i)
                    numbr.append(int(number/i))
                else:
                    numbers.append(i)
            i +=1
    
        return numbers + numbr[::-1]
        
     
def comm_num(m,n, size):
        array_size = m*n
        size_rank = array_size/size
        mrange = divisor_finder(m)
        nrange = divisor_finder(n)
        num = []
        for i in mrange:
            for j in nrange:
                if i*j == size_rank:
                    num.append((i,j))
        return num
    
def comm_counter(m,n, num):
        for i in num:
            count = (int(m/i[0]) -1)*2*n + (int(n/i[1]) -1)*2*m 
            
            yield count
    
        
def forming_init_matrix(inital_matrix, optimum_shape, m, n):
        rows = []
        row_index = [i for i in range(0,m + optimum_shape[0], optimum_shape[0])]
        col_index = [i for i in range(0,n + optimum_shape[1], optimum_shape[1])]
        for i in range(len(row_index)-1):
            for j in range(len(col_index)-1):
                for k in range(row_index[i], row_index[i+1]):
                    for l in range(col_index[j], col_index[j+1]):
                        rows.append(inital_matrix[k][l])
        return rows
            
def split_init_matrix(inital_matrix, optimum_shape, m, n, size):
    row_split = np.split(inital_matrix, int(m/optimum_shape[0]), axis=0)
    for i in range(len(row_split)):
        row_split[i] = np.split(row_split[i], int(n/optimum_shape[1]), axis=1)
    rows = np.reshape(row_split, (size,int(m*n/size)))
    return rows

def forming_final_matrix(gathered, inital_matrix, optimum_shape, m, n, reshaped_col_num):
    inital_matrix = np.zeros((m,n), dtype=float)
    row_index = [i for i in range(0,m + optimum_shape[0], optimum_shape[0])]
    col_index = [i for i in range(0,n + optimum_shape[1], optimum_shape[1])]
    for i in range(len(row_index)-1):
        for j in range(len(col_index)-1):
            inital_matrix[row_index[i]:row_index[i+1],col_index[j]:col_index[j+1]] = gathered[reshaped_col_num*i + j]
    return inital_matrix
    



