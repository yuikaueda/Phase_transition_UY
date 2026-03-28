#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 19:02:04 2024

@author: ueda
"""
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import ScalarFormatter

mu_0 = 1e-19
#n = 10
a = 20
kb = 1.38e-23
T = 309.5

f_0 = 1e-9
f = 1e-10
c_values = np.linspace(0, 5, 10000)
n_values = [10]

def E(x, n, c):
    term1 = n*(1-x)*mu_0*math.exp(-f/f_0)
    term2 = n*x*mu_0*math.exp(-f*c/f_0)
    return term1 + term2

def S(x, n):
    return kb * ((a+1-n*x)*math.log(a+1-n*x) - (n-n*x)*math.log(n-n*x) - (a-n)*math.log(a-n))

def A(x, n, c):
    return E(x, n, c) - T * S(x, n)

def min_x(c, n):
    x_values = np.linspace(0, 0.99, 10000)
    min_x = None
    min_A = float('inf')
    for x in x_values:
        current_A = A(x, n, c)
        if current_A < min_A:
            min_A = current_A
            min_x = x
    return min_x

min_x_values_all_n = []
for n in n_values:
    min_x_values = []  
    for c in c_values:
        min_x_values.append(min_x(c, n))
    min_x_values_all_n.append(min_x_values)

fig, ax = plt.subplots()    
colors = ['black', 'blue', 'green', 'orange']
for i, n in enumerate(n_values):
    plt.plot(c_values, min_x_values_all_n[i], color=colors[i])  

ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.xlabel(r'$c_{ass}$', fontsize=19)
plt.ylabel(r'$x^{*}_{3}$', fontsize=19)

fig.set_dpi(300)  
plt.savefig('PS3_x0forc_suchi.png', bbox_inches="tight", pad_inches=0.05, dpi=300)  