## @file net.py
#  @author Mark Vecsernyes
#
#  @brief Ez a fájl tartalmazza a neurális hálót
#  @{ 

## A szükséges könyvtárak importálása
import torch
from torch import autograd, nn
import torch.nn.functional as F

## Neurális hálók generálása
def generateNet(hidden):
	return Net(input_size=3, hidden_size=hidden, num_classes=1)

## Neurális háló leíró osztálya
class Net(nn.Module):
    ## Konstruktor
    #  @param input size integer bemeneti adatok száma
    #  @param hidden size integer rejtett réteg száma
    #  @param integer osztályok száma
    def __init__(self, input_size, hidden_size, num_classes):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size) 
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)  
    
    ##Forward metódus
    #  @param x input_size méretű float elemeket tartalmazó lista
    #  @paramt out float a neurális háló futásának eremdénye 
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

##  @} 

