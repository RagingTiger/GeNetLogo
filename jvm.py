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

# 3rd party libraries
from py4j.java_gateway import JavaGateway

# constants
PRG = 'INDISIM3Controller'
TST = (13.0, 12.0, 500.0, 1.80, 50.0, 0.5, 0.0,
       0.50, 0.25, 200.0, 300.0, 901200.0, 10.0,
       0.040, 3.00, 200)


# classes
class JVM(object):

    # constructor
    def __init__(self, prgpath):

        # build command
        self.cmd = ['java', prgpath]

    # functions
    def run_java_code(self, params):

        # get fit values
        fit = self._java_object.fitness_function(*params)

        # print values
        for val in fit:
            print val

    # enter method for 'with' statement (see PEP 343)
    def __enter__(self):

        # start JVM
        subprocess.os.chdir('java_source/')
        self._jvm = subprocess.Popen(self.cmd)

        # wait
        time.sleep(1)

        # startup gateway
        self._gateway = JavaGateway()

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
        jcode.run_java_code(TST)
