from PySide6.QtWidgets import QMainWindow

import pyqtgraph as pg

from .ui.ui_results_window import Ui_Results

from classification.classificator import Classificator
from reporting.pdf_gen import generate_individual_pdf



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
        self.file_name = path[len(path)-1]

        # Classificator initialization
        self.classificator = Classificator(bacteria, algorithm, bin_size)
        self.results = self.classificator.classify(data)

        # UI initialization
        self.ui = Ui_Results()
        self.ui.setupUi(self, self.results)

        self.ui.file_name_label.setText(self.file_name)
        self.ui.bacteria_name_label.setText(bacteria)
        
        pen = pg.mkPen(color=(58, 125, 173), width=2)
        self.ui.ms_graph.plot(self.X["mass"], self.X["intensity"], pen=pen)

        self.ui.export_button.clicked.connect(self.__generate_report)


    def __generate_report(self):
        generate_individual_pdf(self.X, self.results, self.file_name, self.bacteria, self.algorithm, self.bin_size)