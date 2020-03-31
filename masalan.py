#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:46:08 2020

@author: mojtaba
"""

import numpy as np

B = np.arange(0,10)
print(B)

np.savetxt('B.csv', B, delimiter=',', header='Please count these numbers!')