import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.dirname(__file__))

from evaluate import evaluate

if __name__ == "__main__":
    print("Running defended retrieval scenario...")
    evaluate(
        data_path="../data/clean",
        output_file="results_defended.json",
        attack_type="defended_filtering"
    )
