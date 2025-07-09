import os
import faiss
import pickle

def build_faiss_indices(base_dir):
    for subdomain in os.listdir(base_dir):
        folder = os.path.join(base_dir, subdomain)
        embeddings = []
        files = []
        for fname in os.listdir(folder):
            if fname.endswith('.embedding.npy'):
                emb = np.load(os.path.join(folder, fname))
                embeddings.append(emb)
                files.append(fname)
        embeddings = np.stack(embeddings)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        faiss.write_index(index, os.path.join(folder, 'faiss.index'))
        with open(os.path.join(folder, 'faiss_files.pkl'), 'wb') as f:
            pickle.dump(files, f)

import pandas as pd
import numpy as np

def create_similarity_pairs(base_dir, k=3, num_neg=3):
    for subdomain in os.listdir(base_dir):
        folder = os.path.join(base_dir, subdomain)
        index = faiss.read_index(os.path.join(folder, 'faiss.index'))
        with open(os.path.join(folder, 'faiss_files.pkl'), 'rb') as f:
            files = pickle.load(f)
        embeddings = [np.load(os.path.join(folder, fname)) for fname in files]
        pairs = []
        for i, emb in enumerate(embeddings):
            emb = np.expand_dims(emb, axis=0)
            D, I = index.search(emb, k + 1)
            for j in range(1, k+1):
                idx = I[0][j]
                pairs.append({'file1': os.path.join(folder, files[i]), 'file2': os.path.join(folder, files[idx]), 'label': 1})
            neg_indices = set(range(len(files))) - set(I[0][:k+1])
            neg_indices = list(neg_indices)
            np.random.shuffle(neg_indices)
            for j in range(num_neg):
                idx = neg_indices[j]
                pairs.append({'file1': os.path.join(folder, files[i]), 'file2': os.path.join(folder, files[idx]), 'label': 0})
        df = pd.DataFrame(pairs)
        df.to_csv(os.path.abspath(os.path.join(folder, 'pairs.csv'), index=False))
