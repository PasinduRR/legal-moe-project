import os
import sys
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
import json

# Add src directory to path to allow for imports from src
if __package__ is None:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from moe.gating_network import GatingNetwork
from experts.expert import Expert

def moe_retrieve(query, subdomains, base_dir, gating_model_path):
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = embedding_model.encode(query)
    query_tensor = torch.tensor(query_embedding, dtype=torch.float32)
    input_dim = query_tensor.shape[0]
    
    # Load gating network
    gating = GatingNetwork(input_dim, len(subdomains))
    gating.load_state_dict(torch.load(gating_model_path))
    gating.eval()
    
    gate_probs = gating(query_tensor.unsqueeze(0)).detach().numpy()[0]
    print(f"Subdomains: {subdomains}")
    print(f"Gating probabilities: {gate_probs}")
    
    # Load experts and compute similarities
    results = []
    for i, subdomain in enumerate(subdomains):
        model = Expert(input_dim)
        # Corrected path for expert model
        expert_model_path = os.path.join(base_dir, subdomain, "expert_model_similarity.pt")
        model.load_state_dict(torch.load(expert_model_path))
        model.eval()
        
        expert_query_vec = model(query_tensor.unsqueeze(0)).detach().numpy()[0]
        
        folder = os.path.join(base_dir, subdomain)
        for fname in os.listdir(folder):
            if fname.endswith(".embedding.npy"):
                section_emb = np.load(os.path.join(folder, fname))
                section_tensor = torch.tensor(section_emb, dtype=torch.float32)
                section_vec = model(section_tensor.unsqueeze(0)).detach().numpy()[0]
                
                # Cosine similarity
                similarity = np.dot(expert_query_vec, section_vec) / (np.linalg.norm(expert_query_vec) * np.linalg.norm(section_vec))
                
                weighted_score = gate_probs[i] * similarity
                results.append((subdomain, fname, weighted_score))
                
    results.sort(key=lambda x: -x[2])
    return results[:5]

if __name__ == '__main__':
    from moe_inference import moe_retrieve
    subdomains = ["company_law", "tax_law", "banking_law", "securities_law", "insolvency_law",
    "contract_law", "negotiable_instruments_law", "consumer_law", "ip_law",
    "arbitration_law", "trust_law", "electronic_transactions_law", "foreign_exchange_law"]  # List of subdomain names
    results = moe_retrieve(
        query="what is contract law?",
        subdomains=subdomains,
        base_dir="data/subdomains/",
        gating_model_path="data/gating_network.pt"
    )
    for subdomain, fname, score in results:
        print(f"{subdomain}: {fname} (score: {score:.4f})")