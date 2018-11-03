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
#  @param database Database adatbázis
#  @param population integer a populació mérete
def geneticAlgorithm(database, population):
    print("genetic algorithm called")

    birds_data = database.select_bird(population)
    fitness = database.select_fitness(population)
    sample = []

    j = 0
    for i in birds_data:
        sample.append( [ i[0], generateNet(), fitness[j][1] ] )
        sample[j][1].load_state_dict( pickle.loads(i[1]) )
        j+=1

    sample = selection(sample)
    sample = crossover(sample)
    sample = mutation(sample)

    #TODO: write to database the updated neural networks (dont forget to pickle dump)
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