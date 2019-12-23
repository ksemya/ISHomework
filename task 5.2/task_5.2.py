import numpy
import random
import math

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

indNum=200
population = []

for i in range(indNum):
    individual=''
    for j in range(len(data)):
        individual+=str(random.randrange(2))
    population.append(individual)

def fitness(individual):
    weight = 0.0
    volume = 0.0
    value = 0.0
    for i in range(len(individual)):
        weight += int(individual[i])*weidhts[i]
        volume += int(individual[i])*volumes[i]
        value += int(individual[i])*values[i]
    if volume > maxVolume or weight > maxWeight:
        return maxWeight, maxVolume,  0           
    return weight, volume, value

def selection(population):
    sortedPop = sorted(population, key=  lambda i: fitness(i)[2], reverse=True)
    indForCross=[]
    for i in range(math.floor(len(sortedPop)*0.2)):
        indForCross.append(sortedPop[i])
    return indForCross

def crossingover(indForCross):
    children=[]
    for i in range(len(indForCross)):
        item1=''
        item2=''
        if i<len(indForCross)-i-1:
            for j in range(len(data)):
                if indForCross[i][j] == indForCross[len(indForCross)-i-1][j]:
                    bit=indForCross[i][j]
                    item1+=bit
                    item2+=bit
                else:
                    bit=random.randrange(2)
                    item1+=str(bit)
                    bit=random.randrange(2)
                    item2+=str(bit)
            children.append(item1)
            children.append(item2)
    return children

def mutation(children):
    for i in range(math.floor(len(children)*0.1)):
        index=random.randrange(len(children))
        if any(item ==0 for item in children[index]):
            changed=False
            while(not changed):
                bit=random.randrange(len(children[index]))
                if children[index][bit]==0:
                    children[index][bit]=1
                    changed=True
    return children

def createNewPopulation(population, children):
    indFit={}
    for individ in population:
        indFit[individ]=math.floor(fitness(individ)[2]*0.8)
    for child in children:
        indFit[child]=math.floor(fitness(child)[2])
    indSorted= sorted(indFit.items(), key=lambda item: item[1], reverse=True)
    newPopulation=[]
    for i in range(indNum):
        newPopulation.append(indSorted[i][0])
    return newPopulation

def solver(population):
    lastIterRes=0
    for i in range(500):
        selectedInd=selection(population)
        children=crossingover(selectedInd)
        mutChildren=mutation(children)
        population=createNewPopulation(population,mutChildren)
        bestIndivid=sorted(population, key=  lambda i: fitness(i)[2], reverse=True)[0]
        bestIndividFit=fitness(bestIndivid)[2]
        if abs(bestIndividFit-lastIterRes)<math.floor(bestIndividFit*0.1):
            return bestIndivid
        if i>0 and i%15==0:
            lastIterRes=bestIndividFit
    return bestIndivid
 
best=solver(population)
print("packed items")
for i in range(len(best)):
    if(best[i]=='1'):
        print(i, data[i])
print("total weight, volume, value")
print(fitness(best))