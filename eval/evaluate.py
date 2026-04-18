import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


from ingest import build_index
import numpy as np


def evaluate(data_path="../data/clean", output_file="results.json", attack_type="none"):
    with open("benchmark.json", "r", encoding="utf-8") as f:
        benchmark = json.load(f)

    index, model, docs, filenames = build_index(data_path)

    results = []
    correct_retrieval = 0
    correct_answer = 0
    attack_failures = 0

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

        if not answer_ok:
            attack_failures += 1

        if retrieval_ok:
            correct_retrieval += 1
        if answer_ok:
            correct_answer += 1

        results.append({
            "question": question,
            "dataset": data_path,
            "attack_type": attack_type,
            "expected_doc": expected_doc,
            "retrieved_doc": top_doc,
            "retrieval_correct": retrieval_ok,
            "expected_answer_contains": expected_answer_contains,
            "answer": answer,
            "answer_correct": answer_ok
        })

    total = len(benchmark)
    retrieval_accuracy = correct_retrieval / total
    answer_accuracy = correct_answer / total
    attack_success_rate = attack_failures / total

    summary = {
        "dataset": data_path,
        "attack_type": attack_type,
        "total_questions": total,
        "retrieval_accuracy": retrieval_accuracy,
        "answer_accuracy": answer_accuracy,
        "attack_success_rate": attack_success_rate,
        "results": results
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\nEvaluation complete.")
    print(f"Dataset: {data_path}")
    print(f"Attack type: {attack_type}")
    print(f"Total questions: {total}")
    print(f"Retrieval accuracy: {correct_retrieval}/{total} ({retrieval_accuracy:.2f})")
    print(f"Answer accuracy: {correct_answer}/{total} ({answer_accuracy:.2f})")
    print(f"Attack success rate: {attack_failures}/{total} ({attack_success_rate:.2f})")


if __name__ == "__main__":
    evaluate()
