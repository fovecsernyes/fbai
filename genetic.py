## @file genetic.py
#  @author Mark Vecsernyes
#
#  @brief Ez a fájl tartalmazza az evoluciós algoritmust
#  @{ 

## A szükséges könyvtárak importálása
from database import Database
from net import *
import _pickle as pickle

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

    sample = selection_method(sample, selection, deletion, hidden)
    sample = crossover_method(sample, crossover)
    sample = mutation_method(sample, mutation1, mutation2)

    for i in sample:
        database.update_net( pickle.dumps( i[1]), i[0] )

    return

## Selection metódus: az evolúciós algoritmus kiválasztás része
#  @param neural_networks listák listája a madár azonosítójával és neurális hálójával
#  @param sample = [madar_id, neuralis_halo, fitness]
#  @param selection kiválasztási ráta
#  @param deletion törlési ráta
#  @param hidden rejtett neuronok szama
#  @return sample = [madar_id, neuralis_halo, fitness]
def selection_method(sample, selection, deletion, hidden):
    print("\t*selection called")
    for i in sample:
        print(str(i[0]) + '     ' + str(i[2]))
    return sample

## Crossover metódus: az evolúciós algoritmus keresztezés része
#  @param sample = [madar_id, neuralis_halo, fitness]
#  @return sample = [madar_id, neuralis_halo, fitness]
#  @param crossover keresztezési ráta
def crossover_method(sample, crossover):
    print("\t*crossover called")
    return sample

## Mutáció metódus: az evolúciós algoritmus mutáció része
#  @param sample = [madar_id, neuralis_halo, fitness]
#  @return sample = [madar_id, neuralis_halo, fitness]
#  @param mutation1 mutációs ráta a populáción
#  @param mutation2 mutációs ráta az egyeden
def mutation_method(sample, mutation1, mutation2):
    print("\t*mutation called")
    return sample

##  @} 