import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import joblib
import lightgbm as lgb
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer

def flatten_features(feature_dict, parent_key='', sep='.'):
    """
    Flattens a nested dictionary.
    """
    items = []
    for k, v in feature_dict.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_features(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # For lists, we can either ignore them or try to extract some features
            # For now, let's just get the length of the list
            items.append((new_key + '_len', len(v)))
        else:
            items.append((new_key, v))
    return dict(items)

def train_new_model(features_file="data/new_malware_features.json", model_dir="models"):
    """
    Trains a new LightGBM model on the extracted features.

    Args:
        features_file (str): The path to the JSON file with the extracted features.
        model_dir (str): The directory where the trained model will be saved.
    """
    # --- Data Loading and Preparation ---
    with open(features_file, "r") as f:
        features_list = json.load(f)

    flat_features_list = [flatten_features(f) for f in features_list]
    vectorizer = DictVectorizer()
    X = vectorizer.fit_transform(flat_features_list)

    # Since we downloaded from MalwareBazaar, we assume all samples are malware (label 1)
    y = np.ones(X.shape[0])

    # --- Train/Test Split ---
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- Model Training ---
    print("Training LightGBM model...")
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

    lgbm = lgb.LGBMClassifier(**params)
    lgbm.fit(X_train, y_train)

    # --- Model Saving ---
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "new_malware_model.joblib")
    print(f"Saving model to {model_path}...")
    joblib.dump(lgbm, model_path)

    vectorizer_path = os.path.join(model_dir, "new_malware_vectorizer.joblib")
    print(f"Saving vectorizer to {vectorizer_path}...")
    joblib.dump(vectorizer, vectorizer_path)

    print("Model and vectorizer saved successfully.")

    # --- Evaluation ---
    print("Evaluating model...")
    score = lgbm.score(X_test, y_test)
    print(f"Model accuracy on the test set: {score:.4f}")

if __name__ == "__main__":
    train_new_model()
