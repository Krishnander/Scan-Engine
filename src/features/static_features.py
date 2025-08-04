import pefile
import os

def extract_static_features(filepath):
    """
    Extracts basic static features from a PE file.

    This function is a starting point for custom feature extraction.
    You can extend it to extract many more features.

    Args:
        filepath (str): The path to the PE file.

    Returns:
        dict: A dictionary of extracted features, or None if the file is not a PE file.
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return None

    try:
        pe = pefile.PE(filepath)
    except pefile.PEFormatError:
        print(f"Error: {filepath} is not a valid PE file.")
        return None

    features = {
        "timestamp": pe.FILE_HEADER.TimeDateStamp,
        "num_sections": pe.FILE_HEADER.NumberOfSections,
        "num_symbols": pe.FILE_HEADER.NumberOfSymbols,
        "machine": pe.FILE_HEADER.Machine,
    }

    # Example of extracting imported functions
    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        features["num_imports"] = len(pe.DIRECTORY_ENTRY_IMPORT)
        imported_functions = []
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            for imp in entry.imports:
                if imp.name:
                    imported_functions.append(imp.name.decode())
        features["imported_functions"] = imported_functions
    else:
        features["num_imports"] = 0
        features["imported_functions"] = []


    return features

if __name__ == "__main__":
    # This is an example of how to use the feature extractor.
    # We will create a dummy file for demonstration since we can't have
    # real PE files in the environment.

    # In a real scenario, you would provide a path to a real PE file.
    # For example:
    # features = extract_static_features("path/to/your/file.exe")
    # if features:
    #     print("\n--- Extracted Features ---")
    #     for key, value in features.items():
    #         if isinstance(value, list):
    #             print(f"{key}: {len(value)} items")
    #         else:
    #             print(f"{key}: {value}")
    #     print("------------------------\n")

    print("Static feature extraction script created.")
    print("This script is ready to be used with real PE files.")
    pass
