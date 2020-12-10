#!/usr/bin/env python

from PIL import Image
from scipy.fftpack import dct, idct
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import signal

fs = 1/0.05 # 50ms
nqy = 0.5 * fs * 60 # 600

b1,a1   = signal.butter(6,[40.0/nqy , 200.0/nqy], 'band') #heart rate parameter for fft
b, a    = signal.butter(6, [10.0/nqy , 30.0/nqy],'band') #breath rate parameter for fft 

tukwd = signal.tukey(200,alpha=0.5)
while(1):
	stat = int(input("please input stat: "))
	strn = int(input("please input file: "))
	times = int(input("please input times: "))

	txt = ".\%s\%s\out-ch-%s.txt" % (str(stat), str(strn), str(times))
	file_ch = open(txt, "r")
	ch_cnt = file_ch.read()
	file_ch.close()


	ch_lst = ch_cnt.split()
	ch = [float(x) for x in ch_lst]

	dct = dct(ch, norm = 'ortho')
	hr_d = np.zeros(500)
	br_d = np.zeros(500)
	for i in range(500):
		if i>=10 and i <= 30:
			br_d[i] = ch[i]
		elif i >=40 and i<=200:
			hr_d[i] = ch[i]
	hrn = idct(hr_d, norm = 'ortho')
	brn = idct(br_d, norm = 'ortho')



	x = np.arange(500)
	plt.figure()

	 

	#plt.ylim(20, 150)

	#(3.0)breathing rate bandpass filter
	hr0 = signal.filtfilt(b1, a1, ch)
	br0 = signal.filtfilt(b, a, ch)
	#(3.0.1) remove DC level
	'''
	br0d = np.diff(br0)
	br0d = np.append(br0d,0.0)
	hr0d = np.diff(hr0)
	hr0d = np.append(hr0d,0.0)
	'''
	#(3.0.2) windowing

	plt.subplot(121)
	plt.plot(x, hr0, 'r')
	plt.subplot(122)
	plt.plot(x, br0, 'r')
	plt.show()


input()