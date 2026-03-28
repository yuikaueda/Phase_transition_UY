import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.ticker import ScalarFormatter

mu_0 = 1e-20
a = 20
A = a * a
kb = 1.38e-23
T = 309.5

B = 1.5e-20
C = 2.5e+12

def calculate_dG(F, x, Na):
    mu_s = B * math.exp(-C * F)
    term1 = -mu_0 * Na + mu_s * Na
    term2 = -math.log(A - Na * x) + math.log(Na - Na * x) - 1 / a * math.log(Na * x) + 1 / a * math.log(2 * A - Na * x)
    dG = term1 - kb * T * Na * term2
    return dG

Na_values = np.linspace(10, 150, 100)
F_values = np.linspace(0, 1e-11, 100)

F_values, Na_values = np.meshgrid(F_values, Na_values)
x_at_dG_zero_values = np.zeros_like(F_values)

for i in range(len(F_values)):
    for j in range(len(Na_values)):
        Na = Na_values[j, i]
        F = F_values[j, i]

        # x
        x_values = np.linspace(0.001, 0.999, 10000)  # 0 < x < 1
        dG_values = [calculate_dG(F, x, Na) for x in x_values]

        x_zero_dG = [x for x, dG in zip(x_values, dG_values) if abs(dG) < 1e-21]
        if x_zero_dG:
            x_at_dG_zero_values[j, i] = x_zero_dG[0]
        else:
            x_at_dG_zero_values[j, i] = 0

plt.figure(figsize=(18, 12))  
fig, ax = plt.subplots()

contour = plt.contourf(F_values, Na_values, x_at_dG_zero_values, levels=20, cmap='RdBu_r')

ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'

plt.xlabel(r'$F_1$', fontsize=19)
plt.ylabel(r'$N_{a}$', fontsize=19)

colorbar = plt.colorbar(contour)
colorbar.set_label(r'$x^*_1$', fontsize=19)
colorbar.ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.savefig('PS1_col_3D_x_Na_F.png', bbox_inches="tight", pad_inches=0.05, dpi=1200)
plt.show()

