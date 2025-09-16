import numpy as np

def vectorize_features(features):
    """
    Converts the feature dictionary from static_features.py into a flat numpy array.

    This is a simple implementation. A more robust solution would involve
    more sophisticated feature engineering, such as hashing imported function names
    or using a more detailed analysis of section properties.

    Args:
        features (dict): The feature dictionary from extract_static_features.

    Returns:
        np.ndarray: A flat numpy array representing the feature vector.
    """
    vector = []

    # Header features (all numerical)
    header = features.get("header", {})
    vector.extend([
        header.get("timestamp", 0),
        header.get("num_sections", 0),
        header.get("num_symbols", 0),
        header.get("machine", 0),
        header.get("subsystem", 0),
        header.get("dll_characteristics", 0),
        header.get("image_base", 0),
        header.get("size_of_image", 0),
    ])

    # Imports features
    imports = features.get("imports", {})
    vector.append(imports.get("num_imports", 0))
    # For now, we'll just use the count of imported functions.
    # In the future, we could use hashing or other techniques on the names.
    vector.append(len(imports.get("imported_functions", [])))

    # Section features
    sections = features.get("sections", [])
    if sections:
        # Aggregate features from all sections
        num_sections = len(sections)
        avg_virtual_size = sum(s.get("virtual_size", 0) for s in sections) / num_sections
        avg_raw_data_size = sum(s.get("size_of_raw_data", 0) for s in sections) / num_sections
        avg_entropy = sum(s.get("entropy", 0) for s in sections) / num_sections
        vector.extend([num_sections, avg_virtual_size, avg_raw_data_size, avg_entropy])
    else:
        vector.extend([0, 0, 0, 0])

    # String features
    strings = features.get("strings", {})
    vector.extend([
        strings.get("num_strings", 0),
        strings.get("avg_string_len", 0),
        strings.get("num_path_strings", 0),
        strings.get("num_url_strings", 0),
        strings.get("num_registry_strings", 0),
    ])

    return np.array(vector, dtype=np.float32)
