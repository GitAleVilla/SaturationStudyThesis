import h5py
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

SAMPLING = 0.1
BIN_NUMBER = 500
PE_NUMBER = 1

#f25um = h5py.File(str(PE_NUMBER) + 'pepe_peak_10k_50ns_25um_NoNoise.h5','r')
#f15um = h5py.File(str(PE_NUMBER) + 'pepe_peak_10k_50ns_15um_NoNoise.h5','r')
#f10um = h5py.File(str(PE_NUMBER) + 'pepe_peak_10k_50ns_10um_NoNoise.h5','r')
#f25um = h5py.File(str(PE_NUMBER) + 'pe_peak_10k_50ns_25um.h5','r')
#f15um = h5py.File(str(PE_NUMBER) + 'pe_peak_10k_50ns_15um.h5','r')
#f10um = h5py.File(str(PE_NUMBER) + 'pe_peak_10k_50ns_10um.h5','r')
f25um = h5py.File('E40GeV_50ns_25um.h5','r')
f10um = h5py.File('E40GeV_50ns_10um.h5','r')

events25um = np.array(f25um.get('Geometry')[:,0])
#events15um = np.array(f15um.get('Geometry')[:,0])
events10um = np.array(f10um.get('Geometry')[:,0])

integral25um = np.array([])
integral15um = np.array([])
integral10um = np.array([])
'''
for fib in range(events25um.size):
	wave = np.array(f25um.get('Waveforms')[fib])
	integral = np.sum(wave[50:3050]) * SAMPLING
	del wave
	integral25um = np.append(integral25um, integral)

for fib in range(events15um.size):
	wave = np.array(f15um.get('Waveforms')[fib])
	integral = np.sum(wave[50:3050]) * SAMPLING
	del wave
	integral15um = np.append(integral15um, integral)

for fib in range(events10um.size):
	wave = np.array(f10um.get('Waveforms')[fib])
	integral = np.sum(wave[50:3050]) * SAMPLING
	del wave
	integral10um = np.append(integral10um, integral)

print('Shapes finali')
print(integral25um.shape)
#print(integral15um.shape)
print(integral10um.shape)

#(mu25, sigma25) = norm.fit(integral25um)
#(mu15, sigma15) = norm.fit(integral15um)
#(mu10, sigma10) = norm.fit(integral10um)
#print('Gaussiana 25 um: mu ' + str(mu25) + '; sigma ' + str(sigma25))
#print('Gaussiana 15 um: mu ' + str(mu15) + '; sigma ' + str(sigma15))
#print('Gaussiana 10 um: mu ' + str(mu10) + '; sigma ' + str(sigma10))

#print('Media 10 micron per pe: ' + str(np.mean(integral10um) / PE_NUMBER))
#print('Media 15 micron per pe: ' + str(np.mean(integral15um) / PE_NUMBER))
#print('Media 25 micron per pe: ' + str(np.mean(integral25um) / PE_NUMBER))

plt.figure()
x25, hist25, patch25 = plt.hist(integral25um,
								bins=BIN_NUMBER,
								label='25 um',
								histtype = 'step',
								density=True)
x15, hist15, patch15 = plt.hist(integral15um,
								bins=BIN_NUMBER,
								label='15 um',
								histtype = 'step',
								density=True)
x10, hist10, patch10 = plt.hist(integral10um,
								bins=BIN_NUMBER,
								label='10 um',
								histtype = 'step',
								density=True)

'''
integral25umb = np.array(f25um.get('Features')[:,1])
print(integral25umb.shape)
print(np.mean(integral25umb))

x25b, hist25b, patch25b = plt.hist(integral25umb,
								   bins=BIN_NUMBER,
								   range = (0,500),
								   label='25 um - b',
								   histtype = 'step')

integral10umb = np.array(f10um.get('Features')[:,1])
print(integral10umb.shape)
print(np.mean(integral10umb))

x10b, hist10b, patch10b = plt.hist(integral10umb,
								   bins=BIN_NUMBER,
								   range = (0,500),
								   label='10 um - b',
								   histtype = 'step')


plt.xlabel('Integral (A.U.)')
plt.ylabel('Counts')

plt.legend()
plt.show()
