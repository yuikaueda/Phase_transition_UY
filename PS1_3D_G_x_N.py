import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import ScalarFormatter

mu_0 = 1e-20
#Na = 100
a = 20
A = a * a
kb = 1.38e-23
T = 309.5
F = 1e-12

B = 1.5e-20
C = 2.5e+12
mu_s = lambda F: B * math.exp(-C * F)

def E(x, Na):
    return mu_0 * (Na - x * Na) + mu_s(F) * x * Na

def S(x, A, Na):
    term1 = (A-Na*x) * math.log(A)
    term2 = Na * (1 - x) * math.log(Na * (1 - x))
    term3 = (A - Na) * math.log(A - Na)
    term4 = 4 * a * math.log(a) + 2 * a * math.log(2)
    term5 = Na * x / a * math.log(Na * x)
    term6 = (2 * a - Na * x / a) * math.log(2 * A - Na * x)
    return kb * (term1 - term2 - term3 + term4 - term5 - term6)

def G(x, F, A, Na):
    return E(x, Na) - T * S(x, A, Na)

Na_values = np.linspace(10, 150, 100)

x_values = np.linspace(0.01, 0.99, 100)

G_matrix = np.zeros((len(Na_values), len(x_values)))

for i, Na in enumerate(Na_values):
    for j, x in enumerate(x_values):
        G_matrix[i][j] = G(x, F, A, Na)

plt.figure(figsize=(18, 12))
fig, ax = plt.subplots()

contour = plt.contourf(x_values, Na_values, G_matrix, levels=20, cmap='RdBu_r')

ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'

plt.xlabel(r'$x_1$', fontsize=19)
plt.ylabel(r'$N_{a}$', fontsize=19)

colorbar = plt.colorbar(contour)
colorbar.set_label(r'$A_1$', fontsize=19)
colorbar.ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.savefig('PS1_col_3D_A_N_x_F1e-12.png', bbox_inches="tight", pad_inches=0.05, dpi=1200)
plt.show()