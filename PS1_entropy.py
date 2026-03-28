#%%
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
Na_values = [50, 100, 200]


def S(x, A, Na):
    term1 = (A-Na*x) * math.log(A)
    term2 = Na * (1 - x) * math.log(Na * (1 - x))
    term3 = (A - Na) * math.log(A - Na)
    term4 = 4 * a * math.log(a) + 2*a*math.log(2)
    term5 = Na * x / a * math.log(Na * x)
    term6 = (2 * a - Na * x / a) * math.log(2 * A - Na * x)
    return kb * (term1 - term2 - term3 + term4 - term5 - term6)


x_values = np.linspace(0.01, 0.99, 100)

fig, ax = plt.subplots()

for Na in Na_values:
    S_values = [S(x, A, Na) for x in x_values]
    plt.plot(x_values, S_values, label=f'$N_a = {Na}$')

ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.xlabel(r"$x_1$", fontsize=19)
plt.ylabel(r"$S_1$", fontsize=19)
plt.legend()

fig.set_dpi(300)  
plt.savefig('PS1_entropy_v2.png', bbox_inches="tight", pad_inches=0.05, dpi=300)  # 保存の解像度を上げる
plt.show()



