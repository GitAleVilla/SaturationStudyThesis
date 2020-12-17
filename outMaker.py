import itertools
f = open('9pe_peak_10k.txt','w')

events = 1
fibers = 10000

ID = 1
for fib in range(fibers):
	fibID = fib+1
	x = (fib+1) * 1.
	y = (fib+1) * 1.
	z = (fib+1) * 1.
	n = 9
	time = 15.
	strin = str(ID) 
	strin = strin + ' Scin '
	strin = strin + str(fibID)
	strin = strin + ' ' + str(x)
	strin = strin + ' ' + str(y)
	strin = strin + ' ' + str(z)
	strin = strin + ' ' + str(n)
	i = 1
	for _  in itertools.repeat(None, n):
		strin = strin + ' ' + str(time)
		i =+ 1
	f.write(strin + '\n')

f.close()
