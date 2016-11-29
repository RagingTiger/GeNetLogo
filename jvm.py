#!/usr/bin/env python
'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Description:
    This module opens a Java virtual machine with code specified by user to
    be accessed as a fitness function in genetic algorithm application for
    NetLogo.
Usage:
    jvm run <java_classpath>
    jvm test

'''

# libraries
import subprocess
import time
import json

# 3rd party libraries
from py4j.java_gateway import JavaGateway, GatewayParameters, launch_gateway

# constants
PRG = '/java_source INDISIM3Controller'
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


# NOTE: Refactor with 'launch_gateway()'
# classes
class JVM(object):

    # constructor
    def __init__(self, prgpath):

        # start jvm
        self.pid = launch_gateway(classpath=prgpath, die_on_exit=True)

        # startup gateway
        params = GatewayParameters(auto_convert=True)
        self._gateway = JavaGateway(gateway_parameters=params)

        # get gateway entry point
        self._java_object = self._gateway.entry_point
        self.fitness_function = self._java_object.fitness_function

    # functions
    def run_java_code(self, params):

        # get fit values
        return self.fitness_function(params)

    def print_return(self, params):

        # get values
        values = self.run_java_code(params)

        # print
        for val in values:
            print val


# executable
if __name__ == '__main__':

    # executable import only
    from docopt import docopt

    # check CLA
    args = docopt(__doc__)

    # control flow
    if args['run']:

        # run code
        code = JVM(args['<java_classpath>'])

        code.print_return(TST_DICT)

    elif args['test']:

        # test code
        test = JVM(PRG)

        # print test
        test.print_return(TST_DICT)
