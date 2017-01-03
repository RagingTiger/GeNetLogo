#!/usr/bin/env python

'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Description:
    Module for implementing genetic algorithm using NetLogo instance running on
    a Java virtual machine as the fitness function.
Documentation: http://deap.readthedocs.io/en/master/
Attribution: http://deap.readthedocs.io/en/master/examples/ga_onemax.html
Usage:
    genalgo onemax <population> <generations>
'''

# libraries
import random
import sys
from deap import creator, base, tools, algorithms


# functions
def dump_params(params):
    '''
    Function to dump parameters dictionary.
    '''
    # iterate over dict
    for key, val in params.iteritems():
        print 'Args: {0} | Vals: {1}'.format(key, val)


# closures
def pretty_print(func=dump_params, **kwargs):
    '''
    Closure for creating stdout template.
    '''
    # print border
    print '-'*80

    # call func
    func(**kwargs)

    # print border
    print '-'*80


# classes
class ArgError(Exception):
    '''
    Class inheriting from the Exception class that handles any error in the
    arguments passed to a constructor (see Parameters class below).
    '''
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class EvalFunc(object):
    pass


class FitFunc(object):
    pass


class IndividualAttrs(object):
    pass


class GenAlgo(base.Toolbox):
    '''
    Class that subclasses base.Toolbox and is used as a base class for other
    Genetic Algorithm implementations
    '''
    # constructor
    def __init__(self, population, generations, funcname, fitfunc, evalfunc,
                 args=(), indidividual_attrs=(), repeat_func=1):
        # call super class constructor
        base.Toolbox.__init__(self)

        # store creator method: first class functions
        self.create = creator.create

        # meta programming
        self._init_data(population, generations)
        self._create_individuals(indidividual_attrs)
        self._register_functions(funcname, fitfunc, args, repeat_func)
        self._register_genops(evalfunc)

    def _init_data(self, pop, gen):
        '''
        Private method to initialize 'toolbox' data
        '''
        # initialize data
        data = (
            'self.psize = {0}\n'
            'self.gensize = {1}\n'
        ).format(pop, gen)

        # compile + execute
        compiled_setup = compile(data, '<string>', 'exec')
        exec compiled_setup

    def _create_individuals(self, attrs):
        '''
        Private method to create unique individuals
        '''
        # creating simulations individual
        individuals = (
            'self.create(\'FitMax\', base.Fitness, weights=(1.0,))\n'
            'self.create(\'Individual\', list, fitness=creator.FitMax,\n'
            '               *{0})\n'
        ).format(attrs)

        # compile + execute
        compiled_setup = compile(individuals, '<string>', 'exec')
        exec compiled_setup

    def _register_functions(self, funcname, fitfunc, args, repeat):
        '''
        Private method to register functions
        '''
        # register functions
        functions = (
            'self.register(\'{0}\', {1}, *{2})\n'
            'self.register(\'individual\', tools.initRepeat,\n'
            '                      creator.Individual,\n'
            '                      self.{0}, {3})\n'
            'self.register(\'population\', tools.initRepeat, list,\n'
            '                      self.individual)\n'
        ).format(funcname, fitfunc, args, repeat)

        # compile + execute
        compiled_setup = compile(functions, '<string>', 'exec')
        exec compiled_setup

    def _register_genops(self, evalfunc):
        '''
        Private method to register genetic operations
        '''
        # register genetic operations
        genops = (
            'self.register(\'evaluate\', {0})\n'
            'self.register(\'mate\', tools.cxTwoPoint)\n'
            'self.register(\'mutate\', tools.mutFlipBit, indpb=0.05)\n'
            'self.register(\'select\', tools.selTournament,\n'
            '                      tournsize=3)\n'
        ).format(evalfunc)

        # compile + execute
        compiled_setup = compile(genops, '<string>', 'exec')
        exec compiled_setup


class OneMax(GenAlgo):
    '''
    Class to demonstrate onemax problem in DEAP.
    Attribution: http://deap.readthedocs.io/en/master/examples/ga_onemax.html
    '''
    # constructor
    def __init__(self, pops, gens):
        # call base class constructor
        GenAlgo.__init__(self, pops, gens, 'attr_bool', 'random.randint',
                         'self.evalOneMax', (0, 1), repeat_func=20)

        # self._init_data(pops, gens)
        # self._create_individuals(())
        # self._register_functions('attr_bool', 'random.randint', (0, 1), 20)
        # self._register_genops('self.evalOneMax')

    def evalOneMax(self, individual):
        '''
        Function to evaluate fitness of individuals in onemax problem.
        '''
        return sum(individual),

    def main(self):
        '''
        Function to run Onemax Genetic Algorithm.
        '''
        # initial population
        pop = self.population(self.psize)

        # get fitnesses of population
        fitnesses = list(map(self.evaluate, pop))

        # assign fitness to individual in population
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        # evolve population
        for g in range(self.gensize):
            offspring = algorithms.varAnd(pop, self, cxpb=0.5,
                                          mutpb=0.1)
            fits = self.map(self.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
            pop = self.select(offspring, k=len(pop))

        # select top 10
        self.top_fittest(pop, 10)

    def top_fittest(self, pop, levels):
        '''
        Function to print out the top most fit individuals in the population.
        '''
        # print out banner
        print 'Top {0} Most Fit Inviduals in Population:'.format(levels)

        # print out ranked individuals
        for i, ind in enumerate(tools.selBest(pop, k=levels)):
            space = ' '*(4-len(str(i+1)))
            print ' #{0}{2}Individual: {1}'.format(i+1, ind, space)
            print '{2}  {0}   - Fitness: {1}'.format(space, ind.fitness.values,
                                                     ' '*len(str(i+1)))


class RandomParameters(object):
    '''
    Class to generate parameters randomly within a given range and for a
    specifed type (i.e. float, int).
    Design Patterns: "Creational Pattern" (i.e. Builder)
    Reference:
        "Design Patterns: Elements of Reusable Object-Oriented Software",
         pages: 97 - 106
    '''
    # constructor
    def __init__(self, arg_dict):

        # store ranges
        self._range_dict = arg_dict

    def get_rparams(self):
        '''
        Function to return random parameters.
        '''
        # init dict
        rand_params = {}

        # generate attributes w/values
        for key, val in self._range_dict.iteritems():

            # check type
            if all(isinstance(item, int) or
               isinstance(item, float) for item in val):
                rval = random.uniform(val[0], val[1])
            else:
                raise TypeError('Arguments can only be int or float')

            # add key/val
            rand_params[key] = float(rval)

        # return random parameters
        return rand_params

    def print_randparams(self, randparams):
        '''
        Funciton to print out randomly generated parameters.
        '''
        # call self.dump_params()
        pretty_print(params=randparams)

    def print_args(self):
        '''
        Function to print out original parameter ranges.
        '''
        # call self.dump_params()
        pretty_print(params=self._range_dict)


# executable
if __name__ == '__main__':

    # exectuable only imports
    from docopt import docopt

    # banner
    start = '\nStarting Genetic Algorithm ...\n'

    # check CLA
    args = docopt(__doc__)

    # check commands
    if args['onemax']:
        print start
        ga = OneMax(int(args['<population>']), int(args['<generations>']))
        ga.main()
