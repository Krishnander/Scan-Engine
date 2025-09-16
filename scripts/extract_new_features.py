import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
from src.features.static_features import extract_features
from tqdm import tqdm

def extract_features_from_directory(directory="new_malware", output_file="data/new_malware_features.json"):
    """
    Extracts features from all files in a directory and saves them to a JSON file.

    Args:
        directory (str): The directory containing the malware samples.
        output_file (str): The path to the output JSON file.
    """
    features_list = []
    file_list = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    for filename in tqdm(file_list, desc="Extracting features"):
        filepath = os.path.join(directory, filename)
        features = extract_features(filepath)
        if features:
            features_list.append(features)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(features_list, f, indent=4)

    print(f"Extracted features from {len(features_list)} files and saved to {output_file}")

if __name__ == "__main__":
    extract_features_from_directory()
