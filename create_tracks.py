"main entry point"

import pickle
from pprint import pprint

import numpy as np

import marine_cadastre.utilities as ut
from marine_cadastre.config import Config
import marine_cadastre.ais_broadcast_pts_to_tracks as pts2trks


def run_create_tracks():
    print("Running Marine Cadastre Main Function")

    config = Config()
    pprint(config)

    # get filenames
    filenames = ut.list_files_by_type(config.rois_data_dir, ".csv")
    if len(filenames) == 0:
        print(f"No CSV files found in {config.rois_data_dir}")
        return
    else:
        pprint(filenames)
        print(f"Found {len(filenames)} CSV files in {config.rois_data_dir}")

    for file in filenames:

        filepath = config.rois_data_dir/file
        print(f"working on {filepath}")

        track_data_dir = config.track_data_dir
        track_data_dir.mkdir(parents=True, exist_ok=True)
        track_filepath = config.track_data_dir/file
        track_filepath = track_filepath.with_suffix(".pkl")
        if track_filepath.exists():
            print(f"\t{file} exists SKIPPING")
            continue

        tracks = pts2trks.broadcast_pts_to_tracks(filepath)

        track_stats = pts2trks.calculate_track_stats(tracks)
        # filter tracks based on stats
        track_stats = track_stats[
            (track_stats["total_distance"] > config.track_params.min_dist_nmi) &
            (track_stats["duration_hours"] > config.track_params.min_duration_hrs) &
            (track_stats["number_of_positions"] > config.track_params.min_raw_points)]

        traisformer = []
        for _, row in track_stats.iterrows():
            mmsi = int(row['mmsi'])
            timestamps, lats, lons, sogs, cogs = pts2trks.resample(
                tracks[mmsi],
                interval=config.track_params.resampled_time_sec
            )
            # trajectory data in the format used in TrAISformer publication
            if timestamps.shape[0] < config.track_params.min_resampled_points:
                continue
            entry = {}
            entry["mmsi"] = mmsi
            traj = np.zeros((timestamps.shape[0], 6), dtype=np.float32)
            traj[:, 0] = (lats - config.roi.lat_min)/(config.roi.lat_width)
            traj[:, 1] = (lons - config.roi.lon_min)/(config.roi.lon_width)
            traj[:, 2] = sogs/40.0
            traj[:, 3] = cogs/360.0
            traj[:, 4] = timestamps
            traj[:, 5] = mmsi
            entry["traj"] = traj
            traisformer.append(entry)

        with open(track_filepath, "wb") as f:
            pickle.dump(traisformer, f)


if __name__ == "__main__":
    run_create_tracks()
