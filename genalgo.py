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
    genalgo base <population> <generations>
'''

# libraries
import random
from deap import creator, base, tools, algorithms


# classes
class GenAlgo(object):
    '''
    Class used as base class by other Genetic Algorithm classes.
    '''
    # constructor
    def __init__(self, population, generations, funcname, fitfunc, evalfunc):

        # meta programming
        self.setup = (
            '# initialize data\n'
            'self.toolbox = base.Toolbox()\n'
            'self.psize = {0}\n'
            'self.gensize = {1}\n'

            '# creating simulations individual\n'
            'creator.create(\'{2}\', {3}, weights=(1.0,))\n'
            'creator.create(\'Individual\', list, fitness=creator.{2},\n'
            '               params=dict)\n'

            '# register functions\n'
            'self.toolbox.register(\'attr_bool\', random.randint, 0, 1)\n'
            'self.toolbox.register(\'individual\', tools.initRepeat,\n'
            '                      creator.Individual,\n'
            '                      self.toolbox.attr_bool, 20)\n'
            'self.toolbox.register(\'population\', tools.initRepeat, list,\n'
            '                      self.toolbox.individual)\n'

            '# register genetic operations\n'
            'self.toolbox.register(\'evaluate\', {4})\n'
            'self.toolbox.register(\'mate\', tools.cxTwoPoint)\n'
            'self.toolbox.register(\'mutate\', tools.mutFlipBit, indpb=0.05)\n'
            'self.toolbox.register(\'select\', tools.selTournament,\n'
            '                      tournsize=3)\n'
        ).format(population, generations, funcname, fitfunc, evalfunc)

        # compile and execute
        compiled_setup = compile(self.setup, '<string>', 'exec')
        exec compiled_setup

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
        self.top_most_fit(pop, 10)

    def top_most_fit(self, pop, levels):
        '''
        Function print out the top most fit individuals in the population.
        '''
        # print out banner
        print 'Top {0} Most Fit Inviduals in Population:'.format(levels)

        # print out ranked individuals
        for i, ind in enumerate(tools.selBest(pop, k=levels)):
            print '#{0}{2}Individual: {1}'.format(i+1, ind,
                                                  ' '*(5-len(str(i+1))))


class OneMax(GenAlgo):
    '''
    Class to demonstrate onemax problem in DEAP.
    Attribution: http://deap.readthedocs.io/en/master/examples/ga_onemax.html
    '''
    # constructor
    def __init__(self, pops, gens):
        # call base class constructor
        GenAlgo.__init__(self, pops, gens, 'FitnessMax', 'base.Fitness',
                         'self.evalOneMax')

    def evalOneMax(self, individual):
        '''
        Function to evaluate fitness of individuals in onemax problem.
        '''
        return sum(individual),


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

    elif args['base']:
        print start
        p = int(args['<population>'])
        g = int(args['<generations>'])
        ga = GenAlgo(p, g, 'FitnessMax', 'base.Fitness', 'self.evalOneMax')
        ga.main()
