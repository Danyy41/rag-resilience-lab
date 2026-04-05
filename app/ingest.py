import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

DATA_PATH = "../data/clean"

def load_documents():
    docs = []
    filenames = []

    for file in os.listdir(DATA_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
                docs.append(f.read())
                filenames.append(file)

    return docs, filenames

def build_index():
    docs, filenames = load_documents()

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(docs)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings, dtype="float32"))

    return index, model, docs, filenames
