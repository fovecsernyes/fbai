from database import Database

def geneticAlgorithm(database):
    print("genetic algorithm called")
    selection(database)
    crossover(database)
    mutation(database)
    return

def selection(database):
    print("\t*selection called")

def crossover(database):
    print("\t*crossover called")

def mutation(database):
    print("\t*mutation called")