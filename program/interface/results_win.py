import sys
import pandas as pd 

from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QPixmap

from PIL.ImageQt import ImageQt

from .ui.ui_results_window import Ui_Results

from classification.classificator import Classificator
from classification.visualization_utils import visualize




class Results(QMainWindow):
    def __init__(self, file, bacteria, algorithm="MLP", bin_size=5):
        super(Results, self).__init__()

        # Variable initialization
        self.file = file
        self.bacteria = bacteria
        self.algorithm = algorithm
        self.bin_size = bin_size

        path = self.file.split("/")
        file_name = path[len(path)-1]

        # Classificator initialization
        self.classificator = Classificator(bacteria, algorithm, bin_size)

        # UI initialization
        self.ui = Ui_Results()
        self.ui.setupUi(self)

        self.ui.file_label.setText("Archivo: " + file_name)
        self.ui.bacteria_label.setText("Bacteria: " + bacteria)
        self.ui.model_label.setText("Algoritmo: " + algorithm)
        self.ui.binning_label.setText("Binning: " + str(bin_size))

        self.ui.s_antibiotic_1_label.setText("Classification:")
        self.ui.s_proba_1_label.setText(str(self.classificator.classify(file)))

        x = pd.read_csv(self.file)
        im = visualize(x)
        qim = ImageQt(im)
        pix = QPixmap.fromImage(qim)
        self.ui.spectrometry_label.setPixmap(pix)
