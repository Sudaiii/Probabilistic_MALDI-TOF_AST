import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile

from .ui.ui_start_window import Ui_Start

from .config_win import Config

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Start()
        self.ui.setupUi(self)

        self.ui.config_button.clicked.connect(self.deploy_config)


    def deploy_config(self):
        self.config = Config()
        self.config.show()


def launch():
    app = QApplication(sys.argv)
    #app.setWindowIcon(QIcon(resource_path('placeholder.ico')))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())