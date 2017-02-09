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
    def __init__(self, params, prgpath, prgname):
        # call base class constructor
        # genalgo.GenAlgo.__init__(self, pops, gens, funcname, func, args,
        #                          evalfunc)
        jvm.JVM.__init__(self, prgpath, prgname)

        # store params object
        self.parameter_ranges = genalgo.RandomParameters(params)


class INDISIMGenAlgo(GeNetLogo):
    '''
    Class to implement a Genetic Algorithm with JVM interface for the INDISIM
    NetLogo model
    '''
    # constructor
    def __init__(self, params, prgpath, prgname):
        # NOTE: need to clarify what is unique to this class and what varies
        # call super class constructor
        GeNetLogo.__init__(self, params, prgpath, prgname)
        self._superclass_init()

    def main(self):
        '''
        Method for implementing actual genetic algorithm
        '''
        pass

    def gen_individual(self, container, func):
        '''
        Method to create individual, calculate the fitness values, and store
        simulation parameters with it
        '''
        # first call initIterate
        instance = genalgo.tools.initIterate(container, func)

        # store parameters
        instance.params = self._rand_params

        # return
        return instance

    def get_fitness(self):
        '''
        Method to call fitness_function on JVM NetLogo code and convert
        JavaArray to a list
        '''
        # first store new randparams
        self._rand_params = self.parameter_ranges.get_rparams()

        # then get fitness/call JVM
        return self.run_java_code(self._rand_params)

    # fitness evaluation function
    def eval_fit(self, individual):
        '''
        Method to evaluate fitness of individuals for GeNetLogo applications
        '''
        # NOTE: Need to investigate properties of JavaArray object
        return sum(individual),

    def _mating(self, ind1, ind2):
        '''
        Private method to mate two 'dict' object individuals
        '''
        # take percentage of fitnesses
        total = float(ind1.fitness.values) + float(ind2.fitness.values)

        # get individual percents
        perc1 = float(ind1.fitness.values) / total
        perc2 = float(ind2.fitness.values) / total

        # get parant dicts
        d1 = ind1.params
        d2 = ind2.params

        # get dict keys
        keys = [key for key in ind1.params.iterkeys()]

        # now create child
        return {key: (perc1 * d1[key]) + perc2 * d2[key] for key in key}

    def _mutating(self, individual):
        '''
        Private method to mutate an individual
        '''
        pass

    def _reval_fitness(self, population):
        '''
        Private method to evaluate fitness of multiple sequence types
        '''
        # iterate through population
        for ind in population:

            # closure
            def closure():
                return self.run_java_code(ind.params)

            # first call evalfit
            genalgo.tools.initIterate(container, closure)


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
        with INDISIMGenAlgo(jvm.TST_DICT, jvm.PRGPATH, jvm.PRGNAME) as indisim:

            # register fitness function
            indisim._init_data(10, 10)
            indisim._create_individuals('netlogo_params=dict')
            indisim._register_functions('self.get_fitness',
                                        'self.gen_individual')
            indisim._register_genops('self.eval_fit')

            # run genetic algorithm
            # NOTE: seems to be problem with 'freezing' arguments
            #       might need to use closure to add params to a function
            #       then pass those parameters to the fitness function?
            indisim.main(func=indisim._reval_fitness)
