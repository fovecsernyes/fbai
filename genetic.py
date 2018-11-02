## @file genetic.py
#  @author Mark Vecsernyes
#
#  @brief Ez a fájl tartalmazza az evoluciós algoritmust
#  @{ 

## A szükséges könyvtárak importálása
from database import Database

## geneticAlgorithm metódus: ez az evolúciós algoritmus
#  @param database Database adatbázis
#  @param population integer a populació mérete
def geneticAlgorithm(database, population):
    print("genetic algorithm called")

    #TODO: read the current fitness scores and neural networks from the database
    #fitness, neural_networks = fitness_and_neural_networks_selection_from_database

    #fitness, neural_networks = selection(fitness, neural_networks)
    #fitness, neural_networks = crossover(fitness, neural_networks)
    #fitness, neural_networks = mutation(fitness, neural_networks)

    #TODO: write to database the updated neural networks
    return

## Selection metódus: az evolúciós algoritmus kiválasztás része
#  @param database Database
def selection(database):
    print("\t*selection called")

## Crossove metódus: az evolúciós algoritmus keresztezés része
#  @param database Database
def crossover(database):
    print("\t*crossover called")

## Mutáció metódus: az evolúciós algoritmus mutáció része
#  @param database Database
def mutation(database):
    print("\t*mutation called")

##  @} 