from PySide6.QtWidgets import QDialog
from .ui.ui_config_window import Ui_Config



SUPPORTED_BINS = [5, 20]
SUPPORTED_ALGORITHMS = ["MLP", "XGB", "RF"]



class Config(QDialog):
    def __init__(self, main_window):
        super(Config, self).__init__()
        self.main_window = main_window
        self.ui = Ui_Config()
        self.ui.setupUi(self)

        self.__load_combo_box()

        self.ui.binning_select.setCurrentIndex(self.ui.binning_select.findText(str(self.main_window.bin_size)))
        self.ui.model_select.setCurrentIndex(self.ui.model_select.findText(self.main_window.algorithm))

        self.ui.confirm_button.clicked.connect(self.confirm_changes)


    def __load_combo_box(self):
        i = 0
        for bin in SUPPORTED_BINS:
            self.ui.binning_select.addItem(str(bin))
            self.ui.binning_select.setItemData(i, bin)
            i+=1
        i = 0
        for algorithm in SUPPORTED_ALGORITHMS:
            self.ui.model_select.addItem(algorithm)
            self.ui.model_select.setItemData(i, algorithm)
            i+=1


    def confirm_changes(self):
        self.main_window.bin_size = self.ui.binning_select.currentData()
        self.main_window.algorithm = self.ui.model_select.currentData()
        self.close()