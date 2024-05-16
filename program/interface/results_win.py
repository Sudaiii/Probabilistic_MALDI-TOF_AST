import sys
import pandas as pd 

from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QPixmap

from PIL.ImageQt import ImageQt

import pyqtgraph as pg

from .ui.ui_results_window import Ui_Results

from classification.classificator import Classificator
from classification.visualization_utils import melt_data



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

        self.ui.file_label.setText("Archivo: " + file_name)
        self.ui.bacteria_label.setText("Bacteria: " + bacteria)
        self.ui.model_label.setText("Algoritmo: " + algorithm)
        self.ui.binning_label.setText("Binning: " + str(bin_size))
        
        melt_X = melt_data(self.X)

        pen = pg.mkPen(color=(58, 125, 173), width=2)
        self.ui.spectrometry_label.plot(melt_X["Da"], melt_X["Value"], pen=pen)
