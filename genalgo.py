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
    genalgo <population> <generations>
'''

# libraries
import random
from deap import creator, base, tools, algorithms
import jvm


# classes
class OneMax(object):
    '''
    Class to demonstrate onemax problem in DEAP.
    '''
    # constructor
    def __init__(self, population, generations):

        # initialize data
        self.toolbox = base.Toolbox()
        self.psize = population
        self.gensize = generations

        # creating simulations individual
        creator.create('FitMax', base.Fitness, weights=(1.0,))
        creator.create('SimulationCell', list, fitness=creator.FitMax,
                       params=dict)

        # register functions
        self.toolbox.register('attr_bool', random.randint, 0, 1)
        self.toolbox.register('simcell', tools.initRepeat,
                              creator.SimulationCell, self.toolbox.attr_bool,
                              20)
        self.toolbox.register('population', tools.initRepeat, list,
                              self.toolbox.simcell)

        # register genetic operations
        self.toolbox.register("evaluate", self.eval_fit)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def eval_fit(self, individual):
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
        print tools.selBest(pop, k=10)


# executable
if __name__ == '__main__':

    # exectuable only imports
    from docopt import docopt

    # check CLA
    args = docopt(__doc__)

    # print
    print 'Starting Genetic Algorithm ...'
    ga = OneMax(int(args['<population>']), int(args['<generations>']))
    ga.main()
