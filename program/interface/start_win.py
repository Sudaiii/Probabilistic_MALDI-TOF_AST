import sys
import json
import pandas as pd

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog

from qt_material import apply_stylesheet

import pyqtgraph as pg

from .ui.ui_start_window import Ui_Start

from .config_win import Config
from .results_win import Results
from .results_multiple_win import ResultsMulti

from classification.processing_utils import read_file

from variables import RESOURCE_PATH



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.algorithm = "MLP"
        self.bin_size = 5

        # UI initialization
        self.ui = Ui_Start()
        self.ui.setupUi(self)

        self.setWindowTitle("MALDI-TOF MS AST")


        self.__load_combo_box()

        # Button setup
        self.ui.config_button.clicked.connect(self.deploy_config)
        self.ui.start_button.clicked.connect(self.deploy_results)
        self.ui.browse_button.clicked.connect(self.browse_files)

        self.ui.start_button.setEnabled(False)


    def __load_combo_box(self):
        antibiotic_dictionary_file = open(RESOURCE_PATH+"antibiotics.json", "r")
        antibiotic_dictionary = json.load(antibiotic_dictionary_file)
        i = 0
        for bac_key in antibiotic_dictionary.keys():
            self.ui.bacteria_select.addItem(bac_key)
            self.ui.bacteria_select.setItemData(i, bac_key)
            i+=1


    def browse_files(self):
        self.ui.start_button.setEnabled(False)
        self.file_addresses = QFileDialog.getOpenFileNames(
            self,
            'Buscar Archivo',
            '',
            'MALDI-TOF MS Data (*.csv *.txt)'
        )[0]
        if len(self.file_addresses) > 0:
            self.X = read_file(self.file_addresses[0])

            pen = pg.mkPen(color=(58, 125, 173), width=2)
            self.ui.ms_graph.clear()
            self.ui.ms_graph.plot(self.X["mass"], self.X["intensity"], pen=pen)
            if len(self.file_addresses) == 1:
                path = self.file_addresses[0].split("/")
                self.ui.file_name.setText(path[len(path)-1])
            else:
                self.ui.file_name.setText(str(len(self.file_addresses))+" archivos")
            self.ui.start_button.setEnabled(True)


    def deploy_config(self):
        self.config = Config(self)
        self.config.show()


    def deploy_results(self):
        if len(self.file_addresses) == 1:
            self.results = Results(
                file=self.file_addresses[0], 
                data=self.X, 
                bacteria=self.ui.bacteria_select.currentData(), 
                algorithm=self.algorithm, 
                bin_size=self.bin_size
            )
            self.results.show()
        else:
            self.results = ResultsMulti(
                file_addresses=self.file_addresses, 
                bacteria=self.ui.bacteria_select.currentData(), 
                algorithm=self.algorithm, 
                bin_size=self.bin_size
            )
            self.results.show()


def launch():
    app = QApplication(sys.argv)
    #app.setWindowIcon(QIcon(resource_path('placeholder.ico')))
    
    apply_stylesheet(app, theme="dark_blue.xml", css_file="custom.css")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())