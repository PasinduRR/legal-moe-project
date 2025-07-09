import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from gating_network import GatingNetwork
import numpy as np
import pandas as pd

class GatingDataset(Dataset):
    def __init__(self, csv_path):
        df = pd.read_csv(csv_path)
        df['query_embedding_path'] = df['query_embedding_path'].str.replace('../', '', regex=False)
        self.embeddings = [np.load(path) for path in df['query_embedding_path']]
        self.labels = df['expert_label'].astype('category').cat.codes
    def __len__(self):
        return len(self.embeddings)
    def __getitem__(self, idx):
        return torch.tensor(self.embeddings[idx], dtype=torch.float32), torch.tensor(self.labels[idx], dtype=torch.long)

input_dim = 384
num_experts = 13  # Adjust as needed
dataset = GatingDataset("data/gating_train.csv")
loader = DataLoader(dataset, batch_size=8, shuffle=True)
model = GatingNetwork(input_dim, num_experts)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()
epochs = 10
for epoch in range(epochs):
    for X, y in loader:
        optimizer.zero_grad()
        output = model(X)
        loss = criterion(output, y)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
torch.save(model.state_dict(), "data/gating_network.pt")
