"main entry point"

import csv
from typing import List, Dict
from pathlib import Path
from pprint import pprint

import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx

import marine_cadastre.utilities as ut
import marine_cadastre.config as cfg
import marine_cadastre.ais_broadcast_pts_to_tracks as pts2trks
import marine_cadastre.plotting as mc_plt
import marine_cadastre.track_data_handler as tdh


def main():
    print("Running Marine Cadastre Main Function")

    config = cfg.Config()
    pprint(config)

    # get filenames
    filenames = ut.list_files_by_type(config.data_dir, ".csv")
    if len(filenames) == 0:
        print(f"No CSV files found in {config.data_dir}")
        return
    else:
        pprint(filenames)
        print(f"Found {len(filenames)} CSV files in {config.data_dir}")


    csv_file = Path("./output/roi/AIS_2023_01_01.csv")
    # tk_cfg = cfg.TrackParameters()

    # tracks = pts2trks.broadcast_pts_to_tracks(csv_file)

    # track_stats = pts2trks.calculate_track_stats(tracks)
    # # filter tracks based on stats, TODO can be combined into one step
    # track_stats = track_stats[
    #     (track_stats["total_distance"] > tk_cfg.min_dist_nmi) &
    #     (track_stats["duration_hours"] > tk_cfg.min_duration_hrs) &
    #     (track_stats["number_of_positions"] > tk_cfg.min_points)]

    # print("Track Summary:")
    # print(track_stats.to_string())

    # resampled_tracks: Dict[int, np.ndarray] = {}
    # for _, row in track_stats.iterrows():
    #     mmsi = int(row['mmsi'])
    #     resampled_tracks[mmsi] = pts2trks.resample(tracks[mmsi], interval=600)
    # print(resampled_tracks)
    # TODO format data in TrAISformer normalized format
    # TODO normalized lat, lon, sog, cog
    # TODO add mmsi and timestamp values to np.array


    basemap_path = mc_plt.get_basemap(Path("./output"), config.roi)
    track_datapath = Path("./data/ct_dma_train.pkl")
    data = tdh.load_pkld_track_data(track_datapath, config.roi)
    
    plt.style.use("fivethirtyeight")
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.scatter(data[0]["traj"][:, 1], data[0]["traj"][:, 0], s=10, c="blue", alpha=0.5)
    ax.scatter(data[1]["traj"][:, 1], data[1]["traj"][:, 0], s=10, c="red", alpha=0.5)
    ax.scatter(data[2]["traj"][:, 1], data[2]["traj"][:, 0], s=10, c="green", alpha=0.5)
    ax.scatter(data[3]["traj"][:, 1], data[3]["traj"][:, 0], s=10, c="black", alpha=0.5)
    ax.scatter(data[4]["traj"][:, 1], data[4]["traj"][:, 0], s=10, c="orange", alpha=0.5)
    ax.scatter(data[5]["traj"][:, 1], data[5]["traj"][:, 0], s=10, c="purple", alpha=0.5)
    ctx.add_basemap(ax, source=basemap_path, crs="epsg:4326")
    plt.show()




if __name__ == "__main__":
    main()
