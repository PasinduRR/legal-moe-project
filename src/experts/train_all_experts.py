import os
import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from expert import Expert

base_dir = "data/subdomains/"
subdomains = os.listdir(base_dir)

def train_expert_for_subdomain(subdomain):
    csv_path = os.path.join(base_dir, subdomain, "train.csv")
    df = pd.read_csv(csv_path)
    class LegalDataset(Dataset):
        def __init__(self, df):
            self.embeddings = []
            for rel_path in df['embedding_path']:
                # Remove leading ../ if it exists
                rel_path = rel_path.lstrip("./").lstrip("../")
                # Replace backslashes with slashes (Windows)
                rel_path = rel_path.replace("\\", "/")
                full_path = os.path.join(os.getcwd(), rel_path)
                if not os.path.exists(full_path):
                    raise FileNotFoundError(f"File not found: {full_path}")
                self.embeddings.append(np.load(full_path))

            self.labels = df['label'].astype('category').cat.codes
        def __len__(self):
            return len(self.embeddings)
        def __getitem__(self, idx):
            return (
                torch.tensor(self.embeddings[idx], dtype=torch.float32),
                torch.tensor(self.labels.iloc[idx], dtype=torch.long)
            )
            
    dataset = LegalDataset(df)
    loader = DataLoader(dataset, batch_size=4, shuffle=True)
    input_dim = dataset[0][0].shape[0]
    output_dim = len(df['label'].unique())
    model = Expert(input_dim, output_dim)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = torch.nn.CrossEntropyLoss()
    for epoch in range(10):
        for X_batch, y_batch in loader:
            optimizer.zero_grad()
            output = model(X_batch)
            loss = criterion(output, y_batch)
            loss.backward()
            optimizer.step()
        print(f"{subdomain} - Epoch {epoch+1}, Loss: {loss.item():.4f}")
    torch.save(model.state_dict(), os.path.join(base_dir, subdomain, "expert_model.pt"))
    print(f"Model saved for {subdomain}")

for subdomain in subdomains:
    train_expert_for_subdomain(subdomain)
