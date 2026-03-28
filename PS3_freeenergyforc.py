#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %%
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
    term1 = n * (1 - x) * mu_0 * math.exp(-f / f_0)
    term2 = n * x * mu_0 * math.exp(-f * c / f_0)
    return term1 + term2

def S(x, n):
    return kb * ((a + 1 - n * x) * math.log(a + 1 - n * x) - (n - n * x) * math.log(n - n * x) - (a - n) * math.log(a - n))

def A(x, n, c):
    return E(x, n, c) - T * S(x, n)

x_values = np.linspace(0.01, 0.99, 100)

fig, ax = plt.subplots()

for c in c_values:
    A_values = [A(x, n, c) for x in x_values]
    label_text = f'$c_{{ass}} = {c:.1f}$'
    ax.plot(x_values, A_values, label=label_text)

ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.xlabel(r'$x_3$', fontsize=19)
plt.ylabel(r'$A_3$', fontsize=19)
plt.legend()

fig.set_dpi(300)  
plt.savefig('PS3_freeenergy_c.png', bbox_inches="tight", pad_inches=0.05, dpi=300)  
plt.show()
