from attacks.context_poisoning import inject_conflicting_refund_policy
from evaluate import evaluate

if __name__ == "__main__":
    print("Running context poisoning attack scenario...")
    evaluate(
        data_path="../data/contaminated",
        output_file="results_contaminated.json",
        attack_type="context_poisoning"
    )
