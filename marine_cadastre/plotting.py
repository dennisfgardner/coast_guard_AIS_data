from pathlib import Path

import contextily as ctx
import matplotlib.pyplot as plt

from .config import RegionOfInterest


def get_basemap(dir: Path, roi: RegionOfInterest) -> None:
    """"
    Get/Save basemap, if needed

    Args:
        dir: directory to save basemap
        roi: region of interest
    Return:
        basemap_path: Path object to basemap
    """
    basemap_name = f"lat_{roi.lat_cen:.0f}_lon_{roi.lon_cen:.0f}_basemap.tif"
    basemap_path = dir / basemap_name

    if not basemap_path.exists():
        print("Basemap not found, downloading...")
        ctx.bounds2raster(
            roi.lon_min, roi.lat_min,
            roi.lon_max, roi.lat_max,
            ll=True, path=basemap_path,
            source=ctx.providers.CartoDB.PositronNoLabels
        )
    return basemap_path
