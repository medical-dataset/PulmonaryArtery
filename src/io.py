# ----------------------
# src/io.py
# ----------------------
import json
import numpy as np

def save_point_ids(ids, output_path):
    """
    Saves point IDs to a JSON file.
    
    Parameters:
    - ids: List of point indices
    - output_path: Path to output .json file
    """
    with open(output_path, 'w') as f:
        json.dump(ids, f)

def load_point_ids(path):
    """
    Loads point IDs from a JSON file.

    Parameters:
    - path: Path to the .json file

    Returns:
    - ids: List of point indices
    """
    with open(path, 'r') as f:
        return json.load(f)