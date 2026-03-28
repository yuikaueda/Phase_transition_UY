#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 12:52:22 2024

@author: ueda
"""
#%%
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import ScalarFormatter

mu_0 = 1e-20
Na = 200
a = 20
A = a * a
kb = 1.38e-23
T = 309.5
F_values = [1e-14, 1e-13, 1e-12, 1e-11]

B = 1.5e-20  
C = 2.5e+12  
mu_s = lambda F: B * math.exp(-C * F)

# E(x)
E = lambda x, F: mu_0 * (Na - x * Na) + mu_s(F) * x * Na


# x
x_values = np.linspace(0.01, 0.99, 100)
for F in F_values:
    mu_s_value = mu_s(F)
    print(f"mu_s({F}) = {mu_s_value:.4e}")

fig, ax = plt.subplots()

for F in F_values:
    E_values = [E(x, F) for x in x_values]
    exponent = int(np.log10(F))
    mantissa = F / 10**exponent
    label_text = f'$F_1 = {mantissa:.1f} \\times 10^{{{exponent}}}$'
    ax.plot(x_values, E_values, label=label_text)

ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.xlabel(r'$x_1$', fontsize=19)
plt.ylabel(r'$E_1$', fontsize=19)
plt.legend()

fig.set_dpi(300)  
plt.savefig('PS1_energy_v2.png', bbox_inches="tight", pad_inches=0.05, dpi=300)  
plt.show()