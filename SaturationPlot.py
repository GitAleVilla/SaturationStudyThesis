import numpy as np
import h5py
import pickle
import matplotlib.pyplot as plt
import scipy.optimize as opt


#########################################
############### CLASSES #################
#########################################


class Fiber():
	def __init__(self):
		self.ID = []		#list [IDNumber, x, y, z]
		self.ToAph = []		#list [t_ph1, t_ph2, ...]
		self.Integral = 0.	#float
		self.Peak = 0.		#float
		self.ToA = 0.		#float
		self.ToT = 0.		#float
		self.ToP = 0.		#float
		self.Waveform = np.array([])	#list data waveform
		

class Event():
	def __init__(self):
		self.ID	= 0		#int EventNumber
		self.DataFibS = []	#List of Fiber class Scin [fib1, fib2, ...]
		self.DataFibC = []	#List of Fiber class Cher [fib1, fib2, ...]


#########################################
################# MAIN ##################
#########################################


################ IMPORT #################

Path1 = '/home/storage/TesiVilla/Data/Electron40GeV/'
#Path = '/home/storage/TesiVilla/Data/Pion40GeV/'
#Path = '/home/storage/TesiVilla/Data/Electron40GeV/SmallRise/'
#Path = '/home/storage/TesiVilla/Data/Pion40GeV/SmallRise/'
#Path = '/home/storage/TesiVilla/Data/Electron40GeV/SmallFall/'
#Path = '/home/storage/TesiVilla/Data/Pion40GeV/SmallFall/'
Path2 = '/home/storage/TesiVilla/Data/Electron40GeV/SmallCellSize/'
#Path = '/home/storage/TesiVilla/Data/Pion40GeV/SmallCellSize/'
Path3 = '/home/storage/TesiVilla/Data/Electron40GeV/SmallerCellSize/'
#Path = '/home/storage/TesiVilla/Data/Pion40GeV/SmallerCellSize/'
#Path = '/home/storage/TesiVilla/Data/Electron40GeV/NoAP/'
#Path = '/home/storage/TesiVilla/Data/Test/'

pickleFileName1 = 'Events.pikle'
#pickleFileName2 = 'Events2.pikle'
#pickleFileName3 = 'Events3.pikle'
#pickleFileName4 = 'Events4.pikle'

#RootOutputName = 'Plots.root'
#RootOutputName = 'WavesS.root'
#RootOutputName = 'WavesC.root'
#RootOutputName = 'BestFiber.root'
#RootOutputName = 'Correlations.root'
#RootOutputName = 'Waveforms1peak10k.root'
#RootOutputName = 'WaveformsSumS.root'
#RootOutputName = 'WaveformsSumC.root'

#############################
def line(x, m, q):
	return (m * x) + q

plt.figure()

cut = 0.01 #percentuale
I_mean = 49.375
Pedestal = 2.5

#############   FILE 1  #####
infile = open(Path1 + pickleFileName1, 'rb')
eventList = pickle.load(infile, encoding='bytes')
infile.close()

number_of_pe1 = np.array([])
integral1 = np.array([])
for event in eventList:
	print('File 1 Event: ' + str(event.ID) + ' / ' + str(len(eventList)-1))

#---------> Correlation Integral - Number of Ph <-----------
	for x in range(len(event.DataFibS)):
		number_of_pe1 = np.append(number_of_pe1, len(event.DataFibS[x].ToAph))
		integral1 = np.append(integral1, event.DataFibS[x].Integral)
#integral1 = integral1 - Pedestal
plt.plot(number_of_pe1,
		 integral1,
		 marker='.',
		 linestyle='None',
		 markersize=2,
		 label='25 micron')
del eventList

#############   FILE 2  #####
infile = open(Path2 + pickleFileName1, 'rb')
eventList = pickle.load(infile, encoding='bytes')
infile.close()

number_of_pe2 = np.array([])
integral2 = np.array([])
for event in eventList:
	print('File 2 Event: ' + str(event.ID) + ' / ' + str(len(eventList)-1))

#---------> Correlation Integral - Number of Ph <-----------
	for x in range(len(event.DataFibS)):
		number_of_pe2 = np.append(number_of_pe2, len(event.DataFibS[x].ToAph))
		integral2 = np.append(integral2, event.DataFibS[x].Integral)
#integral2 = integral2 - Pedestal
plt.plot(number_of_pe2,
		 integral2,
		 marker='.',
		 linestyle='None',
		 markersize=2,
		 label='10 micron')
del eventList

#############   FILE 3  #####

infile = open(Path3 + pickleFileName1, 'rb')
eventList = pickle.load(infile, encoding='bytes')
infile.close()

number_of_pe3 = np.array([])
integral3 = np.array([])
for event in eventList:
	print('File 3 Event: ' + str(event.ID) + ' / ' + str(len(eventList)-1))

#---------> Correlation Integral - Number of Ph <-----------
	for x in range(len(event.DataFibS)):
		number_of_pe3 = np.append(number_of_pe3, len(event.DataFibS[x].ToAph))
		integral3 = np.append(integral3, event.DataFibS[x].Integral)
integral3 = integral3 - Pedestal
plt.plot(number_of_pe3,
		 integral3,
		 marker='.',
		 linestyle='None',
		 markersize=2,
		 label='1 micron')
del eventList

x_space = np.linspace(0., np.max(number_of_pe3), int(np.max(number_of_pe3) / 50))
int_range = integral3[(number_of_pe3 > 1000) & (number_of_pe3 < 1500)]
number_of_pe_range = number_of_pe3[(number_of_pe3 > 1000) & (number_of_pe3 < 1500)]
optParameters, pcov = opt.curve_fit(line, number_of_pe_range, int_range)
func, = plt.plot(x_space,
				 line(x_space, I_mean, Pedestal),
				 label='Ideal integral')
func_plus, = plt.plot(x_space, line(x_space, *optParameters))
#print(*optParameters)

#plt.fill_between(x_space,
#				 line(x_space, I_mean, 0.) -2000.,
#				 line(x_space, I_mean, 0.) +2000.,
#				 facecolor = 'green',
#				 alpha = 0.3)

plt.xlabel('Number of pe')
plt.ylabel('Integral (A.U.)')

plt.legend()
#plt.show()

plt.figure()

int_pe_ratio1 = np.array([])
int_pe_ratio2 = np.array([])
int_pe_ratio3 = np.array([])

for i in range(number_of_pe1.size):
	print('Rescaling 1: ' + str(i) + ' / ' + str(number_of_pe1.size - 1))
	new_data = integral1[i] / number_of_pe1[i]
	int_pe_ratio1 = np.append(int_pe_ratio1, new_data)
plt.plot(number_of_pe1, int_pe_ratio1, marker='.', linestyle='None', markersize=2, label='25 micron')
#out_range_up = np.count_nonzero(int_diff1 > cut)
#out_range_down = np.count_nonzero(int_diff1 < -cut)
#out_range1 = out_range_up + out_range_down

for i in range(number_of_pe2.size):
	print('Rescaling 2: ' + str(i) + ' / ' + str(number_of_pe2.size - 1))
	new_data = integral2[i] / number_of_pe2[i]
	int_pe_ratio2 = np.append(int_pe_ratio2, new_data)
plt.plot(number_of_pe2, int_pe_ratio2, marker='.', linestyle='None', markersize=2, label='10 micron')
#out_range_up = np.count_nonzero(int_diff2 > cut)
#out_range_down = np.count_nonzero(int_diff2 < -cut)
#out_range2 = out_range_up + out_range_down
#print(str(out_range2) + " strings out of range over " + str(number_of_pe2.size))
#print(str(out_range2 / number_of_pe2.size * 100) + "%")

for i in range(number_of_pe3.size):
	print('Rescaling 3: ' + str(i) + ' / ' + str(number_of_pe3.size - 1))
	new_data = integral3[i] / number_of_pe3[i]
	int_pe_ratio3 = np.append(int_pe_ratio3, new_data)
plt.plot(number_of_pe3, int_pe_ratio3, marker='.', linestyle='None', markersize=2, label='1 micron')
#out_range_up = np.count_nonzero(int_diff3 > cut)
#out_range_down = np.count_nonzero(int_diff3 < -cut)
#out_range3 = out_range_up + out_range_down

#print(str(out_range1) + " strings out of range over " + str(number_of_pe1.size))
#print(str(out_range1 / number_of_pe1.size * 100) + "%")
#print(str(out_range2) + " strings out of range over " + str(number_of_pe2.size))
#print(str(out_range2 / number_of_pe2.size * 100) + "%")
#print(str(out_range3) + " strings out of range over " + str(number_of_pe3.size))
#print(str(out_range3 / number_of_pe3.size * 100) + "%")

#print('I parametri sono: ')
print(str(number_of_pe_range.size) + ' of ' + str(number_of_pe3.size))
#print(int_range.shape)
print(*optParameters)
#print(type(*optParameters))
print(type(optParameters))


func_fit, = plt.plot(x_space, line(x_space, 0., I_mean))

plt.fill_between(x_space,
				 line(x_space, 0., I_mean) * (1 - cut),
				 line(x_space, 0., I_mean) * (1 + cut),
				 facecolor = 'green',
				 alpha = 0.3)

plt.xlabel('Number of pe')
plt.ylabel('Integral / pe (A.U.)')
plt.legend()



plt.show()


