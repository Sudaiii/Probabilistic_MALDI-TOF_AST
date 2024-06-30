import pandas as pd
import io

import joblib

from variables import RESOURCE_PATH



SCALERS_LOCATION = RESOURCE_PATH+"scalers/"



def read_file(file):
    # Contents are read
    if(file.endswith(".txt")):
        X = __raw_ms_to_pd(file)
    elif(file.endswith(".csv")):
        X = __preprocessed_ms_to_pd(file)
    # Columns are renamed for convenience
    X.columns = ["mass", "intensity"]
    # Data is converted into float
    X["mass"] = X["mass"].astype(float)
    X["intensity"] = X["intensity"].astype(float)
    # Filtered down to relevant Da range
    X = X[(X["mass"] >= 2000) & (X["mass"] < 10000)]
    X = X.reset_index(drop=True)
    return X


def __raw_ms_to_pd(file):
    contents = open(file, "r")
    data = [line for line in contents.readlines() if "#" not in line]
    X = pd.read_csv(io.StringIO("".join(data)), sep=" ")
    X = X.reset_index(drop=True)
    return X


def __preprocessed_ms_to_pd(file):
    X = pd.read_csv(file)
    X = X.T.reset_index(drop=False)
    return X


def bin(X, bin_size):
    binned_X = X.copy(deep=True)
    # Rows are binned
    binned_X["bin"] = pd.cut(
        binned_X["mass"], 
        bins=range(2000, 10000+bin_size, bin_size), 
        labels=range(2000, 10000, bin_size), 
        right=False
    )
    binned_X = binned_X.drop(["mass"], axis=1)
    # Mean value of each bin is calculated
    binned_X = binned_X.groupby(["bin"], observed=False).mean().reset_index(drop=False)
    # Data is transposed
    binned_X = binned_X.set_index("bin").T.reset_index(drop=True)
    return binned_X


def normalize(X, bacteria, bin_size):
    # Prebuilt scaler is loaded
    scaler = joblib.load(SCALERS_LOCATION+bacteria+"_driams_bin"+str(bin_size)+".save")
    # Data is normalized
    scaled_X = scaler.transform(X)
    scaled_X = pd.DataFrame(scaled_X, columns=X.columns)

    return scaled_X


def preprocess_data(data, bacteria, bin_size):
    data = bin(data, bin_size)
    data = normalize(data, bacteria, bin_size)
    return data