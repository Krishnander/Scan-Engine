import argparse
import os
import joblib
import pefile
from termcolor import colored
from src.features.static_features import extract_features
from scripts.train_new_model import flatten_features


def load_model(model_path="models/new_malware_model.joblib", vectorizer_path="models/new_malware_vectorizer.joblib"):
    """Loads the trained model and vectorizer."""
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        print(colored(f"Error: Model or vectorizer file not found.", "red"))
        print(colored("Please run the training script first (scripts/train_new_model.py)", "red"))
        return None, None
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer

def scan_file(filepath, model, vectorizer):
    """Scans a single file and returns the prediction."""
    print(f"Scanning: {filepath}")
    try:
        features = extract_features(filepath)
        if not features:
            print(colored("  - Could not extract features. Skipping.", "yellow"))
            return "skipped"

        flat_features = flatten_features(features)
        feature_vector = vectorizer.transform([flat_features])

        prediction = model.predict(feature_vector)[0]
        if prediction == 1:
            print(colored("  -> Prediction: Malware", "red"))
            return "malware"
        else:
            print(colored("  -> Prediction: Benign", "green"))
            return "benign"

    except Exception as e:
        print(colored(f"  - Error processing file: {e}", "red"))
        return "error"

def scan_directory(dirpath, model, vectorizer):
    """Scans a directory for PE files and returns the scan results."""
    results = {"total": 0, "malware": 0, "benign": 0, "skipped": 0, "error": 0, "scanned": 0}
    print(f"\nScanning directory: {dirpath}")
    for root, _, files in os.walk(dirpath):
        for file in files:
            filepath = os.path.join(root, file)
            result = scan_file(filepath, model, vectorizer)
            if result:
                results["total"] += 1
                results[result] += 1
    return results

def main():
    """Main function for the scanner."""
    parser = argparse.ArgumentParser(description="AI Malware Scanner")
    parser.add_argument("path", help="Path to a file or directory to scan.")
    args = parser.parse_args()

    model, vectorizer = load_model()
    if not model or not vectorizer:
        return

    if not os.path.exists(args.path):
        print(colored(f"Error: Path '{args.path}' does not exist.", "red"))
        return

    print(colored("--- AI Malware Scanner ---", "cyan"))
    if os.path.isfile(args.path):
        scan_file(args.path, model, vectorizer)
    elif os.path.isdir(args.path):
        results = scan_directory(args.path, model, vectorizer)
        print(colored("\n--- Scan Summary ---", "cyan"))
        print(f"Total files scanned: {results['total']}")
        print(colored(f"Malware found: {results['malware']}", "red"))
        print(colored(f"Benign found: {results['benign']}", "green"))
        print(colored(f"Skipped: {results['skipped']}", "yellow"))
        print(colored(f"Errors: {results['error']}", "red"))
        print(colored("--------------------", "cyan"))

    else:
        print(colored(f"Error: Path '{args.path}' is not a file or directory.", "red"))

if __name__ == "__main__":
    main()
