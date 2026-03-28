#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 12:43:22 2024

@author: ueda
"""
#%%
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


def E(x, n, f):
    term1 = n*(1-x)/2*mu_0*math.exp(-f*(a-n*(1+x)/2)/f_0)
    term2 = n*(1+x)/2*mu_0*math.exp(-f*(a+n*(x-1)/2)/f_0)
    return term1 + term2

def S(x, n):
    return kb * n * (-(1 + x) / 2 *math.log((1 + x) / 2) - (1-x) / 2 * math.log((1-x) / 2))

def A(x, n, f):
    return E(x, n, f) - T * S(x, n)

x_values = np.linspace(-0.99, 0.99, 100)
f_values = np.linspace(0, 5e-11, 100)


A_matrix = np.zeros((len(f_values), len(x_values)))


for i, f in enumerate(f_values):
    for j, x in enumerate(x_values):
        A_matrix[i][j] = A(x, n, f)


plt.figure(figsize=(18, 12))  
fig, ax = plt.subplots()

contour = plt.contourf(x_values, f_values, A_matrix, levels=20, cmap='RdBu_r')


ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'

plt.xlabel(r'$x_2$', fontsize=19)
plt.ylabel(r'$f_{2}$', fontsize=19)

colorbar = plt.colorbar(contour)
colorbar.set_label(r'$A_2$', fontsize=19)
colorbar.ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))


plt.savefig('PS2_col_3D_A_F_x.png', bbox_inches="tight", pad_inches=0.05, dpi=1200)
plt.show()

