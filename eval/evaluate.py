import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "app"))

from ingest import build_index
import numpy as np

def evaluate():
    with open("benchmark.json", "r", encoding="utf-8") as f:
        benchmark = json.load(f)

    index, model, docs, filenames = build_index()

    results = []
    correct_retrieval = 0
    correct_answer = 0

    for item in benchmark:
        question = item["question"]
        expected_doc = item["expected_doc"]
        expected_answer_contains = item["expected_answer_contains"]

        query_embedding = model.encode([question])
        query_embedding = np.array(query_embedding, dtype="float32")

        distances, indices = index.search(query_embedding, k=min(3, len(docs)))

        top_doc = filenames[indices[0][0]]
        answer = docs[indices[0][0]]

        retrieval_ok = top_doc == expected_doc
        answer_ok = expected_answer_contains.lower() in answer.lower()

        if retrieval_ok:
            correct_retrieval += 1
        if answer_ok:
            correct_answer += 1

        results.append({
            "question": question,
            "expected_doc": expected_doc,
            "retrieved_doc": top_doc,
            "retrieval_correct": retrieval_ok,
            "expected_answer_contains": expected_answer_contains,
            "answer": answer,
            "answer_correct": answer_ok
        })

    summary = {
        "total_questions": len(benchmark),
        "retrieval_accuracy": correct_retrieval / len(benchmark),
        "answer_accuracy": correct_answer / len(benchmark),
        "results": results
    }

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\nEvaluation complete.")
    print(f"Total questions: {len(benchmark)}")
    print(f"Retrieval accuracy: {correct_retrieval}/{len(benchmark)}")
    print(f"Answer accuracy: {correct_answer}/{len(benchmark)}")

if __name__ == "__main__":
    evaluate()