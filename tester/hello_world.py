import ivi
import threading
import time
from subprocess import Popen

psu = ivi.rigol.rigolDP832("USB0::0x1AB1::0x0E11::DP8C171701414::INSTR")
psu.outputs[0].voltage_level = 5.0

time.sleep(1)

stop = False

def measure_thread():
	energy = 0.0
	while not stop:
		start = time.time()
		curr_power = psu.outputs[2].measure('power')
		energy = energy + curr_power * 0.5 / 3600.0
		print (str(curr_power) + " " + str(energy))
		end = time.time()
		time.sleep(0.5 - (end - start))
	print("Total energy: " +str(energy))



for freq in range(200000, 2000000, 100000):
	print("Frequency: " + str(freq));

	stop = False
	m_th = threading.Thread(target=measure_thread)
	m_th.daemon = True;
	m_th.start();

	p = Popen(['taskset', '-c', '4', '/root/testapp/sqrt.o'])
	p.wait();
	stop = True
	m_th.join();
