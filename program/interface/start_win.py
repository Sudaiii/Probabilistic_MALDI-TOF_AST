import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QFile
from PySide6.QtGui import QPixmap, QIcon

from .ui.ui_start_window import Ui_Start

from .config_win import Config
from .results_win import Results

from classification.classificator import Classificator

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Start()
        self.ui.setupUi(self)

        self.ui.config_button.clicked.connect(self.deploy_config)
        self.ui.start_button.clicked.connect(self.deploy_results)
        self.ui.browse_button.clicked.connect(self.browse_files)

        self.classificator = Classificator()

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
            self.classificator.visualize(self.file_address)
            # pixmap = QPixmap(self.image_addresses[0])


    def deploy_config(self):
        self.config = Config()
        self.config.show()

    def deploy_results(self):
        self.results = Results()
        self.results.show()


def launch():
    app = QApplication(sys.argv)
    #app.setWindowIcon(QIcon(resource_path('placeholder.ico')))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())