import json
import joblib
from os.path import exists

from variables import RESOURCE_PATH
from .processing_utils import preprocess



MODEL_PATH = RESOURCE_PATH+"models/"



class Classificator():
    def __init__(self, bacteria="Klebsiella pneumoniae", algorithm="MLP", bin_size=5):
        self.bacteria = bacteria

        bacteria_dictionary_file = open(RESOURCE_PATH+"bacteria.json", "r")
        bacteria_dictionary = json.load(bacteria_dictionary_file)
        self.bacteria_alias = bacteria_dictionary[self.bacteria]

        self.algorithm = algorithm
        self.bin_size = bin_size

        self.model_load()
        

    def model_load(self):
        model_file = self.bacteria_alias+"_driams_bin"+str(self.bin_size)+"_"+self.algorithm.lower()+"_standard_lps.joblib"
        self.model = joblib.load(MODEL_PATH+model_file)

    def classify(self, file):
        X = preprocess(file, self.bacteria_alias, self.bin_size)
        return self.model.predict(X)



# Classificator().visualize("D:/Development/Projects/Probabilistic_MALDI-TOF_AST/data/program/k_pneumoniae_sample.csv")