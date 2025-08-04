import ember
import lightgbm as lgb
import joblib
import os

def train_ember_model(data_dir="data/ember2018", model_dir="models"):
    """
    Trains a LightGBM model on the EMBER 2018 dataset and saves it.

    Args:
        data_dir (str): The directory where the EMBER dataset is located.
        model_dir (str): The directory where the trained model will be saved.
    """

    # --- Data Loading ---
    # The EMBER dataset is large, so we need to vectorize it first.
    # This creates a memory-mapped file that can be accessed efficiently.
    # This function only needs to be run once.
    print("Vectorizing features. This may take a while...")
    ember.create_vectorized_features(data_dir)

    # --- Model Training ---
    print("Reading vectorized features...")
    X_train, y_train, X_test, y_test = ember.read_vectorized_features(data_dir)

    print("Training LightGBM model...")
    # These are the recommended parameters from the EMBER paper.
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
    model_path = os.path.join(model_dir, "ember_model.joblib")
    print(f"Saving model to {model_path}...")
    joblib.dump(lgbm, model_path)
    print("Model saved successfully.")

    # --- Evaluation (Optional) ---
    # You can uncomment this section to evaluate the model on the test set.
    # print("Evaluating model...")
    # score = lgbm.score(X_test, y_test)
    # print(f"Model accuracy: {score:.4f}")


if __name__ == "__main__":
    # This script assumes you have downloaded the EMBER 2018 dataset
    # and extracted it into the 'data/ember2018' directory.
    #
    # To run this script:
    # 1. Download the dataset from: https://ember.elastic.co/ember_dataset_2018_2.tar.bz2
    # 2. Extract it to 'data/ember2018'.
    # 3. Run this script: python scripts/train_model.py
    train_ember_model()
