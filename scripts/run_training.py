import os
import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.model_selection import train_test_split

# Add the project root to the Python path to allow importing from src
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.features.static_features import extract_static_features
from src.features.vectorizer import vectorize_features

# --- Constants ---
EMBER_DATA_DIR = "data/ember2018"
MODEL_DIR = "models"
NEW_MODEL_NAME = "custom_model.joblib"

import ember

def process_ember_dataset():
    """
    Processes the EMBER dataset using the custom feature extractor.
    This is a long-running process that can take several hours.
    """
    print("Processing EMBER dataset with custom feature extractor...")

    metadata = ember.read_metadata(EMBER_DATA_DIR)

    # We will use the training set from EMBER.
    train_meta = metadata[metadata["subset"] == "train"]

    X_list = []
    y_list = []

    # Using tqdm for a progress bar
    for sha256, label in tqdm(train_meta[["sha256", "label"]].values, desc="Extracting Features"):
        filepath = os.path.join(EMBER_DATA_DIR, "train", sha256)
        if os.path.exists(filepath):
            features = extract_static_features(filepath)
            if features:
                vector = vectorize_features(features)
                X_list.append(vector)
                y_list.append(label)

    # Convert to numpy arrays
    X_data = np.array(X_list)
    y_data = np.array(y_list)

    # The labels are -1 for unlabeled, 0 for benign, 1 for malicious.
    # We will only train on labeled data.
    labeled_indices = np.where(y_data != -1)[0]
    X_data = X_data[labeled_indices]
    y_data = y_data[labeled_indices]

    print(f"Processed {len(X_data)} labeled samples.")

    return X_data, y_data

def train_new_model(X, y):
    """
    Trains a new LightGBM model on the provided data.
    """
    print("Training new LightGBM model...")
    params = {
        "boosting_type": "gbdt",
        "objective": "binary",
        "metric": "binary_logloss",
        "num_leaves": 1023,
        "learning_rate": 0.05,
        "feature_fraction": 0.9,
        "bagging_fraction": 0.8,
        "bagging_freq": 5,
        "verbose": 0,
        "n_estimators": 1000,
    }
    model = lgb.LGBMClassifier(**params)
    model.fit(X, y)
    return model

def main():
    """
    Main function for the training pipeline.
    """
    print("--- Starting Unified Training Pipeline ---")

    # 1. Process the dataset
    X_data, y_data = process_ember_dataset()

    if X_data.size == 0 or y_data.size == 0:
        print("No data was processed. Please ensure the EMBER dataset is in data/ember2018.")
        return

    # 2. Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X_data, y_data, test_size=0.2, random_state=42, stratify=y_data
    )

    # 3. Train the model
    model = train_new_model(X_train, y_train)


    # 4. Evaluate the model
    print("\n--- Model Evaluation ---")
    score = model.score(X_test, y_test)
    print(f"Model accuracy on the test set: {score:.4f}")

    # 5. Save the model
    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, NEW_MODEL_NAME)
    print(f"\nSaving new model to {model_path}...")
    joblib.dump(model, model_path)
    print("Model saved successfully.")

    print("\n--- Unified Training Pipeline Finished ---")

if __name__ == "__main__":
    main()
