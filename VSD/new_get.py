''' 
Vital Signs : 2019/2/13 15:47
ex0:
Display heart rate & breathing rate data
(1)Download lib:
install:
~#sudo pip intall mmWave
update:
~#sudo pip install mmWave -U
'''
import serial
import struct
import datetime
import requests
import json
import queue
from firebase import firebase
from scipy import signal

import numpy as np
from mmWave import vitalsign

 
class globalV:
	count = 0
	hr = 0.0
	br = 0.0
	def __init__(self, count):
		self.count = count
		

#UART initial
try:    #pi 3
	port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
except: #pi 2
	port = serial.Serial("/dev/ttyAMA0",baudrate = 921600, timeout = 0.5)

#**************************************************** 
# Set Firebase URL, Location, Pin No                                                   
#**************************************************** 
firebase_url = 'https://mmwave-project.firebaseio.com/' 
fdb = firebase.FirebaseApplication(firebase_url, None)

#
#initial global value
#
gv = globalV(0)

vts = vitalsign.VitalSign(port)

hr_q = queue.Queue(maxsize=200)
br_q = queue.Queue(maxsize=200)

for i in range(200):
  hr_q.put(0)
  br_q.put(0)

# UART : 50 ms
def uartGetTLVdata(name):
	print("mmWave: {:} example:".format(name))
	pt = datetime.datetime.now()
	ct = datetime.datetime.now()
	port.flushInput()
	cont = 0
	num = 0
	hr_tmp = 0
	br_tmp = 0
	while True:
		"""
    if cont == time:
			break
		if num == 0:
			txt = "out-hr-%s.txt" % (str(cont))
			out_hr = open(txt, "w")
			txt = "out-br-%s.txt" % (str(cont))
			out_br = open(txt, "w")
			txt = "out-ch-%s.txt" % (str(cont))
			out_ch = open(txt, "w")
			txt = "out-mv-%s.txt" % (str(cont))
			out_mv = open(txt, "w")
			num = num + 1
		"""
		#mmWave/VitalSign tlvRead & Vital Sign 
		#print(datetime.datetime.now().time())
		pt = datetime.datetime.now()
		(dck , vd, rangeBuf) = vts.tlvRead(False)
		vs = vts.getHeader()
		#vts.showHeader()
		 
		if dck:
			ct = datetime.datetime.now()
			gv.br = vd.breathingRateEst_FFT
			gv.hr = vd.heartRateEst_FFT
			ch_tmp = vd.unwrapPhasePeak_mm
			mv_tmp = vd.motionDetectedFlag
			fs = 1/0.05 # 50ms
			nqy = 0.5 * fs * 60 # 600
			b1,a1   = signal.butter(6,[40.0/nqy , 200.0/nqy], 'band') #heart rate parameter for fft
			b, a    = signal.butter(6, [10.0/nqy , 30.0/nqy],'band') #breath rate parameter for fft 
			cd6  = np.zeros(200)
			cd6[:-1] = cd6[1:]
			cd6[-1]  = vd.unwrapPhasePeak_mm
			hr0 = signal.filtfilt(b1, a1, cd6)
			br0 = signal.filtfilt(b, a, cd6)
			brse = vd.sumEnergyBreathWfm
			hrse = vd.sumEnergyHeartWfm 
			x = -10000 +10000/9e+10*brse+hrse
			y = -2000 +2000/2.5e+8*brse+hrse
			if x>0:
			  stat = 2 #move
			elif y>0:
			  stat = 1 #human
			else:
			  stat = 0 #human
			print("Heart Rate:{:.4f} Breath Rate:{:.4f} #:{:d}  {}".format(gv.hr,gv.br,vs.frameNumber, ct-pt))
			if gv.hr >= 0 and gv.hr<=500:
				hr_tmp = gv.hr
			if gv.br >= 0 and gv.br<=500:
				br_tmp = gv.br
			"""
			out_hr.write( "%.5s " % str(("%.5f" % hr_tmp)) )
			out_br.write( "%.5s " % str(("%.5f" % br_tmp)) )
			out_ch.write( "%.5s " % str(("%.5f" % ch_tmp)) )
			out_mv.write( "%.5s " % str(("%.5f" % mv_tmp)) )
			"""
			#**************************************************** 
			# Insert Data                                                                              
			#****************************************************
			tmp = hr_q.get()
			tmp = br_q.get()
			hr_q.put(hr0)
			br_q.put(br0)
			#data = {'Heart Rate':hr_tmp, 'Breath Rate':br_tmp, 'ch':ch_tmp, 'mv':mv_tmp}
      #for data in new_users:		
			#for data in range(200):
			#fdb.put('/0', 'HR0', [list(hr_q.queue)[0], list(hr_q.queue)[1], list(hr_q.queue)[2], list(hr_q.queue)[3]])
			#fdb.put('/0', 'BR0', list(br_q.queue)[0])
      
			fdb.put('/0', 'stat', stat)
			fdb.put('/0', 'heart rate', gv.hr)
			fdb.put('/0', 'breath rate', gv.br)
			fdb.put('/0', 'cd', ch_tmp)
			#result = requests.post(firebase_url + str(cont) + '.json', data=json.dumps(data))
			"""
			if num == 500:
				out_br.close()
				out_hr.close()
				out_ch.close()
				out_mv.close()
				num = 0
				cont = cont + 1
			else:
				num = num + 1
			"""
	print("END")
uartGetTLVdata("VitalSign")

