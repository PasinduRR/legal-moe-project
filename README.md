# Legal MoE AI: A Mixture of Experts System for Semantic Legal Document Retrieval

## 1. Project Overview

This project implements a sophisticated Mixture of Experts (MoE) model designed for the intelligent retrieval of legal documents. By leveraging specialized "expert" models for different subdomains of law (e.g., Company Law, Tax Law, Banking Law), the system can provide highly relevant search results from a large corpus of legal texts. A top-k gating network routes user queries to the most appropriate experts, ensuring both accuracy and efficiency.

### Key Features

*   **Modular Architecture:** Each legal domain is handled by a dedicated expert model, making the system scalable and easy to maintain.
*   **Semantic Search:** Utilizes state-of-the-art sentence transformers to understand the meaning behind legal queries, going beyond simple keyword matching.
*   **Intelligent Routing:** A trainable top-k gating network dynamically selects the most relevant expert(s) for a given query, improving retrieval accuracy.
*   **End-to-End Pipeline:** Includes comprehensive scripts for data preparation, text extraction, model training, and final inference.
*   **Similarity-Based Learning:** Experts are trained using contrastive loss to learn meaningful representations, enabling them to identify semantically similar legal clauses.

## 2. Project Structure

The project is organized into a modular structure to separate data, source code, and notebooks.

legal-moe-project/
├── data/                       # All datasets and model outputs
│   ├── gating_queries/         # .npy embeddings of queries used to train the gating network
│   ├── raw_pdfs/               # Original legal PDFs, organized by Act
│   ├── subdomains/             # Processed data, organized by legal subdomain
│   │   ├── company_law/            # Example subdomain folder
│   │   │   ├── *.cleaned.txt          # Cleaned text sections
│   │   │   ├── *.embedding.npy       # Vector embeddings of sections
│   │   │   ├── pairs.csv             # Positive/negative training pairs for expert
│   │   │   ├── faiss.index           # FAISS index for similarity search
│   │   │   ├── faiss_files.pkl       # Mapping of files in FAISS index
│   │   │   └── expert_model_similarity.pt # Trained expert model weights
│   │   └── ...                   # Other legal subdomains follow similar structure
│   ├── gating_network.pt        # Trained weights of the gating network
│   ├── gating_train.csv         # Training data for gating network (queries & labels)
│   └── subdomain_map.json       # Maps human-readable subdomain names to labels
│
├── notebooks/                   # Jupyter notebooks for data preparation and exploration
│   ├── extract_and_clean_sections.ipynb # Extract & clean text from PDFs
│   ├── embed_sections.ipynb            # Generate embeddings from cleaned text
│   └── build_faiss_and_pairs.ipynb    # Build FAISS indices & generate pairs
│
├── src/                         # Source code
│   ├── experts/                     # Expert model components
│   │   ├── expert.py                    # Expert model architecture
│   │   ├── contrastive_loss.py         # Contrastive loss definition
│   │   └── train_expert_similarity.py  # Script to train all expert models
│   ├── moe/                         # Mixture of Experts components
│   │   ├── gating_network.py           # Gating network architecture
│   │   ├── train_gating_network.py     # Script to train gating network
│   │   └── moe_inference.py            # Inference pipeline combining gating & experts
│   └── utils.py                    # Utility functions
│
├── tests/                       # Unit and integration tests
│
├── query_moe.py                 # Script to run a query through the trained MoE system
├── README.md                    # Project documentation (this file)
└── requirements.txt             # Python dependencies


## 3. Setup and Installation

Follow these steps to set up the project environment.

### 3.1. Clone the Repository

git clone <your-repository-url>
cd legal-moe-project

### 3.2. Create and Activate a Virtual Environment

Create the environment
python -m venv venv

Activate it (on Windows)
venv\Scripts\activate

Activate it (on macOS/Linux)
source venv/bin/activate

### 3.3. Install Dependencies

First, create a `requirements.txt` file with the following content:
torch
pandas
numpy
sentence-transformers
spacy
scikit-learn
jupyter
faiss-cpu
pdfplumber

Then, install the packages:
pip install -r requirements.txt
python -m spacy download en_core_web_sm

## 4. End-to-End Workflow

### Step 1: Data Preparation
1.  **Place PDFs:** Put your sectioned PDFs into the `data/raw_pdfs/` directory. Each original act should have its own subfolder containing its section PDFs.
2.  **Extract & Clean Text:** Use the `notebooks/extract_and_clean_sections.ipynb` to process the PDFs. This script will:
    *   Read each PDF from `data/raw_pdfs/`.
    *   Extract and clean the text.
    *   Save the cleaned text into the appropriate folder under `data/subdomains/`.

### Step 2: Generate Embeddings and Build Search Indices
1.  **Generate Embeddings:** Run the `notebooks/embed_sections.ipynb`. This notebook iterates through all `.cleaned.txt` files in `data/subdomains/` and generates a sentence-transformer embedding for each, saving it as a `.embedding.npy` file.
2.  **Build FAISS Index:** Run the `notebooks/build_faiss_and_pairs.ipynb`. This step:
    *   Creates a FAISS index for each subdomain, allowing for ultra-fast similarity searches.
    *   Saves the index as `faiss.index` in each subdomain folder.

### Step 3: Create Training Pairs for Experts
The `notebooks/build_faiss_and_pairs.ipynb` also handles this step. Using the FAISS index, it finds semantically similar and dissimilar pairs of sections within each subdomain and saves them to a `pairs.csv` file. This data is crucial for training the experts.

### Step 4: Train the Expert Models
The expert models are trained to understand the nuances of their specific legal domain.
*   **Run Training Script:**
    ```
    python src/experts/train_expert_similarity.py
    ```
*   **Output:** This script will train one expert model for each subdomain and save the trained weights as `expert_model_similarity.pt` inside each subdomain's folder.

### Step 5: Train the Gating Network
The gating network learns to route a user's query to the most relevant expert(s).
1.  **Prepare Training Data:** First, you need to create the `data/gating_train.csv` file. This involves creating a list of ~200 sample queries and manually assigning the correct `expert_label` to each. Then, generate embeddings for these queries.
2.  **Run the Training Script:**
    ```
    python src/moe/train_gating_network.py
    ```
*   **Output:** This saves the trained gating model to `data/gating_network.pt` and a label mapping to `data/subdomain_map.json`.

## 5. Running the MoE System for Inference

Once all models are trained, you can query the system using the main inference script.
*   **How to Run:**
    ```
    python query_moe.py
    ```
*   **Functionality:** This script takes a hardcoded query, loads the gating network and all expert models, routes the query to the top-k experts, retrieves the most relevant documents, and prints the final weighted results. You can easily modify the `my_query` variable in the script to ask your own questions.
