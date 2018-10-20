#this file contains the neural network

import torch
from torch import autograd, nn
import torch.nn.functional as F

#generating random neural networks
def generateNet():
	return Net(input_size=3, hidden_size=4, num_classes=1)

#class for neural network
class Net(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.h1 = nn.Linear(input_size, hidden_size)
        self.h2 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        x = self.h1(x)
        x = F.sigmoid(x)
        x = self.h2(x)
        return x

