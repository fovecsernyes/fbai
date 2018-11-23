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
    #print(TEST: net generate_net( ) called)
	return Net(input_size=3, hidden_size=hidden)


## Class of neural networks
class Net(nn.Module):
    ## Constructor
    #  @param input_size integer
    #  @param hidden_size integer
    #  @param num_classes integer
    def __init__(self, input_size, hidden_size):
        #print(TEST: net __init__( ) called)
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size) 
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, 1)  


    ##Forward method
    #  @param x input vector
    #  @return out
    def forward(self, x):
        #print(TEST: net forward( ) called)
        out = self.relu(self.fc1(x))
        out = self.fc2(out)
        return out

##  @} 

