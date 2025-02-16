"main entry point"

import csv
from pprint import pprint

from marine_cadastre.config import Config
import marine_cadastre.utilities as ut


def main():
    print("Running Marine Cadastre Main Function")

    config = Config()
    pprint(config)

    files = ut.list_files_by_type(config.data_dir, ".csv")
    pprint(files)

    for file in files:
        print(f"Processing {file}...")

        with open(f"{config.data_dir}/{file}", "r") as input_csv:
            with open(f"{config.data_dir}/filtered_{file}", "w") as output_csv:

                reader = csv.reader(input_csv)
                writer = csv.writer(output_csv)

                header = next(reader)
                writer.writerow(header)

                good_rows = 0
                for ii, row in enumerate(reader):

                    mmsi = int(row[0])
                    if not ut.is_mmsi_vessel(mmsi):
                        continue
                        print(f"row {ii+2} {row} contains invalid mmsi")

                    sog = float(row[4])
                    if not ut.is_sog_valid(sog):
                        continue
                        print(f"row {ii+2} {row} contains invalid sog")

                    cog = float(row[5])
                    cog = ut.apply_cog_correction(cog)
                    if not ut.is_cog_valid(cog):
                        continue
                        print(f"row {ii+2} {row} contains invalid cog")

                    lat = float(row[2])
                    lon = float(row[3])
                    if not ut.is_lat_lon_valid(lat, lon):
                        continue
                        print(f"row {ii+2} {row} contains invalid lat/lon")
                    good_rows += 1
                    writer.writerow(row)
        print(f"\tFinished processing {file}")
        print(f"\t\t{ii:,} lines read")
        print(f"\t\t{good_rows:,} valid rows")
        print(f"\t\t{good_rows/ii*100.0:.2f}% valid")


if __name__ == "__main__":
    main()
