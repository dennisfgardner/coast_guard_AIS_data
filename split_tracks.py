"filter invalid data from marine cadastre csv files"

import random
import pickle
from typing import List
from pathlib import Path
from pprint import pprint
from itertools import islice

import marine_cadastre.utilities as ut
from marine_cadastre.config import Config, TrackParameters
import marine_cadastre.track_data_handler as tdh

def run_split_data():
    """
    Split the pickled track data into train, validation, and test.
    """
    config = Config()
    pkl_track_data_dir = config.track_data_dir
    filenames = ut.list_files_by_type(pkl_track_data_dir, ".pkl")
    if len(filenames) == 0:
        print(f"No pickled files found in {pkl_track_data_dir}")
        return
    else:
        # pprint(filenames)
        print(f"Found {len(filenames)} pickled files in {pkl_track_data_dir}")

    random.shuffle(filenames)
    # pprint(filenames)

    num_train = int(config.splits.train * len(filenames))
    num_valid = int(config.splits.valid * len(filenames))
    num_test = int(config.splits.test * len(filenames))

    total_num = num_train + num_valid + num_test
    unused_data_num = len(filenames) - total_num
    assert unused_data_num > 0, "Splits result in more data than available"
    assert unused_data_num < 3, "Too much data unused "
    if unused_data_num == 1:
        num_test = num_test + 1
    elif unused_data_num == 2:
        num_test = num_test + 1
        num_valid = num_valid +1
    total_num = num_train + num_valid + num_test
    assert total_num == len(filenames), "Unused data"
    print(f"{num_train=} {num_valid=} {num_test=}")
    print(f"{total_num=}")
    print(f"train {num_train/total_num*100:.1f}% "
          f"valid {num_valid/total_num*100:.1f}% "
          f"test {num_test/total_num*100:.1f}%")

    split_nums = [num_train, num_valid, num_test]

    it = iter(filenames)

    filename_splits = [list(islice(it, 0, i)) for i in split_nums]
    split_names = ["mc_ais_train", "mc_ais_valid", "mc_ais_test"]
    counter = 0
    for name, files in zip(split_names, filename_splits):
        print(name)
        # pprint(files)
        print(f"{len(files)}")

        save_dir = config.results_dir
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = config.results_dir/f"{name}.pkl"
        if save_path.exists():
            print(f"{save_path} exists SKIPPING")
            continue
        accum_data = []
        for pkl_file in files:
            pkl_file = config.track_data_dir/pkl_file
            with open(pkl_file, "rb") as f:
                data = pickle.load(f)
            accum_data.extend(data)
            counter += 1
            # print(counter)
        with open(save_path, "wb") as f:
            pickle.dump(accum_data, f)


if __name__ == "__main__":
    run_split_data()
