from evaluate import evaluate

if __name__ == "__main__":
    print("Running defended retrieval scenario...")
    evaluate(
        data_path="../data/clean",
        output_file="results_defended.json",
        attack_type="defended_filtering"
    )
