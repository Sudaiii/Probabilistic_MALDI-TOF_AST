import json
import joblib
from os.path import exists

from variables import RESOURCE_PATH
from .processing_utils import preprocess_data


MODEL_PATH = RESOURCE_PATH+"models/"



class Classificator():
    def __init__(self, bacteria="Klebsiella pneumoniae", algorithm="MLP", bin_size=5):
        self.bacteria = bacteria
        self.algorithm = algorithm
        self.bin_size = bin_size

        self.load_files()
        

    def load_files(self):
        bacteria_dictionary_file = open(RESOURCE_PATH+"bacteria.json", "r")
        bacteria_dictionary = json.load(bacteria_dictionary_file)
        self.bacteria_alias = bacteria_dictionary[self.bacteria]

        model_file = self.bacteria_alias+"_driams_bin"+str(self.bin_size)+"_"+self.algorithm.lower()+"_standard_lps.joblib"
        self.model = joblib.load(MODEL_PATH+model_file)

        lc_file = self.bacteria_alias+"_driams_bin"+str(self.bin_size)+"_encoder.save"
        self.lc = joblib.load(RESOURCE_PATH+"/encoder/"+lc_file)
        self.classes = self.lc.classes_

        antibiotics_file = open(RESOURCE_PATH+"antibiotics.json", "r")
        antibiotic_dictionary = json.load(antibiotics_file)
        self.antibiotics = antibiotic_dictionary[self.bacteria]


    def classify(self, data):
        X = preprocess_data(data, self.bacteria_alias, self.bin_size)
        proba = self.model.predict_proba(X)
        
        antibiotic_proba = self.__probability_dictionary()
    
        for i in range(len(proba[0])):
            class_proba = proba[0][i]
            class_antibiotics = list(self.classes[i])
            for j in range(len(class_antibiotics)):
                if class_antibiotics[j] == "0":
                    antibiotic_proba[self.antibiotics[j]] += class_proba

        sorted_antibiotic_proba = {k: v for k, v in sorted(antibiotic_proba.items(), key=lambda item: item[1], reverse=True)}
        return sorted_antibiotic_proba
            

    def __probability_dictionary(self):
        antibiotic_proba = {}
        for antibiotic in self.antibiotics:
            antibiotic_proba[antibiotic] = 0
        return antibiotic_proba