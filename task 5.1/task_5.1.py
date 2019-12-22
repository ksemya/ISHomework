import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

data=[]
weidhts=[]
volumes=[]
values=[]
file = open('15.txt')
for line in file:
    data.append(line.split())
maxVolume = float(data[0][1])
maxWeight = float(data[0][0])
del data[0]
for item in data:
    weidhts.append(float(item[0]))
    volumes.append(float(item[1]))
    values.append(float(item[2]))

NBR_ITEMS = len(data)
creator.create("Fitness", base.Fitness, weights=(-1.0,-1.0, 1.0))
creator.create("Individual", set, fitness=creator.Fitness)

items = {}
for i in range(NBR_ITEMS):
    items[i] = (weidhts[i],volumes[i], values[i])

toolbox = base.Toolbox()

## Attribute generator
toolbox.register("attr_item", random.randrange, 30)
## Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.attr_item, 30)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)



def evalKnapsack(individual):
    weight = 0.0
    volume = 0.0
    value = 0.0
    for item in individual:
        weight += items[item][0]
        volume += items[item][1]
        value += items[item][2]
    if volume > maxVolume or weight > maxWeight:
        return maxWeight, maxVolume,  0           
    return weight, volume, value

def cxSet(ind1, ind2):
    temp = set(ind1)                # Used in order to keep type
    ind1 &= ind2                    # Intersection (inplace)
    ind2 ^= temp                    # Symmetric Difference (inplace)
    return ind1, ind2

def mutSet(individual):
    individual.add(random.randrange(NBR_ITEMS))
    return individual,

toolbox.register("evaluate", evalKnapsack)
toolbox.register("mate", cxSet)
toolbox.register("mutate", mutSet)
toolbox.register("select", tools.selNSGA2)

def main():
    NGEN = 500
    MU = 200
    LAMBDA = 100
    CXPB = 0.2
    MUTPB = 0.1
    
    pop = toolbox.population(n=MU)
    stats = tools.Statistics(lambda val: val)
    stats.register("max", numpy.max, axis=0)
    
    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats)
    
if __name__ == "__main__":
    main()                 