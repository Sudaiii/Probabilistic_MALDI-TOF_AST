from PySide6.QtWidgets import QMainWindow

from .ui.ui_results_multiple_window import Ui_Results_Multi

from classification.classificator import Classificator
from classification.processing_utils import read_file



class ResultsMulti(QMainWindow):
    def __init__(self, files, bacteria, algorithm="MLP", bin_size=5):
        super(ResultsMulti, self).__init__()

        # Variable initialization
        self.num_files = len(files)
        self.files = files
        self.bacteria = bacteria
        self.algorithm = algorithm
        self.bin_size = bin_size

        self.file_names = []
        self.X_data = []
        self.results = []

        # Classificator initialization
        self.classificator = Classificator(bacteria, algorithm, bin_size)

        # Get results
        self.__obtain_results()

        # UI initialization
        self.ui = Ui_Results_Multi()
        self.ui.setupUi(self, self.file_names, self.results)
        self.ui.bacteria_name_label.setText(bacteria)
        

    def __obtain_results(self):
        for file_address in self.files:
            path = file_address.split("/")
            file_name = path[len(path)-1]
            self.file_names.append(file_name)

            X = read_file(file_address)
            self.X_data.append(X)

            results = self.classificator.classify(X)
            self.results.append(results)
