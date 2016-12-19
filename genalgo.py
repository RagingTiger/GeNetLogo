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


class GenAlgo(object):
    '''
    Class used as base class by other Genetic Algorithm classes.
    Design Patterns: Template Method
    Reference:
        "Design Patterns: Elements of Reusable Object-Oriented Software",
         pages: 325 - 330
    '''
    # constructor
    def __init__(self, population, generations, funcname, fitfunc, evalfunc,
                 args=(), indidividual_attrs=(), repeat_func=1):

        # meta programming
        self.setup = (
            '# initialize data\n'
            'self.toolbox = base.Toolbox()\n'
            'self.psize = {0}\n'
            'self.gensize = {1}\n'

            '# creating simulations individual\n'
            'creator.create(\'FitMax\', base.Fitness, weights=(1.0,))\n'
            'creator.create(\'Individual\', list, fitness=creator.FitMax,\n'
            '               *{6})\n'

            '# register functions\n'
            'self.toolbox.register(\'{2}\', {3}, *{4})\n'
            'self.toolbox.register(\'individual\', tools.initRepeat,\n'
            '                      creator.Individual,\n'
            '                      self.toolbox.{2}, {7})\n'
            'self.toolbox.register(\'population\', tools.initRepeat, list,\n'
            '                      self.toolbox.individual)\n'

            '# register genetic operations\n'
            'self.toolbox.register(\'evaluate\', {5})\n'
            'self.toolbox.register(\'mate\', tools.cxTwoPoint)\n'
            'self.toolbox.register(\'mutate\', tools.mutFlipBit, indpb=0.05)\n'
            'self.toolbox.register(\'select\', tools.selTournament,\n'
            '                      tournsize=3)\n'
        ).format(population, generations, funcname, fitfunc, args, evalfunc,
                 indidividual_attrs, repeat_func)

        # compile and execute
        compiled_setup = compile(self.setup, '<string>', 'exec')
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

    def evalOneMax(self, individual):
        '''
        Function to evaluate fitness of individuals in onemax problem.
        '''
        return sum(individual),

    def main(self):
        '''
        Function to run Genetic Algorithm.
        '''
        # initial population
        pop = self.toolbox.population(self.psize)

        # get fitnesses of population
        fitnesses = list(map(self.toolbox.evaluate, pop))

        # assign fitness to individual in population
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        # evolve population
        for g in range(self.gensize):
            offspring = algorithms.varAnd(pop, self.toolbox, cxpb=0.5,
                                          mutpb=0.1)
            fits = self.toolbox.map(self.toolbox.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
            pop = self.toolbox.select(offspring, k=len(pop))

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
