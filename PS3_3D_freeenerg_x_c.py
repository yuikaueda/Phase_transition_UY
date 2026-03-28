#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 14:05:26 2024

@author: ueda
"""
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import ScalarFormatter

mu_0 = 1e-19
n = 10
a = 20
kb = 1.38e-23
T = 309.5

f_0 = 1e-9
f = 1e-10

def E(x, n, c):
    term1 = n*(1-x)*mu_0*math.exp(-f/f_0)
    term2 = n*x*mu_0*math.exp(-f*c/f_0)
    return term1 + term2

def S(x, n):
    return kb * ((a+1-n*x)*math.log(a+1-n*x) - (n-n*x)*math.log(n-n*x) - (a-n)*math.log(a-n))

def A(x, n, c):
    return E(x, n, c) - T * S(x, n)

x_values = np.linspace(0.01, 0.99, 100)
c_values = np.linspace(0, 5, 100)

A_matrix = np.zeros((len(c_values), len(x_values)))

for i, c in enumerate(c_values):
    for j, x in enumerate(x_values):
        A_matrix[i][j] = A(x, n, c)


plt.figure(figsize=(18, 12))  
fig, ax = plt.subplots()

contour = plt.contourf(x_values, c_values, A_matrix, levels=20, cmap='RdBu_r')

ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'

plt.xlabel(r'$x_3$', fontsize=19)
plt.ylabel(r'$c_{{ass}}$', fontsize=19)

colorbar = plt.colorbar(contour)
colorbar.set_label(r'$A_3$', fontsize=19)
colorbar.ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.savefig('PS3_col_3D_A_c_x.png', bbox_inches="tight", pad_inches=0.05, dpi=1200)
plt.show()