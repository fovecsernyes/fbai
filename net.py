#this file contains the neural network

import torch
from torch import autograd, nn
import torch.nn.functional as F

#generating random neural networks
def generateNet():
	return Net(input_size=3, hidden_size=4, num_classes=1)

class Net(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size) 
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)  
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

