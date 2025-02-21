"main entry point"

import csv
from typing import List
from pathlib import Path
from pprint import pprint

import marine_cadastre.utilities as ut
from marine_cadastre.config import Config, RegionOfInterest


def roi_selector(roi: RegionOfInterest, csv_files: List[Path], output_dir: Path):
    """
    Select based on region of interest.

    Args:
        roi: region of interest
        csv_files: filtered csv files, full path to file
        output_dir: directory to write output

    Returns:
        None, write csv to output dir
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


def run_roi_selector():
    print("Running Marine Cadastre ROI Selector Function")

    # get filenames
    config = Config()
    filtered_data = config.filtered_data_dir
    filenames = ut.list_files_by_type(filtered_data, ".csv")
    if len(filenames) == 0:
        print(f"No CSV files found in {filtered_data}")
        return
    else:
        pprint(filenames)
        print(f"Found {len(filenames)} CSV files in {filtered_data}")

    # select based on roi
    roi_data_dir = config.rois_data_dir
    roi_data_dir.mkdir(parents=True, exist_ok=True)
    filtered_data_filepaths = [filtered_data/f for f in filenames]
    roi = config.roi
    roi_selector(roi, filtered_data_filepaths, roi_data_dir)


if __name__ == "__main__":
    run_roi_selector()
