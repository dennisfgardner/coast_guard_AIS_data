"explore pickled track data"

import pickle
from pathlib import Path
from pprint import pprint


# path to TrAISformer data
traisformer_data_dir = Path("/home/ubuntu/TrAISformer/data/ct_dma/")
datasets = ["train", "valid", "test"]
datapaths = []
for name in datasets:
    datapaths.append(traisformer_data_dir/f"ct_dma_{name}.pkl")
pprint(datapaths)

track_nums = []
overall_shortest_track = 1000000
overall_longest_track = -1000000
for name, file in zip(datasets, datapaths):
    shortest_track = 1000000
    longest_track = -1000000
    with open(file, "rb") as f:
        data = pickle.load(f)
    track_nums.append(len(data))
    for track in data:
        track_data = track["traj"]
        track_pts = track_data.shape[0]
        longest_track = max(longest_track, track_pts)
        shortest_track = min(shortest_track, track_pts)
    print(f"{name} set has {len(data):,} tracks the shortest is {shortest_track} and the longest is {longest_track}")
    overall_longest_track = max(overall_longest_track, longest_track)
    overall_shortest_track = min(overall_shortest_track, shortest_track)

sum = 0
for length in track_nums:
    sum += length
print(f"there are a total of {sum:,} tracks in all the datasets the shortest is {overall_shortest_track} and the longest is {overall_longest_track}")

for name, length in zip(datasets, track_nums):
    print(f"{name} is {length/sum*100:.1f}% of all the data")
