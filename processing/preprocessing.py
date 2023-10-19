import os
import json
import argparse

import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--Folder", help = "Wheter to process the raw or the binned folder")
parser.add_argument("-m", "--Min", help = "Minimum amount of instances a class must have to be included")
args = parser.parse_args()

min_instances = 10
if args.Min:
    min_instances = args.Min

unprocessed_folder = "data/unprocessed/raw/"
processed_folder = "data/processed/raw/"
if args.Folder:
    unprocessed_folder = "data/unprocessed/"+args.Folder+"/"
    processed_folder = "data/processed/"+args.Folder+"/"

antibiotic_dictionary_file = open("data/antibiotics.json", "r")
antibiotic_dictionary = json.load(antibiotic_dictionary_file)

unprocessed_files = os.listdir(unprocessed_folder)
unprocessed_file_paths = [unprocessed_folder + file for file in unprocessed_files]

for file in unprocessed_file_paths:
    print("Processing", file)
    bacteria = pd.read_csv(file)

    malditof = bacteria[bacteria.columns.drop(list(bacteria.filter(regex='[^0-9]')))]

    if "species" in bacteria.columns:
        species = bacteria["species"][0]
        antibiotics = antibiotic_dictionary[species]
    else:
        antibiotics = list(bacteria.columns.difference(malditof.columns))

    trimmed_bac = pd.DataFrame(np.column_stack([malditof, bacteria[antibiotics]]))
    trimmed_bac.columns = list(malditof.columns) + antibiotics

    scrubbed_bac = trimmed_bac.dropna()

    value_counts = scrubbed_bac[antibiotics].value_counts()
    df_value_counts = value_counts.rename("Count").to_frame().reset_index()
    to_drop = df_value_counts.loc[df_value_counts["Count"] < min_instances].drop("Count", axis=1)
    reduced_aux_bac = pd.merge(scrubbed_bac, to_drop, indicator=True, how='outer', on=antibiotics)
    reduced_bac = reduced_aux_bac.loc[reduced_aux_bac["_merge"] == "left_only"].drop("_merge", axis=1)

    x = reduced_bac[reduced_bac.columns.drop(list(reduced_bac.filter(regex='[^0-9]')))]
    y = reduced_bac[antibiotics]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0, stratify=y[antibiotics])

    minmax_scaler = MinMaxScaler()
    normalized_x_train = minmax_scaler.fit_transform(x_train)
    normalized_x_test = minmax_scaler.transform(x_test)

    train = pd.DataFrame(np.column_stack([normalized_x_train, y_train]))
    train.columns = list(malditof.columns) + antibiotics

    test = pd.DataFrame(np.column_stack([normalized_x_test, y_test]))
    test.columns = list(malditof.columns) + antibiotics

    file_name_ext = os.path.basename(file)
    file_name = os.path.splitext(file_name_ext)[0]
    ext = os.path.splitext(file_name_ext)[1]
    train_name = processed_folder+"train_"+file_name+ext
    test_name = processed_folder+"test_"+file_name+ext

    train.to_csv(train_name, index=False, mode='w')
    test.to_csv(test_name, index=False, mode='w')

    print("Done.\n")