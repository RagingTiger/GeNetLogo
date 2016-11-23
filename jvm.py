#!/usr/bin/env python
'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Program: jvm
Description:
    This module opens a Java virtual machine with code specified by user to
    be accessed as a fitness function in genetic algorithm application for
    NetLogo.
'''

# libraries
import subprocess
import time
import json

# 3rd party libraries
from py4j.java_gateway import JavaGateway, GatewayParameters

# constants
PRG = 'INDISIM3Controller'
TST_TUPLE = (13.0, 12.0, 500.0, 1.80, 50.0, 0.5, 0.0,
             0.50, 0.25, 200.0, 300.0, 901200.0, 10.0,
             0.040, 3.00, 200)

TST_DICT = {

  "init_bact1": 1.0,
  "init_loc_nutr": 500.0,
  "yield_1": 1.80,
  "mass_repr": 50.0,
  "avail_k": 0.5,
  "inhib_k": 0.0,
  "uptake_k": 0.50,
  "maint": 0.25,
  "viabil": 200.0,
  "fed_nutr": 300.0,
  "out_res_nutr": 901200.0,
  "len_time_fed": 10.0,
  "in_out_percnt": 0.040,
  "init_bact2": 25.0,
  "yield_2": 3.00,
  "ticks": 200.00

}


# classes
class JVM(object):

    # constructor
    def __init__(self, prgpath):

        # build command
        self.cmd = ['java', prgpath]

    # functions
    def run_java_code(self, params):

        # get fit values
        return self._java_object.fitness_function(params)

    # enter method for 'with' statement (see PEP 343)
    def __enter__(self):

        # start JVM
        subprocess.os.chdir('java_source/')
        self._jvm = subprocess.Popen(self.cmd)

        # wait
        time.sleep(1)

        # startup gateway
        params = GatewayParameters(auto_convert=True)
        self._gateway = JavaGateway(gateway_parameters=params)

        # get gateway entry point
        self._java_object = self._gateway.entry_point
        self.fitness_function = self._java_object.fitness_function

        # finally return self
        return self

    # exit method for 'with' statement (see PEP 343)
    def __exit__(self, exception_type, exception_value, traceback):

        # close gateway server
        self._gateway.shutdown()

        # kill jvm
        self._jvm.kill()


# executable
if __name__ == '__main__':

    # using with keyword for safe execution
    with JVM(PRG) as jcode:
        print 'JVM up!'
        fit = jcode.run_java_code(TST_DICT)
        for item in fit:
            print item
