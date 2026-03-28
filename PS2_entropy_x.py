#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:21:08 2024

@author: ueda
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import ScalarFormatter

mu_0 = 1e-19
n = 100
a = 20
A = a * a
kb = 1.38e-23
T = 309.5
n_values = [5, 10, 20, 30]


def S(x, n):
    return kb * n * (-(1 + x) / 2 *math.log((1 + x) / 2) - (1-x) / 2 * math.log((1-x) / 2))


x_values = np.linspace(-0.99, 0.99, 100)

fig, ax = plt.subplots()

for n in n_values:
    S_values = [S(x, n) for x in x_values]
    plt.plot(x_values, S_values, label=f'$n_2 = {n}$')

#S_values = [S(x, n) for x in x_values]
#plt.plot(x_values, S_values, color='black')

ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.xlabel(r"$x_2$", fontsize=19)
plt.ylabel(r"$S_2$", fontsize=19)
plt.legend()

fig.set_dpi(300)  
plt.savefig('PS2_entropy_v2.png', bbox_inches="tight", pad_inches=0.05, dpi=300)  
plt.show()