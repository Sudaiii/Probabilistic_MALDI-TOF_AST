import sys
import pandas as pd 

from PySide6.QtWidgets import QMainWindow

from PIL.ImageQt import ImageQt

import pyqtgraph as pg

from .ui.ui_results_window import Ui_Results

from classification.classificator import Classificator



class Results(QMainWindow):
    def __init__(self, file, data, bacteria, algorithm="MLP", bin_size=5):
        super(Results, self).__init__()

        # Variable initialization
        self.file = file
        self.X = data
        self.bacteria = bacteria
        self.algorithm = algorithm
        self.bin_size = bin_size

        path = self.file.split("/")
        file_name = path[len(path)-1]

        # Classificator initialization
        self.classificator = Classificator(bacteria, algorithm, bin_size)
        self.results = self.classificator.classify(data)

        # UI initialization
        self.ui = Ui_Results()
        self.ui.setupUi(self, self.results)

        self.ui.file_name_label.setText(file_name)
        self.ui.bacteria_name_label.setText(bacteria)
        
        pen = pg.mkPen(color=(58, 125, 173), width=2)
        self.ui.ms_graph.plot(self.X["mass"], self.X["intensity"], pen=pen)