import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.dirname(__file__))

from evaluate import evaluate

if __name__ == "__main__":
    print("Running context poisoning attack scenario...")
    evaluate(
        data_path="../data/contaminated",
        output_file="results_contaminated.json",
        attack_type="context_poisoning"
    )
