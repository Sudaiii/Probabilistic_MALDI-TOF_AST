from processing_utils import preprocess
from visualization_utils import spectrometry


class Classificator():
    def __init__(self, bacteria="k_pneumoniae", algorithm="mlp", bin_size=20):
        self.bacteria = bacteria
        self.algorithm = algorithm
        self.bin_size = bin_size

        self.model = "abc"
    
    def visualize(self, file):
        X = preprocess(file, self.bacteria, self.bin_size)
        if len(X) > 1:
            X = X.iloc[[0]]
        spectrometry(X)
        

    def classify(self, file):
        X = preprocess(file, self.bacteria, self.bin_size)
        return self.model.predict_proba(X)



Classificator().visualize("D:/Development/Projects/Probabilistic_MALDI-TOF_AST/data/program/k_pneumoniae_sample.csv")