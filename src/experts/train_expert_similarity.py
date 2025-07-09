import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas as pd
import os
from expert import Expert
from contrastive_loss import ContrastiveLoss

class PairDataset(Dataset):
    def __init__(self, csv_path):
        df = pd.read_csv(csv_path)
        csv_dir = os.path.dirname(csv_path)
        pairs = []
        labels = []
        for i, row in df.iterrows():
            path1 = os.path.join(csv_dir, os.path.basename(row['file1']))
            path2 = os.path.join(csv_dir, os.path.basename(row['file2']))
            if not os.path.exists(path1):
                print(f"[WARNING] File not found: {path1} (skipping pair)")
                continue
            if not os.path.exists(path2):
                print(f"[WARNING] File not found: {path2} (skipping pair)")
                continue
            pairs.append((path1, path2))
            labels.append(row['label'])
        self.pairs = pairs
        self.labels = np.array(labels, dtype=np.float32)
        if len(self.pairs) == 0:
            print("[ERROR] No valid pairs found in dataset!")

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        path1, path2 = self.pairs[idx]
        emb1 = np.load(path1)
        emb2 = np.load(path2)
        label = self.labels[idx]
        return (torch.tensor(emb1, dtype=torch.float32),
                torch.tensor(emb2, dtype=torch.float32),
                torch.tensor(label, dtype=torch.float32))

def train_expert(subdomain):
    folder = os.path.join("data", "subdomains", subdomain)
    csv_path = os.path.join(folder, 'pairs.csv')
    if not os.path.exists(csv_path):
        print(f"[ERROR] pairs.csv not found for {subdomain}, skipping.")
        return
    dataset = PairDataset(csv_path)
    if len(dataset) == 0:
        print(f"[ERROR] No valid pairs for {subdomain}, skipping training.")
        return
    loader = DataLoader(dataset, batch_size=8, shuffle=True)
    input_dim = dataset[0][0].shape[0]
    model = Expert(input_dim)
    criterion = ContrastiveLoss(margin=1.0)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    epochs = 10
    for epoch in range(epochs):
        running_loss = 0.0
        for emb1, emb2, label in loader:
            optimizer.zero_grad()
            out1 = model(emb1)
            out2 = model(emb2)
            loss = criterion(out1, out2, label)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        avg_loss = running_loss / len(loader)
        print(f"{subdomain} - Epoch {epoch+1}, Loss: {avg_loss:.4f}")
    torch.save(model.state_dict(), os.path.join(folder, "expert_model_similarity.pt"))
    print(f"Model saved for {subdomain}")

subdomains = [d for d in os.listdir("data/subdomains/") if os.path.isdir(os.path.join("data/subdomains/", d))]
for subdomain in subdomains:
    print(f"\n=== Training expert for subdomain: {subdomain} ===")
    train_expert(subdomain)
