"main entry point"

import csv
from typing import List, Dict
from pathlib import Path
from pprint import pprint

import numpy as np

import marine_cadastre.utilities as ut
import marine_cadastre.config as cfg
import marine_cadastre.ais_broadcast_pts_to_tracks as pts2trks


def filter_invalid_data(csv_files: List[Path], output_dir: Path):
    """
    Read csv file, remove bad rows, write new file with only valid data.

    Args:
        files: marine cadastre csv files, full path to file
        output_dir: directory to write filtered files

    Returns:
        None, write filtered csv to output dir
    """
    for file in csv_files:
        print(f"Processing {file}...")

        with open(file, "r") as input_csv:
            with open(f"{output_dir}/{file.name}", "w") as output_csv:

                reader = csv.reader(input_csv)
                writer = csv.writer(output_csv)

                header = next(reader)
                writer.writerow(header)

                good_rows = 0
                for ii, row in enumerate(reader):
                    mmsi = int(row[0])
                    if not ut.is_mmsi_vessel(mmsi):
                        continue
                    sog = float(row[4])
                    if not ut.is_sog_valid(sog):
                        continue
                    cog = float(row[5])
                    cog = ut.apply_cog_correction(cog)
                    if not ut.is_cog_valid(cog):
                        continue
                    lat = float(row[2])
                    lon = float(row[3])
                    if not ut.is_lat_lon_valid(lat, lon):
                        continue
                    good_rows += 1
                    writer.writerow(row)

        print(f"\tFinished processing {file}")
        print(f"\t\t{ii:,} lines read")
        print(f"\t\t{good_rows:,} valid rows")
        print(f"\t\t{good_rows/ii*100.0:.2f}% valid")


def roi_filter(roi: cfg.RegionOfInterest, csv_files: List[Path], output_dir: Path):
    """
    Filter based on region of interest.

    Args:
        roi: region of interest
        csv_files: filtered csv files, full path to file
        output_dir: directory to write output

    Returns:
        None, write csv to output dir
    """
    for file in csv_files:
        print(f"Processing {file}...")

        with open(file, "r") as input_csv:
            with open(f"{output_dir}/{file.name}", "w") as output_csv:

                reader = csv.reader(input_csv)
                writer = csv.writer(output_csv)

                header = next(reader)
                writer.writerow(header)

                in_roi_rows = 0
                for ii, row in enumerate(reader):
                    lat = float(row[2])
                    lon = float(row[3])
                    if not ut.is_in_roi(roi, lat, lon):
                        continue
                    in_roi_rows += 1
                    writer.writerow(row)

        print(f"\tFinished processing {file}")
        print(f"\t\t{ii:,} lines read")
        print(f"\t\t{in_roi_rows:,} in bound rows")
        print(f"\t\t{in_roi_rows/ii*100.0:.2f}% in bounds")


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

    # filter invalid data
    # filtered_data_dir = config.output_dir / "filtered"
    # filtered_data_dir.mkdir(parents=True, exist_ok=True)
    # raw_data_filepaths = [config.data_dir/f for f in filenames]
    # filter_invalid_data(raw_data_filepaths, filtered_data_dir)

    # filter based on roi
    # roi_data_dir = config.output_dir / "roi"
    # roi_data_dir.mkdir(parents=True, exist_ok=True)
    # filtered_data_filepaths = [filtered_data_dir/f for f in filenames]
    # roi_filter(config.roi, filtered_data_filepaths, roi_data_dir)

    csv_file = Path("./output/roi/AIS_2023_01_01.csv")
    tk_cfg = cfg.TrackParameters()

    tracks = pts2trks.broadcast_pts_to_tracks(csv_file)

    track_stats = pts2trks.calculate_track_stats(tracks)
    # filter tracks based on stats, TODO can be combined into one step
    track_stats = track_stats[
        (track_stats["total_distance"] > tk_cfg.min_dist_nmi) &
        (track_stats["duration_hours"] > tk_cfg.min_duration_hrs) &
        (track_stats["number_of_positions"] > tk_cfg.min_points)]

    print("Track Summary:")
    print(track_stats.to_string())

    resampled_tracks: Dict[int, np.ndarray] = {}
    for _, row in track_stats.iterrows():
        mmsi = int(row['mmsi'])
        resampled_tracks[mmsi] = pts2trks.resample(tracks[mmsi], interval=600)
    print(resampled_tracks)


if __name__ == "__main__":
    main()
