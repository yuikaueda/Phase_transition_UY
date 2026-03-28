#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 14:47:59 2024

@author: ueda
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import ScalarFormatter



mu_0 = 1e-19
#n = 100
n = 10
a = 20
A = a * a
kb = 1.38e-23
T = 309.5

f_0 = 1e-9
f_values = [1e-11, 5e-11, 10e-11, 50e-11]


def E(x, n, f):
    term1 = n*(1-x)/2*mu_0*math.exp(-f*(a-n*(1+x)/2)/f_0)
    term2 = n*(1+x)/2*mu_0*math.exp(-f*(a+n*(x-1)/2)/f_0)
    return term1 + term2


x_values = np.linspace(-0.99, 0.99, 100)

fig, ax = plt.subplots()

for f in f_values:
    E_values = [E(x, n, f) for x in x_values]
    exponent = int(np.log10(f))
    mantissa = f / 10**exponent
    label_text = f'$f_2 = {mantissa:.1f} \\times 10^{{{exponent}}}$'
    ax.plot(x_values, E_values, label=label_text)


ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.xlabel(r'$x_2$', fontsize=19)
plt.ylabel(r'$E_2$', fontsize=19)
plt.legend()

fig.set_dpi(300)  
plt.savefig('PS2_energy_v2.png', bbox_inches="tight", pad_inches=0.05, dpi=300)  
plt.show()