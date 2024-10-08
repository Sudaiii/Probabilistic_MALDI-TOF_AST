import os
import json
import argparse

import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from oversampling import random_oversampling, smote_tomek_oversampling

import joblib


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--Folder", help="What folder to get the data from", default="binned")
parser.add_argument("-n", "--Norm", help="Data normalization method. Supports \"none\",\"min-max\" and \"standard\"", default="standard", choices=["none", "min-max", "standard"])
parser.add_argument("-o", "--Oversampling", help="Method used to oversample data. Supports \"none\", \"random\" and \"smotetomek\"", default="none", choices=["none", "random", "smotetomek"])
parser.add_argument("-s", "--Split", help="How to do the split. Supports 80-20 and 5x2", default="standard", choices=["80-20", "5x2"])
parser.add_argument("-c", "--Filter", help="Use only files with specific string in their name")
args = parser.parse_args()


unprocessed_folder = "data/unprocessed/"+args.Folder+"/"
processed_folder = "data/processed/"+args.Folder+"/"+args.Oversampling+"/"+args.Norm+"/"


if not os.path.exists(processed_folder):
    os.makedirs(processed_folder)

print("Saving at",  processed_folder)

antibiotic_dictionary_file = open("data/antibiotics.json", "r")
antibiotic_dictionary = json.load(antibiotic_dictionary_file)

unprocessed_files = os.listdir(unprocessed_folder)
unprocessed_file_paths = [unprocessed_folder + file for file in unprocessed_files]

if args.Filter is not None:
    unprocessed_file_paths = [file for file in unprocessed_file_paths if args.Filter in file]

if args.Split == "5x2":
    seeds = [0, 1, 2, 3, 4]
    min_instances = 2
else:
    seeds = [0]
    min_instances = 5

for seed in seeds:
    for file in unprocessed_file_paths:
        print("Processing", file)
        bacteria = pd.read_csv(file)

        file_name_ext = os.path.basename(file)
        file_name = os.path.splitext(file_name_ext)[0]
        ext = os.path.splitext(file_name_ext)[1]

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

        if args.Split == "5x2":
            test_size = 0.5
        else:
            test_size = 0.2

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=seed, stratify=y[antibiotics])

        if args.Norm:
            if args.Norm == "min-max":
                scaler = MinMaxScaler()
            elif args.Norm == "standard":
                scaler = StandardScaler()
            x_train = scaler.fit_transform(x_train)
            x_test = scaler.transform(x_test)

            if not os.path.exists(processed_folder+"scaler/"):
                os.makedirs(processed_folder+"scaler/")

            if args.Split == "5x2":
                joblib.dump(scaler, processed_folder+"scaler/"+str(seed)+"_"+file_name+".save")
            else:
                joblib.dump(scaler, processed_folder+"scaler/"+file_name+".save")
        
        lc = LabelEncoder()

        agg_columns = pd.DataFrame()
        agg_columns["Class"] = y_train.astype(int).astype(str).agg(''.join, axis=1)
        agg_columns["Class"] = agg_columns["Class"].astype(str)
        lc.fit(agg_columns.values.ravel())

        if not os.path.exists(processed_folder+"encoder/"):
            os.makedirs(processed_folder+"encoder/")

        if args.Split == "5x2":
            joblib.dump(lc, processed_folder+"encoder/"+str(seed)+"_"+file_name+"_encoder.save")
        else:
            joblib.dump(lc, processed_folder+"encoder/"+file_name+"_encoder.save")

        if args.Oversampling:
            y_train_lps = lc.transform(agg_columns.values.ravel())
            
            if args.Oversampling == "random":
                x_train, y_train_lps = random_oversampling(x_train, y_train_lps)
            elif args.Oversampling == "smotetomek":
                x_train, y_train_lps = smote_tomek_oversampling(x_train, y_train_lps)

            y_train_agg = lc.inverse_transform(y_train_lps)
            
            y_train = []
            for instance in y_train_agg:
                y_train.append(list(instance))


        train = pd.DataFrame(np.column_stack([x_train, y_train]))
        train.columns = list(malditof.columns) + antibiotics

        test = pd.DataFrame(np.column_stack([x_test, y_test]))
        test.columns = list(malditof.columns) + antibiotics

        if args.Split == "5x2":
            train_name_a = processed_folder+"train_A__"+str(seed)+"_"+file_name+ext
            test_name_a = processed_folder+"test_A__"+str(seed)+"_"+file_name+ext

            train.to_csv(train_name_a, index=False, mode='w')
            test.to_csv(test_name_a, index=False, mode='w')

            train_name_b = processed_folder+"train_B__"+str(seed)+"_"+file_name+ext
            test_name_b = processed_folder+"test_B__"+str(seed)+"_"+file_name+ext

            test.to_csv(train_name_b, index=False, mode='w')
            train.to_csv(test_name_b, index=False, mode='w')
        else:
            train_name = processed_folder+"train_"+file_name+ext
            test_name = processed_folder+"test_"+file_name+ext

            train.to_csv(train_name, index=False, mode='w')
            test.to_csv(test_name, index=False, mode='w')

        print("Done.\n")