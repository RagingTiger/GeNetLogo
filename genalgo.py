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
import deap
import jvm

# creating simulations individual
deap.creator.create('FitMax', deap.base.Fitness, weights=(1.0,))
deap.creator.create('SimulationCell', list, fitness=creator.FitMax,
                    params=dict)

# crate toolbox
toolbox = deap.base.Toolbox()

# register functions
toolbox.register('attr_bool', random.randint, 0, 1)
toolbox.register('simcell', deap.tools.initRepeat, deap.creator.SimulationCell,
                 toolbox.attr_bool, 100)
toolbox.register('population', deap.tools.initRepeat, list, toolbox.simcell)


# define evaluation function
def eval_fit(individual):
    return sum(individual)


# executable
if __name__ == '__main__':

    # print
    print 'under construction'
