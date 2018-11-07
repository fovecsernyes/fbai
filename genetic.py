## @file genetic.py
#  @author Mark Vecsernyes
#
#  @brief Ez a fájl tartalmazza az evoluciós algoritmust
#  @{ 

## A szükséges könyvtárak importálása
from database import Database
from net import *
import _pickle as pickle

## geneticAlgorithm metódus: ez az evolúciós algoritmus
#  Adabázisból kiolvassa a madár id-t, neurális hálót és a fitnes értéket
#  @param database Database adatbázis
#  @param population integer a populació mérete
def geneticAlgorithm(database, population):
    print("genetic algorithm called")

    birds_data = database.select_bird(population)
    fitness = database.select_fitness(population)
    sample = []

    j = 0
    for i in birds_data:
        sample.append( [ i[0], pickle.loads(i[1]), fitness[j][1] ] )
        j+=1

    sample.sort(key=lambda x: x[2])

    sample = selection(sample)
    sample = crossover(sample)
    sample = mutation(sample)

    for i in sample:
        database.update_net( pickle.dumps( i[1]), i[0] )

    return

## Selection metódus: az evolúciós algoritmus kiválasztás része
#  @param neural_networks listák listája a madár azonosítójával és neurális hálójával
#  @param sample = [madar_id, neuralis_halo, fitness]
#  @return sample = [madar_id, neuralis_halo, fitness]
def selection(sample):
    print("\t*selection called")
    return sample

## Crossover metódus: az evolúciós algoritmus keresztezés része
#  @param sample = [madar_id, neuralis_halo, fitness]
#  @return sample = [madar_id, neuralis_halo, fitness]
def crossover(sample):
    print("\t*crossover called")
    return sample

## Mutáció metódus: az evolúciós algoritmus mutáció része
#  @param sample = [madar_id, neuralis_halo, fitness]
#  @return sample = [madar_id, neuralis_halo, fitness]
def mutation(sample):
    print("\t*mutation called")
    return sample

##  @} 