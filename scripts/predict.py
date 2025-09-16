import joblib
import numpy as np
import ember

def predict_sample(model_path="models/ember_model.joblib", feature_vector=None):
    """
    Loads a trained model and makes a prediction on a feature vector.

    Args:
        model_path (str): The path to the saved model.
        feature_vector (numpy.ndarray): The feature vector to classify.
    """

    # --- Load Model ---
    print(f"Loading model from {model_path}...")
    try:
        model = joblib.load(model_path)
    except FileNotFoundError:
        print(f"Error: Model file not found at {model_path}")
        print("Please run the training script first (scripts/train_model.py)")
        return

    # --- Prepare Feature Vector ---
    if feature_vector is None:
        print("No feature vector provided. Using a placeholder vector for demonstration.")
        # This is a placeholder. In a real scenario, you would extract
        # features from a PE file to create this vector.
        # The EMBER feature vector has 2381 features.
        feature_vector = np.random.rand(1, 2381)

    # --- Prediction ---
    prediction = model.predict(feature_vector)
    prediction_prob = model.predict_proba(feature_vector)

    # --- Output ---
    print("\n--- Prediction Results ---")
    if prediction[0] == 1:
        print("Prediction: Malware")
    else:
        print("Prediction: Benign")

    print(f"Prediction probabilities (Benign, Malware): {prediction_prob[0]}")
    print("------------------------\n")

    return prediction[0], prediction_prob[0]


if __name__ == "__main__":
    # --- Example Usage ---
    # This script demonstrates how to use the trained model to make a prediction.

    # **To predict on a real file:**
    # 1. You would first need to extract its features using `ember.read_pe_features()`.
    #    This would give you a feature vector.
    # 2. Then, you would pass that vector to the `predict_sample` function.
    #
    # Example with a placeholder vector:
    predict_sample()

    # **Example of how to get a feature vector from a file (for demonstration):**
    #
    # try:
    #     # Read the bytes of a PE file (e.g., putty.exe)
    #     with open("path/to/your/file.exe", "rb") as f:
    #         pe_bytes = f.read()
    #
    #     # Extract features using the ember library
    #     feature_vector = ember.read_pe_features(pe_bytes)
    #
    #     # Reshape for a single prediction
    #     feature_vector = feature_vector.reshape(1, -1)
    #
    #     # Make the prediction
    #     predict_sample(feature_vector=feature_vector)
    #
    # except FileNotFoundError:
    #     print("Example file not found. Skipping prediction on a real file.")
    # except ImportError:
    #     print("Could not import LIEF. Skipping prediction on a real file.")
    pass
