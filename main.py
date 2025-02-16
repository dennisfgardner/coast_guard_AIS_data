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

        with open(f"{config.data_dir}/{file}", "r") as f:

            reader = csv.reader(f)

            header = next(reader)
            pprint(header)

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
                    print(f"row {ii+2} {row} contains invalid cog")
                    continue


if __name__ == "__main__":
    main()
