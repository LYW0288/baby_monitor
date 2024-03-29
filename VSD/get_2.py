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

#
#initial global value
#
gv = globalV(0)

vts = vitalsign.VitalSign(port)

 
# UART : 50 ms
def uartGetTLVdata(name):
	print("mmWave: {:} example:".format(name))
	pt = datetime.datetime.now()
	ct = datetime.datetime.now()
	port.flushInput()
	cont = 0
	hr_tmp = 0
	br_tmp = 0
	while True:
		if cont == 2:
			break
		txt = "out-hr-%s.txt" % (str(cont))
		out_hr = open(txt, "w")
		txt = "out-br-%s.txt" % (str(cont))
		out_br = open(txt, "w")
		for i in range(500):
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
				 
				print("Heart Rate:{:.4f} Breath Rate:{:.4f} #:{:d}  {}".format(gv.hr,gv.br,vs.frameNumber, ct-pt))
				if gv.hr >= 0 and gv.hr<=500:
					hr_tmp = gv.hr
				if gv.br >= 0 and gv.br<=500:
					br_tmp = gv.br
				out_hr.write( "%.5s " % str(("%.5f" % hr_tmp)) )
				out_br.write( "%.5s " % str(("%.5f" % br_tmp)) )


				#print("Filter OUT:{0:.4f}".format(vd.outputFilterHeartOut))
				'''
				print("EST FFT:{0:.4f}".format(vd.heartRateEst_FFT))
				print("EST FFT 4Hz:{0:.4f}".format(vd.heartRateEst_FFT_4Hz))
				print("EST FFT xCorr:{0:.4f}".format(vd.heartRateEst_FFT_4Hz))
				print("Confi Heart Out:{0:.4f}".format(vd.confidenceMetricHeartOut))
				print("Confi Heart O 4Hz:{0:.4f}".format(vd.confidenceMetricHeartOut_4Hz))
				print("Confi Heart O xCorr:{0:.4f}".format(vd.confidenceMetricHeartOut_xCorr))
				'''
				#print("RangeBuf Length:{:d}".format(len(rangeBuf)))
				#print(rangeBuf)
		out_br.close()
		out_hr.close()
		cont = cont + 1
	print("END")
uartGetTLVdata("VitalSign")

