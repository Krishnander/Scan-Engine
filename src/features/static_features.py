import pefile
import os
import math
import re

def calculate_entropy(data):
    """Calculates the Shannon entropy of a byte string."""
    if not data:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(x.to_bytes(1, 'big'))) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

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
        return None

    features = {}

    # Header features
    features["header"] = {
        "timestamp": pe.FILE_HEADER.TimeDateStamp,
        "num_sections": pe.FILE_HEADER.NumberOfSections,
        "num_symbols": pe.FILE_HEADER.NumberOfSymbols,
        "machine": pe.FILE_HEADER.Machine,
        "subsystem": pe.OPTIONAL_HEADER.Subsystem,
        "dll_characteristics": pe.OPTIONAL_HEADER.DllCharacteristics,
        "image_base": pe.OPTIONAL_HEADER.ImageBase,
        "size_of_image": pe.OPTIONAL_HEADER.SizeOfImage,
    }

    # Imports features
    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        imported_functions = []
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            for imp in entry.imports:
                if imp.name:
                    imported_functions.append(imp.name.decode())
        features["imports"] = {
            "num_imports": len(pe.DIRECTORY_ENTRY_IMPORT),
            "imported_functions": imported_functions
        }
    else:
        features["imports"] = {
            "num_imports": 0,
            "imported_functions": []
        }

    # Section features
    sections = []
    for section in pe.sections:
        section_data = {
            "name": section.Name.decode().strip('\x00'),
            "virtual_address": section.VirtualAddress,
            "virtual_size": section.Misc_VirtualSize,
            "size_of_raw_data": section.SizeOfRawData,
            "entropy": calculate_entropy(section.get_data())
        }
        sections.append(section_data)
    features["sections"] = sections

    # String features
    strings = re.findall(b"[\x20-\x7E]{4,}", pe.get_memory_mapped_image())
    string_features = {
        "num_strings": len(strings)
    }
    if strings:
        string_features["avg_string_len"] = sum(len(s) for s in strings) / len(strings)
        string_features["num_path_strings"] = len([s for s in strings if b'/' in s or b'\\' in s])
        string_features["num_url_strings"] = len([s for s in strings if b'http://' in s or b'https://' in s])
        string_features["num_registry_strings"] = len([s for s in strings if b'HKEY_' in s])
    else:
        string_features["avg_string_len"] = 0
        string_features["num_path_strings"] = 0
        string_features["num_url_strings"] = 0
        string_features["num_registry_strings"] = 0
    features["strings"] = string_features

    return features

def extract_basic_features(filepath):
    """
    Extracts basic features from any file.
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return None

    features = {}
    features["size"] = os.path.getsize(filepath)
    with open(filepath, "rb") as f:
        data = f.read()
    features["entropy"] = calculate_entropy(data)

    strings = re.findall(b"[\x20-\x7E]{4,}", data)
    string_features = {
        "num_strings": len(strings)
    }
    if strings:
        string_features["avg_string_len"] = sum(len(s) for s in strings) / len(strings)
        string_features["num_path_strings"] = len([s for s in strings if b'/' in s or b'\\' in s])
        string_features["num_url_strings"] = len([s for s in strings if b'http://' in s or b'https://' in s])
        string_features["num_registry_strings"] = len([s for s in strings if b'HKEY_' in s])
    else:
        string_features["avg_string_len"] = 0
        string_features["num_path_strings"] = 0
        string_features["num_url_strings"] = 0
        string_features["num_registry_strings"] = 0
    features["strings"] = string_features

    return features

def extract_features(filepath):
    """
    Extracts features from any file. It dispatches to the appropriate
    feature extractor based on the file type.
    """
    try:
        pefile.PE(filepath)
        return extract_static_features(filepath)
    except pefile.PEFormatError:
        # Not a PE file, extract basic features
        return extract_basic_features(filepath)

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
