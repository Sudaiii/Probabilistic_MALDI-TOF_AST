import sys
from PySide6.QtWidgets import QApplication, QMainWindow

from .ui.ui_results_window import Ui_Results

from .config_win import Config

class Results(QMainWindow):
    def __init__(self):
        super(Results, self).__init__()
        self.ui = Ui_Results()
        self.ui.setupUi(self)