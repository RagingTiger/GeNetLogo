#!/usr/bin/env python

'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Program: genetlogo
Description:
    This program searches a combination space of NetLogo simulation parameters
    in an effort to find the maximum/minimum value.
Usage:
    genetlogo run <NetLogoJavaController>
    genetlogo test
'''

# libraries
import json
import genalgo
import jvm

# banner for stdout
banner = '''
             _____      _   _      _   _
            |  __ \    | \ | |    | | | |
            | |  \/ ___|  \| | ___| |_| |     ___   __ _  ___
            | | __ / _ \ . ` |/ _ \ __| |    / _ \ / _` |/ _ \\
            | |_\ \  __/ |\  |  __/ |_| |___| (_) | (_| | (_) |
             \____/\___\_| \_/\___|\__\_____/\___/ \__, |\___/
                                                    __/ |
                                                   |___/
'''


# classes
class GeNetLogo(genalgo.GenAlgo):
    '''
    Class to apply Genetic Algorithms to NetLogo simulations.
    '''
    # constructor
    def __init__(self, pops, gens, funcname, func, args, evalfunc):
        # call base class constructor
        genalgo.GenAlgo.__init__(self, pops, gens, funcname, func, args,
                                 evalfunc)

    # fitness evaluation function
    def eval_fit(self, individual):
        '''
        Function to evaluate fitness of individuals for GeNetLogo applications.
        '''
        return sum(individual),

    def fitness_generator(self, start_params):
        '''
        Function to take in starting parameters, generate random parameters,
        and call the fitness function with random parameters.
        '''
        # get names and values of arguments
        argnames, argranges = genalgo.dict_split(start_params)

        # get random parameters
        randparams = genalgo.RandomParameters(argnames, argranges)

        # check params
        randparams.dump_dict()


# executable
if __name__ == '__main__':

    # executabel import only
    from docopt import docopt

    # print
    print banner

    # check CLA
    args = docopt(__doc__)

    # control flow
    if args['test']:
        java_controller = jvm.PRG
        parameters = '../INDISIM3_Parameters.json'

    elif args['run']:
        java_controller = args['<NetLogoJavaController>']

    # start JVM
    print 'Starting Java Virtual Machine ...'
    with jvm.JVM(java_controller) as jcode:

        # launch Genetic Algorithm
        print 'Virtual Machine Started!\nStarting Genetic Algorithm ...'
        ga = GeNetLogo(10, 10, 'attr_bool', 'random.randint', (0, 1),
                       'self.eval_fit')

        # open json parameters file
        with open(parameters, 'r') as params:
            ga.fitness_generator(json.load(params))
