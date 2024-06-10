import os
import json

import pandas as pd
import numpy as np



# Bin Sizes to create a version of the dataset for.
bin_sizes = [5, 20]

antibiotic_dictionary_file = open("data/antibiotics.json", "r")
antibiotic_dictionary = json.load(antibiotic_dictionary_file)

# Create folder to store binned datasets in
binned_folder = "data/unprocessed/binned/"
os.makedirs(binned_folder, exist_ok=True)

unbinned_folder = "data/unprocessed/unbinned/"
unbinned_files = os.listdir(unbinned_folder)
unbinned_file_paths = [unbinned_folder + file for file in unbinned_files]

# For each bin size, create dataset
for bin_size in bin_sizes:
    print("Binning:", unbinned_file_paths)
    print("Bin Size:", bin_size)

    for file in unbinned_file_paths:
        bacteria = pd.read_csv(file)

        species = bacteria["species"][0]
        antibiotics = antibiotic_dictionary[species]

        malditof = bacteria[bacteria.columns.drop(list(bacteria.filter(regex='[^0-9]')))]

        binned_malditof = malditof.T.groupby(np.arange(len(malditof.columns)) // bin_size).mean().T
        binned_malditof.columns = [col for col in range(int(malditof.columns[0]), int(malditof.columns[-1]), bin_size)]

        binned_bac = pd.DataFrame(np.column_stack([binned_malditof, bacteria[antibiotics]]))
        binned_bac.columns = list(binned_malditof.columns) + antibiotics
        binned_bac["species"] = species

        file_name_ext = os.path.basename(file)
        file_name = os.path.splitext(file_name_ext)[0]
        ext = os.path.splitext(file_name_ext)[1]
        new_file_name = binned_folder+file_name+"_bin"+str(bin_size)+ext

        binned_bac.to_csv(new_file_name, index=False, mode='w')

    print("Done.\n")