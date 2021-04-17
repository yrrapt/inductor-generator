import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
import parse


# values = loadmat('Zc.mat')
# values = np.loadtxt('Zc.mat')

# print(values)

freq = []
resistance = []
inductance = []
Q = []


input_file = "Zc.mat"

freq_line = parse.compile("Impedance matrix for frequency = {freq:g} {rows:d} x {cols:d}\n")
with open(input_file, "r") as f:
    for line in f:
        data = freq_line.parse(line)
        if data != None:
            freq.append(data['freq']/1e9)
            g = []
            for x in range(0, data['rows']):
                line = f.readline().replace('j', '').split()
                s = np.asarray(line, dtype=float)
                s = s[::2] + s[1::2] * 1j
                g.append(s)
            Z = np.stack(g)
            impedance = Z.sum()
            print(impedance)
            resistance.append(np.real(impedance))
            inductance.append(np.imag(impedance) / (2 * np.pi * data['freq']))
            Q.append(np.imag(impedance) / np.real(impedance))


# print(inductance)
# print(Q)

plt.subplot(3,1,1)
plt.semilogx(freq,resistance)
plt.grid(True, which="both")
plt.title('Resistance')

plt.subplot(3,1,2)
plt.semilogx(freq,inductance)
plt.grid(True, which="both")
plt.title('Inductance')

plt.subplot(3,1,3)
plt.semilogx(freq,Q)
plt.grid(True, which="both")
plt.title('Quality Factor')
plt.tight_layout()
plt.show()
