from pathlib import Path
from pprint import pprint
from dataclasses import dataclass


@dataclass(frozen=True)
class TrackParameters():
    """define parameters for track processing

    """
    min_duration_hrs: float = 1.0
    min_dist_nmi: float = 5.0
    min_points: int = 10

# TODO RegionOfInterest should have setters which update the calculated values

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


# @dataclass(frozen=True)
# class RegionOfInterest():
#     """define ROI in lat & long degrees

#     default values from TrAISformer publication
#     """

#     # latitude
#     lat_cen: float = 56.75
#     lat_width: float = 2.5
#     # longitude
#     lon_cen: float = 11.65
#     lon_width: float = 2.7
#     # calculate extent of ROI
#     lat_min: float = lat_cen - lat_width / 2
#     lat_max: float = lat_cen + lat_width / 2
#     lon_min: float = lon_cen - lon_width / 2
#     lon_max: float = lon_cen + lon_width / 2


@dataclass()
class Config:
    data_dir: Path = Path("./data")
    output_dir: Path = Path("./output")
    roi: RegionOfInterest = RegionOfInterest()
    track_params: TrackParameters = TrackParameters()


if __name__ == "__main__":
    pprint(Config())
