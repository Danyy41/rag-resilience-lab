from ingest import build_index
import numpy as np

def query_rag(question):
    index, model, docs, filenames = build_index()

    query_embedding = model.encode([question])
    query_embedding = np.array(query_embedding, dtype="float32")

    distances, indices = index.search(query_embedding, k=min(3, len(docs)))

    print("\nTop results:")
    for i, idx in enumerate(indices[0]):
        print(f"{i+1}. {filenames[idx]}")
        print(docs[idx])
        print("------")

if __name__ == "__main__":
    question = input("Ask a question: ")
    query_rag(question)