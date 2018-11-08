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
from collections import OrderedDict
import numpy

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
def genetic_algorithm(database, population, hidden, selection, deletion, crossover, mutation1, mutation2):
    birds_data = database.select_bird(population)
    fitness = database.select_fitness(population)
    sample = []

    j = 0
    for i in birds_data:
        sample.append( [ i[0], pickle.loads(i[1]), fitness[j][1] ] )
        j+=1

    sample.sort(key=lambda x: x[2], reverse=True)

    parents = selection_method(sample, population, selection)
    children = crossover_method(parents, population, crossover)
    children = mutation_method(children, population, hidden, mutation1, mutation2)
    sample = reinsertion_method(children, sample, population, hidden, deletion)

    for i in sample:
        database.update_net( pickle.dumps( i[1]), i[0] )

    return

## Selection metódus: az evolúciós algoritmus kiválasztás része
#  veletlenszeru parokbol kivalasztja a jobbat, population * selection/100 egeszresze darabot, de az elso 3-at mindekepp
#  @param sample = [madar_id, neuralis_halo, fitness]
#  @param population a populáció mérete
#  @param selection kiválasztási ráta
#  @return parents a neurális hálók listája OrderedDictionary formátumban
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

## Crossover metódus: az evolúciós algoritmus keresztezés része
#  population * crossover/100 db utodot hozunk letre
#  @param parents a neurális hálók listája OrderedDict formátumban
#  @param population a populáció mérete
#  @param crossover keresztezési ráta
#  @return neurális hálók listája OrderedDictionary formátumban
def crossover_method(parents, population, crossover):
    total = int(population * crossover/100) 

    children = []
    asd = generate_net(6)
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

        #TODO FIX the neural net changes after runs
        #asd.load_state_dict( children[0] )
        #input = autograd.Variable(torch.tensor([float(10), float(20), float(30)]))
        #out = asd(input)
        #print(float(out))
    
    return children

## Mutáció metódus: az evolúciós algoritmus mutáció része
#  @param children neurális halók listája
#  @population populacio merete
#  @hidden rejtett neuronok száma
#  @param mutation1 mutációs ráta a populáción
#  @param mutation2 mutációs ráta az egyeden
#  @return mutated_childer nuralis halok
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
                r0[r] *= random.uniform(-1, 1)
            elif where == 1:
                r = random.randint( 0, hidden-1 )
                r1[r] *= random.uniform(-1, 1)
            elif where == 2:
                r2 *= random.uniform(-1, 1)
            else:
                r3 *= random.uniform(-1, 1)

        children[pos] = make_odict(r0, r1, r2, r3)

    return children

def reinsertion_method(children, sample, population, hidden, deletion):
    start = population - len(children) - deletion

    for i in range(start, population-deletion-1):
        sample[i][1] = children[i-start]

    for j in range(population-deletion, population):
        sample[j][1] = generate_net(hidden).state_dict()

    sample.sort(key=lambda x: x[0])

    return sample

## OrederedDict típusból 4 mátrixot készít
#  @param odict OrderDictionary
#  @return r0, r1, r2, r3 numpy tömbök
def make_matrix(odict):
    dict_list = list( odict.items() )
    r0 = dict_list[0][1].numpy()
    r1 = dict_list[1][1].numpy()
    r2 = dict_list[2][1].numpy()
    r3 = dict_list[3][1].numpy()

    return r0, r1, r2, r3

## 4 tömbből egy Ordereddict típust készít
#  @param r0, r1, r2, r3 tömbök
#  return OrderedDicttionary
def make_odict(r0, r1, r2, r3):
    return OrderedDict([('fc1.weight', torch.from_numpy(r0)),
                        ('fc1.bias', torch.from_numpy(r1)),
                        ('fc2.weight', torch.from_numpy(r2)),
                        ('fc2.bias', torch.from_numpy(r3))])












##  @} 