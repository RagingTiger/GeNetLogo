#!/usr/bin/env python

'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Program: genalgo
Description:
    Module for implementing genetic algorithm using NetLogo instance running on
    a Java virtual machine as the fitness function.
'''

# libraries
import random
from deap import creator, base, tools
import jvm

# creating simulations individual
creator.create('FitMax', base.Fitness, weights=(1.0,))
creator.create('SimulationCell', list, fitness=creator.FitMax,
               params=dict)

# create toolbox
toolbox = base.Toolbox()

# register functions
toolbox.register('attr_bool', random.randint, 0, 1)
toolbox.register('simcell', tools.initRepeat, creator.SimulationCell,
                 toolbox.attr_bool, 100)
toolbox.register('population', tools.initRepeat, list, toolbox.simcell)


# define evaluation function
def eval_fit(individual):
    return sum(individual)


# executable
if __name__ == '__main__':

    # print
    print 'Starting Genetic Algorithm ...'
