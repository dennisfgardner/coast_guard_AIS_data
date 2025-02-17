from pathlib import Path
from pprint import pprint
from dataclasses import dataclass


@dataclass(frozen=True)
class RegionOfInterest():
    """define ROI in lat & long degrees

    default values center around Chesapeake Bay near Washington D.C.
    with height and width similar to the TrAISformer publication
    """

    # latitude
    lat_cen: float = 38.0
    lat_width: float = 2.5
    # longitude
    lon_cen: float = -76.0
    lon_width: float = 2.7
    # calculate extent of ROI
    lat_min: float = lat_cen - lat_width / 2
    lat_max: float = lat_cen + lat_width / 2
    lon_min: float = lon_cen - lon_width / 2
    lon_max: float = lon_cen + lon_width / 2


@dataclass()
class Config:
    data_dir: Path = Path("./data")
    output_dir: Path = Path("./output")
    roi: RegionOfInterest = RegionOfInterest()


if __name__ == "__main__":
    pprint(Config())
