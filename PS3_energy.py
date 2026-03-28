#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:24:12 2024

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
c_values = [0.5, 1, 2]

def E(x, n, c):
    term1 = n*(1-x)*mu_0*math.exp(-f/f_0)
    term2 = n*x*mu_0*math.exp(-f*c/f_0)
    return term1 + term2


x_values = np.linspace(0.01, 0.99, 100)

fig, ax = plt.subplots()

for c in c_values:
    E_values = [E(x, n, c) for x in x_values]
    plt.plot(x_values, E_values, label=f'$c_{{ass}} = {c}$')

ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.xlabel(r'$x_3$', fontsize=19)
plt.ylabel(r'$E_3$', fontsize=19)
plt.legend()

fig.set_dpi(300)  
plt.savefig('PS3_energy.png', bbox_inches="tight", pad_inches=0.05, dpi=300)  
plt.show()
