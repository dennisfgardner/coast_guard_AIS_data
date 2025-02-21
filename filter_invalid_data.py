"filter invalid data from marine cadastre csv files"

import csv
from typing import List
from pathlib import Path
from pprint import pprint

import marine_cadastre.utilities as ut
from marine_cadastre.config import Config, TrackParameters


def filter_invalid_data(csv_files: List[Path], output_dir: Path, trk_params: TrackParameters):
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
        file_to_write = output_dir/file.name
        if file_to_write.exists():
            print(f"\t{file} exists SKIPPING")
            continue
        with open(file, "r") as input_csv:
            with open(file_to_write, "w") as output_csv:

                reader = csv.reader(input_csv)
                writer = csv.writer(output_csv)

                header = next(reader)
                writer.writerow(header)

                good_rows = 0
                for ii, row in enumerate(reader):
                    # ensure mmsi number is valid
                    try:
                        mmsi = int(row[0])
                    except ValueError:
                        continue
                    if not ut.is_mmsi_vessel(mmsi):
                        continue
                    # ensure sog is valid
                    # max speed over ground in knots
                    sog = float(row[4])
                    max_sog_kts = trk_params.max_sog_kts
                    if not ut.is_sog_valid(sog, max_sog_kts):
                        continue
                    # ensure cog is valid
                    cog = float(row[5])
                    cog = ut.apply_cog_correction(cog)
                    if not ut.is_cog_valid(cog):
                        continue
                    # ensure lat and lon are valid
                    lat = float(row[2])
                    lon = float(row[3])
                    if not ut.is_lat_lon_valid(lat, lon):
                        continue
                    # if all good, then write row
                    good_rows += 1
                    writer.writerow(row)

        print(f"\tFinished processing {file}")
        print(f"\t\t{ii:,} lines read")
        print(f"\t\t{good_rows:,} valid rows")
        print(f"\t\t{good_rows/ii*100.0:.2f}% valid")


def run_filter_invalid_data():
    print("Running Marine Cadastre Filter Invalid Function")

    # get filenames
    config = Config()
    unfiltered_data = config.upzips_data_dir
    filenames = ut.list_files_by_type(unfiltered_data, ".csv")
    if len(filenames) == 0:
        print(f"No CSV files found in {unfiltered_data}")
        return
    else:
        pprint(filenames)
        print(f"Found {len(filenames)} CSV files in {unfiltered_data}")

    # filter invalid data
    filtered_data_dir = config.filtered_data_dir
    filtered_data_dir.mkdir(parents=True, exist_ok=True)
    raw_data_filepaths = [unfiltered_data/f for f in filenames]
    filter_invalid_data(raw_data_filepaths, filtered_data_dir, config.track_params)


if __name__ == "__main__":
    run_filter_invalid_data()
