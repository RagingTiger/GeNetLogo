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
PRGPATH = 'java_source/'
PRGNAME = 'INDISIM3Controller'
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
    def __init__(self, prgpath, prgname, kill_on_exit=True):

        # build command
        self.command = ['java', '-classpath', prgpath, prgname]

    # functions
    def _print_output(self, params):

        # get fit values
        for val in self._java_object.fitness_function(params):
            print '{0}'.format(val)

    # enter method for 'with' statement (see PEP 343)
    def __enter__(self):

        # start JVM
        self.process = subprocess.Popen(self.command)

        # wait
        time.sleep(1)

        # startup gateway
        params = GatewayParameters(auto_convert=True)
        self._gateway = JavaGateway(gateway_parameters=params)

        # get gateway entry point
        self._java_object = self._gateway.entry_point
        self.run_java_code = self._java_object.fitness_function

        # finally return self
        return self

    # exit method for 'with' statement (see PEP 343)
    def __exit__(self, exception_type, exception_value, traceback):

        # close gateway server
        self._gateway.shutdown()

        # kill jvm
        self.process.kill()


# executable
if __name__ == '__main__':

    # executable import only
    from docopt import docopt

    # check CLA
    args = docopt(__doc__)

    # control flow
    if args['run']:
        pass

    elif args['test']:

        # test code
        with JVM(PRGPATH, PRGNAME) as javacode:

            # run test
            javacode._print_output(TST_DICT)
