## @file net.py
#  @author Mark Vecsernyes
#
#  @brief This file contains the neural network
#  @{ 

## AImport modules
import torch
from torch import autograd, nn
import torch.nn.functional as F

## Generate nets
def generate_net(hidden):
	return Net(input_size=3, hidden_size=hidden, num_classes=1)

## Class of neural networks
class Net(nn.Module):
    ## Constructor
    #  @param input_size integer
    #  @param hidden_size integer
    #  @param num_classes integer
    def __init__(self, input_size, hidden_size, num_classes):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size) 
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)  
    
    ##Forward method
    #  @param x input vector
    #  @return out
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

##  @} 

