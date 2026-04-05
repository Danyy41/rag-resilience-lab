from ingest import build_index
import numpy as np
import json

def answer_question(question, data_path="../data/clean"):
    index, model, docs, filenames = build_index(data_path)

    query_embedding = model.encode([question])
    query_embedding = np.array(query_embedding, dtype="float32")

    distances, indices = index.search(query_embedding, k=min(3, len(docs)))

    retrieved_docs = [filenames[i] for i in indices[0]]
    context = "\n".join([docs[i] for i in indices[0]])

    print("\nRetrieved documents:")
    print(retrieved_docs)

    print("\nAnswer:")
    print(context)

    log = {
        "question": question,
        "dataset": data_path,
        "retrieved_docs": retrieved_docs,
        "context": context,
        "answer": context
    }

    with open("../logs/log.json", "w") as f:
        json.dump(log, f, indent=2)