from PySide6.QtWidgets import QDialog
from .ui.ui_config_window import Ui_Config

class Config(QDialog):
    def __init__(self):
        super(Config, self).__init__()
        self.ui = Ui_Config()
        self.ui.setupUi(self)
        self.setWindowTitle("Configuration")

        self.ui.confirm_button.clicked.connect(self.confirm_changes)

    def confirm_changes(self):
        self.close()