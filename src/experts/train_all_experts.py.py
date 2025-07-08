import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from expert import Expert  # Import your class
from pathlib import Path

subdomains = [
    "company_law", "tax_law", "banking_law", "securities_law", "insolvency_law",
    "contract_law", "negotiable_instruments_law", "consumer_law", "ip_law",
    "arbitration_law", "trust_law", "electronic_transactions_law", "foreign_exchange_law"
]

base_dir = "../../data/subdomains/"

def train_expert_for_subdomain(subdomain):
    csv_path = os.path.join(base_dir, subdomain, "train.csv")
    if not os.path.exists(csv_path):
        print(f"Training CSV not found for {subdomain}, skipping.")
        return

    df = pd.read_csv(csv_path)



    class LegalDataset(Dataset):
        def __init__(self, df):
            self.embeddings = []

            # correct project root: one level above src/
            project_root = Path(__file__).parent.parent

            for raw_path in df['embedding_path']:
                # normalize slashes
                p = Path(raw_path.replace("\\", "/"))

                # if relative, resolve from project root
                if not p.is_absolute():
                    p = (project_root / p).resolve()

                print(f"Loading: {p}")  # optional: debug
                self.embeddings.append(np.load(p))

            self.labels = df['label'].astype('category').cat.codes

        def __len__(self):
            return len(self.embeddings)

        def __getitem__(self, idx):
            return torch.tensor(self.embeddings[idx], dtype=torch.float32), torch.tensor(self.labels.iloc[idx], dtype=torch.long)


    dataset = LegalDataset(df)
    loader = DataLoader(dataset, batch_size=4, shuffle=True)

    input_dim = dataset[0][0].shape[0]
    output_dim = len(df['label'].unique())

    model = Expert(input_dim, output_dim)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    epochs = 10
    for epoch in range(epochs):
        for X_batch, y_batch in loader:
            optimizer.zero_grad()
            output = model(X_batch)
            loss = criterion(output, y_batch)
            loss.backward()
            optimizer.step()
        print(f"{subdomain} - Epoch {epoch+1}, Loss: {loss.item():.4f}")

    model_path = os.path.join(base_dir, subdomain, "expert_model.pt")
    torch.save(model.state_dict(), model_path)
    print(f"Model saved for {subdomain} at {model_path}")

for subdomain in subdomains:
    train_expert_for_subdomain(subdomain)
