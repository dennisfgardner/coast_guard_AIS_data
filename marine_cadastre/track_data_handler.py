"normalized track in TrAISformer publication format"

import pickle
from pathlib import Path
from typing import List, Dict

from .config import RegionOfInterest


def load_norm_track_data(datapath: Path, roi: RegionOfInterest) -> List[Dict]:
    """
    Load normalized track data from pickle file.

    Args:
        file_path: path to pickle file
        roi: region of interest

    Returns:
        List of dictionaries containing unnormalized track data
        TODO unnormalized SOG and COG
    """
    with open(datapath, "rb") as f:
        data = pickle.load(f)
    print(f"Loaded {len(data)} tracks")
    # TODO unnormalize LAT LON SOG and COG