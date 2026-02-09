import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(9, 128) # Board
        self.fc2 = nn.Linear(128, 128) # Hidden layer
        self.fc3 = nn.Linear(128, 9) # Possible Moves
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)
    