#!/usr/bin/env python

'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Description:
    Module for implementing genetic algorithm using NetLogo instance running on
    a Java virtual machine as the fitness function.
Documentation: http://deap.readthedocs.io/en/master/
Usage:
    genetalgo <population>
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

# register genetic operations
toolbox.register("evaluate", eval_fit)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


def main(pval):
    '''
    Function to run Genetic Algorithm.
    '''
    # initial population
    pop = toolbox.population(n=int(pval))


# executable
if __name__ == '__main__':

    # exectuable only imports
    from docopt import docopt

    # check CLA
    args = docopt(__doc__)

    # print
    print 'Starting Genetic Algorithm ...'
    main(args['<population>'])
