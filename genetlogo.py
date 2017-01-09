#!/usr/bin/env python

'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Description:
    This program searches a combination space of NetLogo simulation parameters
    in an effort to find the maximum/minimum value.
Usage: genetlogo test
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
class GeNetLogo(genalgo.GenAlgo, jvm.JVM):
    '''
    Class to apply Genetic Algorithms to NetLogo simulations.
    '''
    # constructor
    def __init__(self, pdict, prgpath, prgname):
        # call base class constructor
        # genalgo.GenAlgo.__init__(self, pops, gens, funcname, func, args,
        #                          evalfunc)
        jvm.JVM.__init__(self, prgpath, prgname)


class INDISIMGenAlgo(GeNetLogo):
    '''
    Class to implement a Genetic Algorithm with JVM interface for the INDISIM
    NetLogo model
    '''
    # constructor
    def __init__(self, prgpath, prgname):
        # NOTE: need to clarify what is unique to this class and what varies
        # call super class constructor
        GeNetLogo.__init__(self, {}, prgpath, prgname)
        self._superclass_init()

    def gen_individual(self, container, func):
        '''
        Method to create individual, calculate the fitness values, and store
        simulation parameters with it
        '''
        # first call initIterate
        instance = genalgo.tools.initIterate(container, func)

        # store parameters
        instance.params = func.args

        # return
        return instance

    def get_fitness(self, params):
        '''
        Method to call fitness_function on JVM NetLogo code and convert
        JavaArray to a list
        '''
        return self.run_java_code(params)

    # fitness evaluation function
    def eval_fit(self, individual):
        '''
        Function to evaluate fitness of individuals for GeNetLogo applications
        '''
        # NOTE: Need to investigate properties of JavaArray object
        return sum(individual),


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

        # start JVM
        with INDISIMGenAlgo(jvm.PRGPATH, jvm.PRGNAME) as indisim:

            # register fitness function
            indisim._init_data(10, 10)
            indisim._create_individuals('params=dict')
            indisim._register_functions('self.get_fitness',
                                        jvm.TST_DICT, 'self.gen_individual')
            indisim._register_genops('self.eval_fit')

            # run genetic algorithm
            # NOTE: seems to be problem with 'freezing' arguments
            #       might need to use closure to add params to a function
            #       then pass those parameters to the fitness function?
            indisim.main()
