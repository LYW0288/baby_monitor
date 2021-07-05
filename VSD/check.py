
import serial
import struct
import datetime

import numpy as np
from mmWave import vitalsign
from firebase import firebase
import firebase_admin
from firebase_admin import credentials, db

 
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

#
#initial global value
#
gv = globalV(0)

vts = vitalsign.VitalSign(port)

 
#**************************************************** 
# Set Firebase URL, Location, Pin No                                                   
#**************************************************** 
#firebase_url = 'https://mmwave-project.firebaseio.com/' 
#fdb = firebase.FirebaseApplication(firebase_url, None)
cred = credentials.Certificate('/home/pi/mmwave-project-firebase-adminsdk-epepi-6b9c45acdd.json')
firebase_admin.initialize_app(cred, {
                              'databaseURL':'https://mmwave-project.firebaseio.com/'
})
ref = db.reference('/0/')
ref2 = db.reference('/1/cd/')

# UART : 50 ms
def uartGetTLVdata(name):
	print("mmWave: {:} example:".format(name))
	pt = datetime.datetime.now()
	ct = datetime.datetime.now()
	port.flushInput()
	a = 0
	while True:
		#mmWave/VitalSign tlvRead & Vital Sign 
		#print(datetime.datetime.now().time())
		pt = datetime.datetime.now()
		(dck , vd, rangeBuf) = vts.tlvRead(False)
		vs = vts.getHeader()
		#vts.showHeader()
		 
		if dck:
			a = a + 1
			ct = datetime.datetime.now()
			gv.br = vd.breathingRateEst_FFT
			gv.hr = vd.heartRateEst_FFT
			ch_tmp = vd.unwrapPhasePeak_mm
			hrs = vd.sumEnergyHeartWfm
			brs = vd.sumEnergyBreathWfm
			x = -10000 +10000/9e+10*brs+hrs
			y = -2000 +2000/2.5e+8*brs+hrs
			if x>0:
				stat = 2
			else:
				if y>0:
					stat = 1
				else:
					stat = 0
			print("stat = {:d}".format(stat))
			if a==100:
				ref.update({"stat":stat, "heart rate": gv.hr, "breath rate": gv.br})
				ref2.push(ch_tmp)
				#fdb.put('/0', 'stat', stat)
				#fdb.put('/0', 'heart rate', gv.hr)
				#fdb.put('/0', 'breath rate', gv.br)
				#fdb.post('/1/cd', ch_tmp)
				a = 0
uartGetTLVdata("VitalSign")
