#!/usr/bin/env python
'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Program: genetlogo
Description:
    This program searches a combination space of NetLogo simulation parameters
    in an effort to find the maximum/minimum value.
'''

# libraries
import subprocess
import time

# 3rd party libraries
from py4j.java_gateway import JavaGateway
import deap

# constants
CMD = ['java', 'INDISIM3Controller']
TST = (13.0, 12.0, 500.0, 1.80, 50.0, 0.5, 0.0, 0.50, 0.25, 200.0, 300.0,
       901200.0, 10.0, 0.040, 3.00, 200)

# start JVM
subprocess.os.chdir('java/')
jvm = subprocess.Popen(CMD)

# wait
time.sleep(1)

# startup gateway
gateway = JavaGateway()

# get function from JVM
indisim_object = gateway.entry_point
fit = indisim_object.fitness_function(13.0, 12.0, 500.0, 1.80, 50.0, 0.5, 0.0,
                                      0.50, 0.25, 200.0, 300.0, 901200.0, 10.0,
                                      0.040, 3.00, 200)
# print return value
print fit[0], fit[1], fit[2]

# close gateway server
gateway.shutdown()

# kill jvm
jvm.kill()
