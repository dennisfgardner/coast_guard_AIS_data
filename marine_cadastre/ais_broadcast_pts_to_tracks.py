"AIS Broadcast Points to Tracks"

from pathlib import Path
from typing import Dict, List


import numpy as np
import pandas as pd

from .config import TrackParameters
from .utilities import haversine_distance


class AISTrack:
    def __init__(self, mmsi: int, vessel_name: str):
        self.mmsi = mmsi
        self.vessel_name = vessel_name
        self.timestamps: List[float] = []
        self.lats: List[float] = []
        self.lons: List[float] = []
        self.sogs: List[float] = []
        self.cogs: List[float] = []
        self.start_time: float = None
        self.end_time: float = None
        self.total_distance: float = 0.0  # maybe get rid of this? or add total duration

    def add_position(self, timestamp: float, lat: float, lon: float,
                     sog: float, cog: float):
        """Add a new position to the track."""
        self.timestamps.append(timestamp)
        self.lats.append(lat)
        self.lons.append(lon)
        self.sogs.append(sog)
        self.cogs.append(cog)

        if self.start_time is None or timestamp < self.start_time:
            self.start_time = timestamp
        if self.end_time is None or timestamp > self.end_time:
            self.end_time = timestamp

    def calculate_statistics(self) -> dict:
        """Calculate basic statistics for the track."""
        return {
            'mmsi': self.mmsi,
            'vessel_name': self.vessel_name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'duration_hours': (self.end_time - self.start_time) / 3600 if self.start_time and self.end_time else 0,
            'number_of_positions': len(self.timestamps),
            'average_speed': np.mean(self.sogs) if self.sogs else 0,
            'max_speed': max(self.sogs) if self.sogs else 0,
            'total_distance': self.calculate_total_distance()
        }

    def calculate_total_distance(self) -> float:
        """Calculate the total distance traveled in nautical miles."""
        total_distance = 0.0
        for i in range(len(self.timestamps) - 1):
            lat1, lon1 = self.lats[i], self.lons[i]
            lat2, lon2 = self.lats[i + 1], self.lons[i + 1]
            total_distance += haversine_distance(lat1, lon1, lat2, lon2)
        return total_distance


def broadcast_pts_to_tracks(csv_file: Path,
                            track_params: TrackParameters = TrackParameters()):
    """
    Combine AIS broadcast points into vessel tracks.

    Args:
        csv_file: path to CSV file containing AIS broadcast points
        track_params: track parameters

    Returns:
        Dictionary of MMSI to AISTrack objects
    """

    df = pd.read_csv(csv_file)

    # use POSIX time in seconds
    df['BaseDateTime'] = pd.to_datetime(df['BaseDateTime'], utc=True)
    df['BaseDateTime'] = df['BaseDateTime'].astype(int) / 10**9

    # Sort by MMSI and timestamp
    df = df.sort_values(['MMSI', 'BaseDateTime'])

    tracks: Dict[int, AISTrack] = {}
    for _, row in df.iterrows():
        mmsi = int(row['MMSI'])

        if mmsi not in tracks:
            tracks[mmsi] = AISTrack(mmsi, row['VesselName'])

        tracks[mmsi].add_position(
            row['BaseDateTime'],
            row['LAT'],
            row['LON'],
            row['SOG'],
            row['COG']
        )
    return tracks


def calculate_track_stats(tracks: Dict[int, AISTrack]) -> pd.DataFrame:
    """
    Calculate track statistics.

    Args:
        tracks: dictionary of MMSI to AISTrack objects

    Returns:
        Dataframe of track statistics
    """
    track_stats = []
    for track in tracks.values():
        track_stats.append(track.calculate_statistics())
    return pd.DataFrame(track_stats)


def resample(track: AISTrack, interval=600) -> np.ndarray:
    """
    Resample AIS broadcast data (default 600 seconds (10-minutes))

    Args:
        tracks: dictionary of MMSI to AISTrack objects
        interval: target sampling rate

    Returns:
        Resample data
    """
    target_timestamps = np.arange(track.start_time, track.end_time, interval)
    resamp_lats = np.interp(target_timestamps, track.timestamps, track.lats)
    resamp_lons = np.interp(target_timestamps, track.timestamps, track.lons)
    resamp_sogs = np.interp(target_timestamps, track.timestamps, track.sogs)
    resamp_cogs = np.interp(target_timestamps, track.timestamps, track.cogs)
    return (target_timestamps, resamp_lats, resamp_lons, resamp_sogs, resamp_cogs)
