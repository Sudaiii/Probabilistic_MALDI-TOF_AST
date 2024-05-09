import sys
import json
import pandas as pd

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QFile
from PySide6.QtGui import QPixmap, QIcon

from PIL.ImageQt import ImageQt

from .ui.ui_start_window import Ui_Start

from .config_win import Config
from .results_win import Results

from classification.visualization_utils import visualize

from variables import RESOURCE_PATH

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.algorithm = "MLP"
        self.bin_size = 5

        # UI initialization
        self.ui = Ui_Start()
        self.ui.setupUi(self)

        self.ui.model_label.setText("Algoritmo: " + self.algorithm)
        self.ui.binning_label.setText("Binning: " + str(self.bin_size))

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
        self.file_address = QFileDialog.getOpenFileName(
            self,
            'Buscar Archivo',
            '',
            'Tabulated data (*.csv *.xlsx)'
        )[0]
        if len(self.file_address) > 0:
            path = self.file_address.split("/")
            file = path[len(path)-1]
            self.ui.file_name.setText(file)
            x = pd.read_csv(self.file_address)
            im = visualize(x)
            qim = ImageQt(im)
            pix = QPixmap.fromImage(qim)
            self.ui.ms_image.setPixmap(pix)
            self.ui.start_button.setEnabled(True)

    def deploy_config(self):
        self.config = Config()
        self.config.show()

    def deploy_results(self):
        self.results = Results(file=self.file_address, bacteria=self.ui.bacteria_select.currentData(), algorithm=self.algorithm, bin_size=self.bin_size)
        self.results.show()


def launch():
    app = QApplication(sys.argv)
    #app.setWindowIcon(QIcon(resource_path('placeholder.ico')))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())