"normalized track in TrAISformer publication format"

import pickle
from pathlib import Path
from typing import List, Dict

from .config import RegionOfInterest
from .utilities import undo_norm_ll


def load_pkld_track_data(datapath: Path, roi: RegionOfInterest) -> List[Dict]:
    """
    Load pickled track data from pickle file and undo lat, lon normalization.
    SOG and COG are still normalized.

    Args:
        file_path: path to pickle file
        roi: region of interest

    Returns:
        List of dictionaries containing unnormalized lat, lon track data
    """
    with open(datapath, "rb") as f:
        data = pickle.load(f)
    for entry in data:
        traj = entry["traj"]
        traj[:, 0], traj[:, 1] = undo_norm_ll(roi, traj[:, 0], traj[:, 1])
    return data
