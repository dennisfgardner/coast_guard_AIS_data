"main entry point"

import csv
from typing import List
from pathlib import Path
from pprint import pprint


from marine_cadastre.config import Config
import marine_cadastre.utilities as ut


def filter_data(csv_files: List[Path], output_dir: Path):
    """Read csv file, remove bad rows, write new file with only vaild data.

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


def main():
    print("Running Marine Cadastre Main Function")

    config = Config()
    pprint(config)

    # get all the filenames
    filenames = ut.list_files_by_type(config.data_dir, ".csv")
    if len(filenames) == 0:
        print(f"No CSV files found in {config.data_dir}")
        return
    else:
        pprint(filenames)
        print(f"Found {len(filenames)} CSV files in {config.data_dir}")

    # filter data, i.e. remove invalid rows
    filtered_data_dir = config.output_dir / "filtered"
    filtered_data_dir.mkdir(parents=True, exist_ok=True)
    full_file_paths = [config.data_dir/f for f in filenames]
    filter_data(full_file_paths, filtered_data_dir)


if __name__ == "__main__":
    main()
