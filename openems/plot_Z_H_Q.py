import matplotlib.pyplot as plt
import numpy as np
import openEMS

# freq = np.arange(0, 18e9, 1e7)
freq     = np.arange(0e9, 100e9, 1e5)

folder = 'sim'

U = openEMS.ports.UI_data( 'vt_0', folder, freq );
I = openEMS.ports.UI_data( 'it_1', folder, freq );

print('U', U.ui_val)
print('I', I.ui_val)

print('len(U.ui_val)', len(U.ui_val[0]))
print('len(U.ui_time)', len(U.ui_time[0]))
print('len(U.ui_f_val)', len(U.ui_f_val[0]))
print('len(I.ui_f_val)', len(I.ui_f_val[0]))
print('len(freq)', len(freq))

Z = [U.ui_f_val[0][_] / I.ui_f_val[0][_] for _ in range(len(U.ui_f_val[0]))];

# print(Z)

# L = imag(Z) ./ (2*pi*freq);
# L = reshape( L, 1, [] ); % row vector

# plt.subplot(3,1,1)
# plt.plot(U.ui_time[0], U.ui_val[0])
# plt.subplot(3,1,2)
# plt.plot(I.ui_time[0], I.ui_val[0])
# plt.subplot(3,1,3)
# plt.plot(I.ui_time[0], [U.ui_val[0][_]/I.ui_val[0][_] for _ in range(len(U.ui_val[0]))])
# plt.show()


# # plt.plot(t,r)
# plt.semilogx(freq, [abs(_) for _ in U.ui_f_val[0]])
# plt.semilogx(freq, [20*np.log10(abs(_)) for _ in U.ui_f_val[0]])
# plt.semilogx(freq, [20*np.log10(abs(_)) for _ in I.ui_f_val[0]])

plt.subplot(3,1,1)
plt.semilogx(freq, [abs(Z[_]) for _ in range(len(Z))])
plt.xlim([1e9, 40e9])
# plt.xlim([1e9, 12e9])
plt.title('Impedance')
plt.grid()

plt.subplot(3,1,2)
plt.semilogx(freq, [abs(Z[_])/(2*np.pi*freq[_]) for _ in range(len(Z))])
plt.xlim([1e9, 40e9])
plt.title('Inductance')
plt.grid()

plt.subplot(3,1,3)
plt.semilogx(freq, [abs(Z[_])/abs(Z[0]) for _ in range(len(Z))])
plt.xlim([1e9, 40e9])
plt.title('Q')
plt.grid()

print('DC resistance = %f' % abs(Z[0]))

plt.show()