"main entry point"

from pprint import pprint

import contextily as ctx
import matplotlib.pyplot as plt

import marine_cadastre.utilities as ut
from marine_cadastre.config import Config
import marine_cadastre.plotting as mc_plt
import marine_cadastre.track_data_handler as tdh


def run_create_tracks():
    print("Running Marine Cadastre Main Function")

    config = Config()
    pprint(config)

    # get filenames
    filenames = ut.list_files_by_type(config.track_data_dir, ".pkl")
    if len(filenames) == 0:
        print(f"No pickle files found in {config.track_data_dir}")
        return
    else:
        pprint(filenames)
        print(f"Found {len(filenames)} pickle files in {config.track_data_dir}")

    # get basemap
    basemap_path = mc_plt.get_basemap(config.results_dir, config.roi)

    for file in filenames:

        filepath = config.track_data_dir/file
        print(f"working on {filepath}")

        plot_data_dir = config.results_dir
        plot_data_dir.mkdir(parents=True, exist_ok=True)
        fig_filename = plot_data_dir/file
        fig_filename = fig_filename.with_suffix(".png")
        if fig_filename.exists():
            print(f"\t{file} exists SKIPPING")
            continue

        data = tdh.load_pkld_track_data(filepath, config.roi)

        print(f"\tLoaded {len(data)} tracks")

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
        fig.savefig(fig_filename)
        print(f"\tshortest {shortest:,} and longest {longest:,}")


if __name__ == "__main__":
    run_create_tracks()
