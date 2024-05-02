import pandas as pd
import numpy as np

import joblib

from sklearn.preprocessing import MinMaxScaler, StandardScaler

SCALERS_LOCATION = "../data/processed/binned/standard/scaler/"


def preprocess(file, bacteria, bin_size):
    X = malditofms_to_pd(file)
    X = bin(X, bin_size)
    X = normalize(X, bacteria, bin_size)
    return X

def malditofms_to_pd(file):
    #...
    X = pd.read_csv(file)
    return X

def bin(X, bin_size):
    binned_X = X.T.groupby(np.arange(len(X.columns)) // bin_size).mean().T
    binned_X.columns = [str(col) for col in range(int(X.columns[0]), int(X.columns[-1]), bin_size)]
    return binned_X

def normalize(X, bacteria, bin_size):
    scaler = joblib.load(SCALERS_LOCATION+bacteria+"_driams_bin"+str(bin_size)+".save")
    scaled_X = scaler.transform(X)
    scaled_X = pd.DataFrame(scaled_X, columns=X.columns)
    return scaled_X

