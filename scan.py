import argparse
import os
import joblib
import ember
import pefile
from termcolor import colored

def load_model(model_path="models/ember_model.joblib"):
    """Loads the trained model."""
    if not os.path.exists(model_path):
        print(colored(f"Error: Model file not found at {model_path}", "red"))
        print(colored("Please run the training script first (scripts/train_model.py)", "red"))
        return None
    return joblib.load(model_path)

def scan_file(filepath, model):
    """Scans a single file and returns the prediction."""
    print(f"Scanning: {filepath}")
    try:
        with open(filepath, "rb") as f:
            pe_bytes = f.read()
        feature_vector = ember.read_pe_features(pe_bytes)
        feature_vector = feature_vector.reshape(1, -1)
        prediction = model.predict(feature_vector)[0]
        if prediction == 1:
            print(colored("  -> Prediction: Malware", "red"))
            return "malware"
        else:
            print(colored("  -> Prediction: Benign", "green"))
            return "benign"
    except pefile.PEFormatError:
        print(colored("  - Not a PE file. Skipping.", "yellow"))
        return "skipped"
    except Exception as e:
        print(colored(f"  - Error processing file: {e}", "red"))
        return "error"

def scan_directory(dirpath, model):
    """Scans a directory for PE files and returns the scan results."""
    results = {"total": 0, "malware": 0, "benign": 0, "skipped": 0, "error": 0}
    print(f"\nScanning directory: {dirpath}")
    for root, _, files in os.walk(dirpath):
        for file in files:
            filepath = os.path.join(root, file)
            result = scan_file(filepath, model)
            if result:
                results["total"] += 1
                results[result] += 1
    return results

def main():
    """Main function for the scanner."""
    parser = argparse.ArgumentParser(description="AI Malware Scanner")
    parser.add_argument("path", help="Path to a file or directory to scan.")
    args = parser.parse_args()

    model = load_model()
    if not model:
        return

    if not os.path.exists(args.path):
        print(colored(f"Error: Path '{args.path}' does not exist.", "red"))
        return

    print(colored("--- AI Malware Scanner ---", "cyan"))
    if os.path.isfile(args.path):
        scan_file(args.path, model)
    elif os.path.isdir(args.path):
        results = scan_directory(args.path, model)
        print(colored("\n--- Scan Summary ---", "cyan"))
        print(f"Total files scanned: {results['total']}")
        print(colored(f"Malware found: {results['malware']}", "red"))
        print(colored(f"Benign found: {results['benign']}", "green"))
        print(colored(f"Skipped (not PE): {results['skipped']}", "yellow"))
        print(colored(f"Errors: {results['error']}", "red"))
        print(colored("--------------------", "cyan"))

    else:
        print(colored(f"Error: Path '{args.path}' is not a file or directory.", "red"))

if __name__ == "__main__":
    main()
