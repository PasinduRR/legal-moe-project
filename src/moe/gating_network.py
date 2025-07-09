import torch.nn as nn
import torch

class GatingNetwork(nn.Module):
    def __init__(self, input_dim, num_experts):
        super().__init__()
        self.fc = nn.Linear(input_dim, num_experts)
    def forward(self, x):
        return torch.softmax(self.fc(x), dim=-1)
