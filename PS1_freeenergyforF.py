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

E = lambda x: mu_0 * (Na - x * Na) + mu_s(F) * x * Na

def S(x, A, Na):
    term1 = (A-Na*x) * math.log(A)
    term2 = Na * (1 - x) * math.log(Na * (1 - x))
    term3 = (A - Na) * math.log(A - Na)
    term4 = 4 * a * math.log(a) + 2*a*math.log(2)
    term5 = Na * x / a * math.log(Na * x)
    term6 = (2 * a - Na * x / a) * math.log(2 * A - Na * x)
    return kb * (term1 - term2 - term3 + term4 - term5 - term6)

G = lambda x, F: E(x) - T * S(x, A, Na)


x_values = np.linspace(0.01, 0.99, 100)
for F in F_values:
    mu_s_value = mu_s(F)
    print(f"mu_s({F}) = {mu_s_value:.4e}")


fig, ax = plt.subplots()

for F in F_values:
    G_values = [G(x, F) for x in x_values]
    exponent = int(np.log10(F))
    mantissa = F / 10**exponent
    label_text = f'$F_1 = {mantissa:.1f} \\times 10^{{{exponent}}}$'
    ax.plot(x_values, G_values, label=label_text)

ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.xlabel(r'$x_1$', fontsize=19)
plt.ylabel(r'$A_1$', fontsize=19)
plt.legend()

fig.set_dpi(300)  
plt.savefig('PS1_freeenergy_v2.png', bbox_inches="tight", pad_inches=0.05, dpi=300)  # 保存の解像度を上げる
plt.show()



