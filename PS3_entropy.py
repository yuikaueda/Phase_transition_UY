#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:15:30 2024

@author: ueda
"""
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import ScalarFormatter

n = 10
a = 20
kb = 1.38e-23
T = 309.5
n_values = [5, 10, 15]


def S(x, n):
    return kb * ((a+1-n*x)*math.log(a+1-n*x) - (n-n*x)*math.log(n-n*x) - (a-n)*math.log(a-n))


x_values = np.linspace(0.01, 0.99, 100)

fig, ax = plt.subplots()

for n in n_values:
    S_values = [S(x, n) for x in x_values]
    plt.plot(x_values, S_values, label=f'$n_3 = {n}$')

ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.xlabel(r"$x_3$", fontsize=19)
plt.ylabel(r"$S_3$", fontsize=19)
plt.legend()

fig.set_dpi(300)  
plt.savefig('PS3_entropy.png', bbox_inches="tight", pad_inches=0.05, dpi=300)  
plt.show()