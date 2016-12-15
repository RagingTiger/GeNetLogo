#!/usr/bin/env python

'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Description:
    This program searches a combination space of NetLogo simulation parameters
    in an effort to find the maximum/minimum value.
Usage:
    genetlogo run <NetLogoJavaControllerPath> <ParametersFile.json>
    genetlogo test random <ParametersFile.json>
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

    def fitness_generator(self, start_params, random=False):
        '''
        Function to take in starting parameters, generate random parameters,
        and call the fitness function with random parameters.
        '''
        if random:
            # get random parameters
            randparams = genalgo.RandomParameters(start_params)

            # get params
            params = randparams.get_rparams()

            # print  randparams
            randparams.print_randparams(params)

        else:
            # non random params
            params = start_params

            # print params
            genalgo.pretty_print(params=params)

        # return dict
        return params


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
        progpath = jvm.PRGPATH
        progname = jvm.PRGNAME

        # genetlogo object
        ga = GeNetLogo(10, 10, 'attr_bool', 'random.randint', 'self.eval_fit',
                       (0, 1))

        if args['random']:
            # open json parameters file
            with open(args['<parameters>'], 'r') as params:
                pdict = ga.fitness_generator(json.load(params), random=True)
        else:
            pdict = ga.fitness_generator(jvm.TST_DICT)

    elif args['run']:

        # get program path and prgram name
        progpath, progname = args['<NetLogoJavaControllerPath>'].rsplit('/', 1)

        # genetlogo object
        ga = GeNetLogo(10, 10, 'attr_bool', 'random.randint', 'self.eval_fit',
                       (0, 1))

        # open json parameters file
        with open(args['<ParametersFile.json>'], 'r') as params:
                pdict = ga.fitness_generator(json.load(params), random=True)

    # start JVM
    print 'Starting Java Virtual Machine ...'
    with jvm.JVM(progpath, progname) as jcode:

        # launch Genetic Algorithm
        print 'Virtual Machine Started!\nStarting Genetic Algorithm ...'

        # print results
        print 'Fitness Results:{0}'.format('\n')

        # NOTE: need to refactor with closure
        for val in jcode.fitness_function(pdict):
            print '{0}{1} {2}{3}'.format(' '*2, '*', val, '\n')
