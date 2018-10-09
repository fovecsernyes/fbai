import torch
from torch import autograd, nn
import torch.nn.functional as F

def generateNet():
	return Net(input_size=3, hidden_size=4, num_classes=1)


class Net(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.h1 = nn.Linear(input_size, hidden_size)
        self.h2 = nn.Linear(hidden_size, num_classes)
        print('Net init')

    def forward(self, x):
        x = self.h1(x)
        x = F.tanh(x)
        x = self.h2(x)
        return x
