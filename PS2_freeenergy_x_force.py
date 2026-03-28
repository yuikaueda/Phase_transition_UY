#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 11:58:08 2024

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
f_values = [1e-12, 1e-11, 1e-10]


def E(x, n, f):
    term1 = n*(1-x)/2*mu_0*math.exp(-f*(a-n*(1+x)/2)/f_0)
    term2 = n*(1+x)/2*mu_0*math.exp(-f*(a+n*(x-1)/2)/f_0)
    return term1 + term2

def S(x, n):
    return kb * n * (-(1 + x) / 2 *math.log((1 + x) / 2) - (1-x) / 2 * math.log((1-x) / 2))

def A(x, n, f):
    return E(x, n, f) - T * S(x, n)

x_values = np.linspace(-0.99, 0.99, 100)

fig, ax = plt.subplots()

for f in f_values:
    A_values = [A(x, n, f) for x in x_values]
    exponent = int(np.log10(f))
    mantissa = f / 10**exponent
    label_text = f'$f_2 = {mantissa:.1f} \\times 10^{{{exponent}}}$'
    ax.plot(x_values, A_values, label=label_text)
    
ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.xlabel(r'$x_2$', fontsize=19)
plt.ylabel(r'$A_2$', fontsize=19)
plt.legend()

fig.set_dpi(300)  
plt.savefig('PS2_freeenergy_v2.png', bbox_inches="tight", pad_inches=0.05, dpi=300)  # 保存の解像度を上げる
plt.show()

