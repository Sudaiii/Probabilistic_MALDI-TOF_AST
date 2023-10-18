import os
import json
import pandas as pd
import xgboost as xgb
from sklearn.feature_selection import RFE


antibiotic_dictionary_file = open("data/antibiotics.json", "r")
antibiotic_dictionary = json.load(antibiotic_dictionary_file)

processed_raw_folder = "data/processed/raw/"
selected_features_folder = "data/features"
processed_raw_files = os.listdir(processed_raw_folder)
processed_raw_files = [x for x in processed_raw_files if "test" not in x]
processed_raw_file_paths = [processed_raw_folder + file for file in processed_raw_files]

for file in processed_raw_file_paths:
    print("Processing", file)
    bacteria = pd.read_csv(file)

    x_train = bacteria[bacteria.columns.drop(list(bacteria.filter(regex='[^0-9]')))]
    y_train = bacteria[bacteria.columns.drop(x_train.columns)]

    selector = RFE(
        estimator=xgb.XGBClassifier(objective="binary:logistic"),
        n_features_to_select=100,
        step=100,
        verbose=1
    )
    selector.fit(x_train, y_train)
    
    mask = selector.support_
    columns = x_train.columns
    selected_features = []
    for i in range(columns.size):
        if mask[i] == True:
            selected_features.append(columns[i])

    file_name_ext = os.path.basename(file)
    file_name = os.path.splitext(file_name_ext)[0]
    file_name_cleaned = file_name.replace("train_", "") 
    feature_file_address = "data/features/"+file_name_cleaned+"_selected_features.txt"
    feature_file = open(feature_file_address, "w")
    for feature in selected_features:
        feature_file.write(feature+",")
    feature_file.close()

    print("Done.\n")