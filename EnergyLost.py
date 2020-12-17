import h5py
import numpy as np
import matplotlib
#matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

def True_Energy(x, cellsize):
	if cellsize == 25:
		m = 49.295
	elif cellsize == 15:
		m = 49.398
	elif cellsize == 10:
		m = 49.414
	else:
		print('Attention! Possible cellsize: 25, 15, 10')
	q = 0.
	return (m * x) + q

pedestal25um = 2.8175
pedestal15um = 2.5389
pedestal10um = 2.6296

######### Importing Data #########
#f25um = h5py.File('E40GeV_50ns_25um.h5','r')
#f15um = h5py.File('E40GeV_50ns_15um.h5','r')
f10um = h5py.File('E40GeV_50ns_10um.h5','r')
print('read h5')
'''
with open('/home/storage/TesiVilla/Data/Electron40GeV/preSiPM.txt','r') as f_true:
	lines = f_true.readlines()
for l in lines:
	line = l.split(' ')[6]
	true_pe = np.append(true_pe,line)'''
true_pe = np.loadtxt('/home/storage/TesiVilla/Data/Electron40GeV/preSiPM.txt',
					 delimiter = ' ',
					 usecols = (0,2,6))
print('read txt')
#event25um = np.array(f25um.get('Geometry')[:,0])
#event15um = np.array(f15um.get('Geometry')[:,0])
event10um = np.array(f10um.get('Geometry')[:,0])
#fib_type25um = np.array(f25um.get('Geometry')[:,1])
#fib_type15um = np.array(f15um.get('Geometry')[:,1])
fib_type10um = np.array(f10um.get('Geometry')[:,1])

#ev_list25um = np.unique(event25um)
#ev_list15um = np.unique(event15um)
ev_list10um = np.unique(event10um)

integral_scin = np.array([])
integral_cher = np.array([])
pe_scin = np.array([])
pe_cher = np.array([])
int_ideal_scin = np.array([])
int_ideal_cher = np.array([])

for ev in ev_list10um:
	print(ev)
	integrals_scin = np.array(f10um.get('Features')
								[(event10um == ev) & (fib_type10um == 1),1]
								 - pedestal10um)
	integrals_cher = np.array(f10um.get('Features')
								[(event10um == ev) & (fib_type10um == 0),1]
								 - pedestal10um)
	integral_scin = np.append(integral_scin, np.sum(integrals_scin))
	integral_cher = np.append(integral_cher, np.sum(integrals_cher))
	pe_number_scin = np.sum(true_pe[(true_pe[:,0] == ev) & (fib_type10um == 1),2])
	pe_number_cher = np.sum(true_pe[(true_pe[:,0] == ev) & (fib_type10um == 0),2])
	pe_scin = np.append(pe_scin, pe_number_scin)
	pe_cher = np.append(pe_cher, pe_number_cher)
	int_ideal_scin = np.append(int_ideal_scin, True_Energy(pe_number_scin, 10))
	int_ideal_cher = np.append(int_ideal_cher, True_Energy(pe_number_cher, 10))


print(integral_scin.size)
print(integral_cher.size)
print(pe_scin.size)
print(pe_cher.size)
print(int_ideal_scin.size)
print(int_ideal_cher.size)
'''
print(integral_scin)
print(integral_cher)
print(pe_scin)
print(pe_cher)
print(int_ideal_scin)
print(int_ideal_cher)'''

############################# Plot 

plt.figure()
plt1_scin = plt.plot(pe_scin, 
				integral_scin,
				'o',
				color = colors[0],
				markersize = 2,
				label = 'Scintillating integral')

plt2_scin = plt.plot(pe_scin, 
				int_ideal_scin,
				'o',
				color = colors[1],
				markersize = 2,
				label = 'Scintillating ideal integral')

plt.xlabel('Photoelectrons')
plt.ylabel('Integral (A.U.)')
plt.title('Schintillating Integral')
plt.legend()

plt.figure()
plt1_cher = plt.plot(pe_cher, 
				integral_cher,
				'o',
				color = colors[0],
				markersize = 2,
				label = 'Cherenkov integral')

plt2_cher = plt.plot(pe_cher, 
				int_ideal_cher,
				'o',
				color = colors[1],
				markersize = 2,
				label = 'Cherenkov ideal integral')

plt.xlabel('Photoelectrons')
plt.ylabel('Integral (A.U.)')
plt.title('Cherenkov Integral')
plt.legend()

plt.figure()
BIN_NUMBER = 70

loss_ratio_cher = (int_ideal_cher - integral_cher) / int_ideal_cher
hist_cher = plt.hist(loss_ratio_cher,
					bins = BIN_NUMBER,
					range = (0,0.07),
					#density = True,
					weights = np.ones_like(loss_ratio_cher) / len(loss_ratio_cher),
					alpha = 0.5,
					color = colors[0],
					#histtype = 'step',
					label = 'Cherenkov')
loss_ratio_scin = (int_ideal_scin - integral_scin) / int_ideal_scin
hist_scin = plt.hist(loss_ratio_scin,
					bins = hist_cher[1],
					range = (0,0.07),
					#density = True,
					weights = np.ones_like(loss_ratio_scin) / len(loss_ratio_scin),
					alpha = 0.5,
					color = colors[1],
					#histtype = 'step',
					label = 'Scintillating')

(mu_scin, sigma_scin) = norm.fit(loss_ratio_scin)
(mu_cher, sigma_cher) = norm.fit(loss_ratio_cher)
y_scin = norm.pdf(hist_scin[1],
				mu_scin,
				sigma_scin) / len(loss_ratio_scin)
y_cher = norm.pdf(hist_cher[1],
				mu_cher,
				sigma_cher) / len(loss_ratio_cher) 
l_cher = plt.plot(hist_cher[1],
				y_cher,
				'--',
				linewidth = 2,
				color = colors[0])
l_scin = plt.plot(hist_scin[1],
				y_scin,
				'--',
				linewidth = 2,
				color = colors[1])
print('Gaussian Scintillating: ' + str(mu_scin) + ', ' + str(sigma_scin))
print('Gaussian Cherenkov: ' + str(mu_cher) + ', ' + str(sigma_cher))

plt.xlabel(r'$\frac{E_{no-sat}-E_{sat}}{E_{no_sat}}$')
plt.ylabel('Counts')
plt.title('Integral loss')
plt.legend()

plt.show()
