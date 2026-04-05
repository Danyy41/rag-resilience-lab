import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def load_documents(data_path):
    docs = []
    filenames = []

    for file in os.listdir(data_path):
        if file.endswith(".txt"):
            with open(os.path.join(data_path, file), "r", encoding="utf-8") as f:
                docs.append(f.read())
                filenames.append(file)

    return docs, filenames

def build_index(data_path="../data/clean"):
    docs, filenames = load_documents(data_path)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(docs)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings, dtype="float32"))

    return index, model, docs, filenames