#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 13:30:13 2024

@author: ueda
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import ScalarFormatter

mu_0 = 1e-19
#n = 100
a = 20
kb = 1.38e-23
T = 309.5

f_0 = 1e-9
f_values = np.linspace(0, 2e-11, 100)
n_values = [5, 10, 20, 30]  
#min_x_values = []

def E(x, n, f):
    term1 = n*(1-x)/2*mu_0*math.exp(-f*(a-n*(1+x)/2)/f_0)
    term2 = n*(1+x)/2*mu_0*math.exp(-f*(a+n*(x-1)/2)/f_0)
    return term1 + term2

def S(x, n):
    return kb * n * (-(1 + x) / 2 *math.log((1 + x) / 2) - (1-x) / 2 * math.log((1-x) / 2))

def A(x, n, f):
    return E(x, n, f) - T * S(x, n)

def min_x(f, n):
    x_values = np.linspace(0, 0.99, 1000)
    min_x = None
    min_A = float('inf')
    for x in x_values:
        current_A = A(x, n, f)
        if current_A < min_A:
            min_A = current_A
            min_x = x
    return min_x

min_x_values_all_n = []
for n in n_values:
    min_x_values = []  
    for f in f_values:
        min_x_values.append(min_x(f, n))
    min_x_values_all_n.append(min_x_values)

#1line
##for f in f_values:
##    min_x_values.append(min_x(f))

fig, ax = plt.subplots()

colors = ['red', 'blue', 'green', 'orange']
for i, n in enumerate(n_values):
    plt.plot(f_values, min_x_values_all_n[i], color=colors[i], label=f'$n_2$ = {n}') # nごとに色を変えてプロット

def min_xn(f, n):
    x_values = np.linspace(-0.99, 0, 1000)
    min_xn = None
    min_A = float('inf')
    for x in x_values:
        current_A = A(x, n, f)
        if current_A < min_A:
            min_A = current_A
            min_xn = x
    return min_xn

min_xn_values_all_n = []
for n in n_values:
    min_xn_values = []  
    for f in f_values:
        min_xn_values.append(min_xn(f, n))
    min_xn_values_all_n.append(min_xn_values)


colors = ['red', 'blue', 'green', 'orange']
for i, n in enumerate(n_values):
    plt.plot(f_values, min_xn_values_all_n[i], color=colors[i])    
    


ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.xlabel(r'$f_{2}$', fontsize=19)
plt.ylabel(r'$x^{*}_{2}$', fontsize=19)

fig.set_dpi(300)  
plt.legend()
plt.savefig('PS2_x0forN_suchi_v2.png', bbox_inches="tight", pad_inches=0.05, dpi=300)  # 保存の解像度を上げる
plt.show()