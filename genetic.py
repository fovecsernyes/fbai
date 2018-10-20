#this file manages the Genetic algorithm

from database import Database

#genetic algorithm
def geneticAlgorithm(database):
    print("genetic algorithm called")
    selection(database)
    crossover(database)
    mutation(database)
    return

#selection part of genetic algorithm
def selection(database):
    print("\t*selection called")

#crossover part of genetic algorithm
def crossover(database):
    print("\t*crossover called")

#mutation part of genetic algorithm
def mutation(database):
    print("\t*mutation called")