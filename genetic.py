## @file genetic.py
#  @author Mark Vecsernyes
#
#  @brief Ez a fájl tartalmazza az evoluciós algoritmust
#  @{ 

## A szükséges könyvtárak importálása
from database import Database
from net import *
import _pickle as pickle
import random

#disable request messages
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

## geneticAlgorithm metódus: ez az evolúciós algoritmus
#  Adabázisból kiolvassa a madár id-t, neurális hálót és a fitnes értéket
#  @param database Database adatbázis
#  @param population integer a populació mérete
#  @param hidden rejtett neuronok szama
#  @param selection kiválasztási ráta
#  @param deletion törlési ráta
#  @param crossover keresztezési ráta
#  @param mutation1 mutációs ráta a populáción
#  @param mutation2 mutációs ráta az egyeden
def geneticAlgorithm(database, population, hidden, selection, deletion, crossover, mutation1, mutation2):
    print("genetic algorithm called")

    birds_data = database.select_bird(population)
    fitness = database.select_fitness(population)
    sample = []

    j = 0
    for i in birds_data:
        sample.append( [ i[0], pickle.loads(i[1]), fitness[j][1] ] )
        j+=1

    sample.sort(key=lambda x: x[2], reverse=True)

    parents = selection_method(sample, population, selection)
    children = crossover_method(parents, population, crossover, deletion)
    mutated_children = mutation_method(children, mutation1, mutation2)
    sample = reinstate_method(mutated_children, sample)


    for i in sample:
        database.update_net( pickle.dumps( i[1]), i[0] )

    return

## Selection metódus: az evolúciós algoritmus kiválasztás része
#  veletlenszeru parokbol kivalasztja a jobbat, selection/population egeszresze darabot
#  @param sample = [madar_id, neuralis_halo, fitness]
#  @param selection kiválasztási ráta
#  @return parents = [madar_id, neuralis_halo, fitness]
def selection_method(sample, population, selection):
    print("\t*selection called")

    total = int( population * selection/100 )
    #versengo veletlensz
    parents = []
    for i in range(total):
        a = random.randint( 0, population-1 )
        b = random.randint( 0, population-1 )

        if sample[a][2] >= sample[b][2]:
            parents.append(sample[a])
        else:
            parents.append(sample[b])

    parents.sort(key=lambda x: x[2], reverse=True)

    return parents

## Crossover metódus: az evolúciós algoritmus keresztezés része
#  @param sample = [madar_id, neuralis_halo, fitness]
#  @return sample = [madar_id, neuralis_halo, fitness]
#  @param crossover keresztezési ráta
def crossover_method(parents, population, crossover, deletion):
    print("\t*crossover called")
    total = int( population - population * deletion/100 )

    print(parents[3][1])
    
    children = []
    for i in range(total):
        a = random.randint( 0, len(parents)-1 )
        b = random.randint( 0, len(parents)-1 )



    return parents

## Mutáció metódus: az evolúciós algoritmus mutáció része
#  @param sample = [madar_id, neuralis_halo, fitness]
#  @return sample = [madar_id, neuralis_halo, fitness]
#  @param mutation1 mutációs ráta a populáción
#  @param mutation2 mutációs ráta az egyeden
def mutation_method(sample, mutation1, mutation2):
    print("\t*mutation called")
    return sample

def reinstate_method(mutated_children, sample):
    print("\t*reinstate called")
    return sample

##  @} 