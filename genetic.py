## @file genetic.py
#  @author Mark Vecsernyes
#
#  @brief This file contains the genetic algorithm
#  @{ 

## Import modules
from database import Database
from net import *
import _pickle as pickle
import random
from collections import OrderedDict
import numpy


## Genetic algorithm method
#  Reads the neural networks from database and modifies them and writes them back
#  @param database Database
#  @param population integer 
#  @param hidden integer hidden neurons
#  @param selection integer selection rate
#  @param deletion integer deletion rate
#  @param crossover integer crossover rate
#  @param mutation1 integer mutation rate of all birds
#  @param mutation2 integer mutation rate on entity
def genetic_algorithm(database, population, hidden, selection, deletion, crossover, mutation1, mutation2):
    birds_data = database.select_bird(population)
    fitness = database.select_fitness(population)
    sample = []

    j = 0
    for i in birds_data:
        sample.append( [ i[0], pickle.loads(i[1]), fitness[j][1] ] )
        j+=1

    #sorting by fitness
    sample.sort(key=lambda x: x[2], reverse=True)

    #selection evolution operator
    parents = selection_method(sample, population, selection)
    #crossover evolution operator
    children = crossover_method(parents, population, crossover)
    #mutation evolution operator
    children = mutation_method(children, population, hidden, mutation1, mutation2)
    #reinsertation evolution operator
    sample = reinsertion_method(children, sample, population, hidden, deletion)

    #update the new neural networks in database
    for i in sample:
        database.update_net( pickle.dumps( i[1]), i[0] )

    return


## Selection method
#  select (population * (selection/100) birds from the best of random pairs
#  @param sample = [bird_id, neural_network, fitness]
#  @param population integer
#  @param selection integer
#  @return parents [net, .., net]
def selection_method(sample, population, selection):
    total = int( population * selection/100 )
    parents = []

    for i in range(total):
        a = random.randint( 0, population-1 )
        b = random.randint( 0, population-1 )

        if sample[a][2] >= sample[b][2]:
            parents.append(sample[a][1])
        else:
            parents.append(sample[b][1])

    return parents


## Crossover method makes (population * crossover/100) children of the parents
#  by randomly mixing their matrices
#  @param parents [net, .., net]
#  @param population integer
#  @param crossover integer
#  @return [net, .. , net]
def crossover_method(parents, population, crossover):
    total = int(population * crossover/100) 

    children = []
    for i in range(total):
        a = random.randint( 0, len(parents)-1 )
        b = random.randint( 0, len(parents)-1 )

        r0, r1, r2, r3 = make_matrix(parents[a])
        q0, q1, q2, q3 = make_matrix(parents[b])

        pos = [random.randint(0, len(x)) for x in [r0, r1]]
        r0[:pos[0]] = q0[:pos[0]]
        r1[:pos[1]] = q1[:pos[1]]

        if random.randint(0, 1) == 0:
            r2 = q2
        if random.randint(0, 1) == 0:
            r3 = q3

        children.append( make_odict(r0, r1, r2, r3) )
        
    return children


## Mutation method mutates the children by modifying a a random value
#  @param childen integer
#  @population integer
#  @hidden integer
#  @param mutation1 integer
#  @param mutation2 integer
#  @return [net, .., net]
def mutation_method(children, population, hidden, mutation1, mutation2):
    total = int(population * mutation1/100)
    for i in range(total):
        pos = random.randint( 0, len(children)-1 )
        r0, r1, r2, r3 = make_matrix(children[pos])
        rows = 0
        for x in [r0, r1, r2, r3]:
            rows+=len(x)
        rate = int( rows * mutation2/100)

        for j in range(rate):
            where = random.randint( 0, 3 )
            if where == 0:
                r = random.randint( 0, hidden-1 )
                q = random.randint( 0, 2 )
                r0[r][q] = random.uniform(-1, 1)

            elif where == 1:
                r = random.randint( 0, hidden-1 )
                r1[r] = random.uniform(-1, 1)

            elif where == 2:
                r = random.randint( 0, hidden-1 )
                r2[0][r] = random.uniform(-1, 1)
            else:
                r3[0] = random.uniform(-1, 1)

        children[pos] = make_odict(r0, r1, r2, r3)

    return children


## Reinertion method inserts new birds into the population
#  population - len(children) - deletion remains
# range(start, population-deletion-1) replaces
#  deletion generates
#  @param sample = [bird_id, neural_network, fitness]
#  @param population integer 
#  @param hidden integer
#  @param deletion integer
#  @return sample = [bird_id, neural_network, fitness]
def reinsertion_method(children, sample, population, hidden, deletion):
    start = population - len(children) - deletion

    for i in range(start, population-deletion-1):
        sample[i][1] = children[i-start]

    for j in range(population-deletion, population):
        sample[j][1] = generate_net(hidden).state_dict()

    sample.sort(key=lambda x: x[0])

    return sample


## Makes 4 matrices from OrederedDictionary
#  @param odict OrderedDictionary
#  @return r0, r1, r2, r3 numpy arrays
def make_matrix(odict):
    dict_list = list( odict.items() )
    r0 = dict_list[0][1].numpy()
    r1 = dict_list[1][1].numpy()
    r2 = dict_list[2][1].numpy()
    r3 = dict_list[3][1].numpy()

    return r0, r1, r2, r3


## Makes OrderedDicttionary from 4 matrices
#  @param r0 numpy array
#  @param r1 numpy array
#  @param r2 numpy array
#  @param r3 numpy array
#  return OrderedDicttionary
def make_odict(r0, r1, r2, r3):
    return OrderedDict([('fc1.weight', torch.from_numpy(r0)),
                        ('fc1.bias', torch.from_numpy(r1)),
                        ('fc2.weight', torch.from_numpy(r2)),
                        ('fc2.bias', torch.from_numpy(r3))])



##  @} 