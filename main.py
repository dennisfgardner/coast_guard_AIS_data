"main entry point"

import pickle
from pathlib import Path
from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx

import marine_cadastre.utilities as ut
from marine_cadastre.config import Config
import marine_cadastre.ais_broadcast_pts_to_tracks as pts2trks
import marine_cadastre.plotting as mc_plt
import marine_cadastre.track_data_handler as tdh


def main():
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

    csv_file = config.rois_data_dir/filenames[0]  # for debug only
    print(csv_file)

    tracks = pts2trks.broadcast_pts_to_tracks(csv_file)

    track_stats = pts2trks.calculate_track_stats(tracks)
    # filter tracks based on stats
    track_stats = track_stats[
        (track_stats["total_distance"] > config.track_params.min_dist_nmi) &
        (track_stats["duration_hours"] > config.track_params.min_duration_hrs) &
        (track_stats["number_of_positions"] > config.track_params.min_raw_points)]

    print("Track Summary:")
    print(track_stats.to_string())

    traisformer = []
    for _, row in track_stats.iterrows():
        mmsi = int(row['mmsi'])
        timestamps, lats, lons, sogs, cogs = pts2trks.resample(tracks[mmsi],
                                                               interval=config.track_params.resampled_time_sec)
        # trajectory data in the format used in TrAISformer publication
        if timestamps.shape[0] < config.track_params.min_resampled_points:
            continue
        entry = {}
        entry[mmsi] = mmsi
        traj = np.zeros((timestamps.shape[0], 6), dtype=np.float32)
        traj[:, 0] = (lats - config.roi.lat_min)/(config.roi.lat_width)
        traj[:, 1] = (lons - config.roi.lon_min)/(config.roi.lon_width)
        traj[:, 2] = sogs/40.0
        traj[:, 3] = cogs/360.0
        traj[:, 4] = timestamps
        traj[:, 5] = mmsi
        entry["traj"] = traj
        traisformer.append(entry)

    track_data_dir = config.track_data_dir
    track_data_dir.mkdir(parents=True, exist_ok=True)
    with open(config.track_data_dir / "traisformer_data.pkl", "wb") as f:
        pickle.dump(traisformer, f)

    basemap_path = mc_plt.get_basemap(config.results_dir, config.roi)
    # track_datapath = Path("./data/ct_dma_train.pkl")
    track_datapath = Path(config.track_data_dir / "traisformer_data.pkl")
    data = tdh.load_pkld_track_data(track_datapath, config.roi)

    print(f"Loaded {len(data)} tracks")

    shortest = 1000000
    longest = -1000000

    plt.style.use("fivethirtyeight")
    fig, ax = plt.subplots(figsize=(10, 10))
    for entry in data:
        pts = entry["traj"].shape[0]
        shortest = min(shortest, pts)
        longest = max(longest, pts)
        ax.scatter(entry["traj"][:, 1], entry["traj"][:, 0], s=10, alpha=0.5)
    ctx.add_basemap(ax, source=basemap_path, crs="epsg:4326")
    fig.savefig(config.results_dir/"track_plot.png")
    print(f"shortest {shortest:,} and longest {longest:,}")


if __name__ == "__main__":
    main()
