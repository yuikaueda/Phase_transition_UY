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
B = 1.5e-20
C = 1.0e+12

def calculate_dG(F, x):
    mu_s = B * math.exp(-C * F)
    term1 = -mu_0 * Na + mu_s * Na
    term2 = -math.log(A - Na * x) + math.log(Na - Na*x) - 1 / a * math.log(Na*x) + 1 / a * math.log(2 * A - Na * x) 
    dG =  term1 - kb * T * Na * term2
    return dG

F_values = np.linspace(0, 1e-11, 500)
  
x_at_dG_zero = []
  
for F in F_values:
    x_values = np.linspace(0.001, 0.999, 100000)  # 0 < x < 1
    dG_values = [calculate_dG(F, x) for x in x_values]
    x_zero_dG = [x for x, dG in zip(x_values, dG_values) if abs(dG) < 1e-22]
    if x_zero_dG:
        x_at_dG_zero.append(x_zero_dG[0])
    else:
        x_at_dG_zero.append(0)

#kaiseki
def calculate_x0(F):
    mu_s = B * math.exp(-C * F)
    x0 = 1 - (A / Na) *math.exp((mu_s - mu_0) / (kb * T))
    x0 = max(0, x0)
    return x0

x0_values = [calculate_x0(F) for F in F_values]


fig, ax = plt.subplots()
plt.plot(F_values, x_at_dG_zero, color='black')
ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.xlabel(r'$F_{1}$', fontsize=19)
plt.ylabel(r'$x^{*}_{1}$', fontsize=19)

fig.set_dpi(300) 
plt.savefig('PS1_x0forF_suchi_v2.png', bbox_inches="tight", pad_inches=0.05, dpi=300)  # 保存の解像度を上げる
plt.show()




