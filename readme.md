# Marine Cadastre

Process all the 2023 Marine Cadastre Automatic Identification System broadcast messages into the format used by [TrAISformer](https://github.com/CIA-Oceanix/TrAISformer).

## Notes

### Getting the Data

Edit the paths in `scripts/get_all_2023_broadcast_data.sh` to download all the data.
It's about 111GB of compressed csv files.
I downloaded to a directory called `zips`.
Then I used the following command to unzip all and move into another directory.

```bash
ls zips/ | xargs -I {} unzip zips/{} -d unzips/
```

The unzipped data is about 303GB.

### Filter Out Invalid data

Run `python ./filter_invalid_data.py` to remove bad data.
Bad data can mean unrealistic speeds (see max_sog_kts in config.py), mmsi numbers that are not 9 digits, mmsi numbers that are aircraft, negative headings, etc.
Rows in the csv that passes the validation checks are written into another csv file.
Roughly 80-82% of the data is valid.
Update the paths for your system.

### Select Region-of-Interest Data

The TrAISformer paper trained a model on a region of interested about 2.5 x 2.7 degrees in lat x lon.
The same ROI size is the default in configs.py.
However, unlike the TrAISformer, the default ROI is centered around Washington, DC / Chesapeake Bay.
Run `python ./select_roi_data.py` to select only the data within the ROI.
About 4-7% of the data is within the default Washington DC / Chesapeake Bay ROI.

### Create Tracks

Create vessel tracks from the broadcast messages.
Run `./create_tracks.py`.
Optionally, you can plot the tracks with `./plot_tracks.py`.