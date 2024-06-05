from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton
from PySide6.QtCore import QSignalMapper, Slot

from .ui.ui_results_multiple_window import Ui_Results_Multi

from reporting.pdf_gen import generate_table_pdf
from classification.classificator import Classificator
from classification.processing_utils import read_file
from .results_win import Results



class ResultsMulti(QMainWindow):
    def __init__(self, file_addresses, bacteria, algorithm="MLP", bin_size=5):
        super(ResultsMulti, self).__init__()

        # Variable initialization
        self.num_files = len(file_addresses)
        self.file_addresses = file_addresses
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
        self.ui.setupUi(self, self.results)
        self.ui.bacteria_name_label.setText(bacteria)
        self.__fill_table()

        self.ui.report_button.clicked.connect(self.__generate_report)


    def __obtain_results(self):
        for file_address in self.file_addresses:
            path = file_address.split("/")
            file_name = path[len(path)-1]
            self.file_names.append(file_name)

            X = read_file(file_address)
            self.X_data.append(X)

            results = self.classificator.classify(X)
            self.results.append(results)


    def __fill_table(self):
        self.signal_mapper = QSignalMapper(self.ui.centralwidget)
        self.signal_mapper.mappedInt.connect(self.__visualize_is_pressed)

        headers = ["File"]
        for key in self.results[0].keys():
            headers.append(key)

        self.pdf_table = [
            headers
        ]        

        for i in range(len(self.results)):
            pdf_row = []

            max_value = 0
            max_labels = []
                
            # Set file name
            file_cell = QLabel(self.ui.centralwidget)
            file_cell.setText(self.file_names[i])
            self.ui.results_table.setCellWidget(i, 0, file_cell)

            pdf_row.append(self.file_names[i])

            # Set results for each antibiotic
            j = 1
            for antibiotic in self.results[i]:
                antibiotic_cell = QLabel(self.ui.centralwidget)
                rounded_proba = round(self.results[i][antibiotic], 4)

                if rounded_proba > max_value:
                    max_value = self.results[i][antibiotic]
                    max_labels = []
                    max_labels.append(antibiotic_cell)
                elif rounded_proba == max_value:
                    max_labels.append(antibiotic_cell)

                antibiotic_cell.setText(f"{rounded_proba*100:.2f}%")
                self.ui.results_table.setCellWidget(i, j, antibiotic_cell)

                pdf_row.append(f"{rounded_proba*100:.2f}%")

                j += 1

            for label in max_labels:
                label.setStyleSheet("color: green;")

            # Set visualize buttons
            button = QPushButton()
            button.setText("Visualizar")
            button.clicked.connect(self.signal_mapper.map)
            self.signal_mapper.setMapping(button, i)            

            self.ui.results_table.setCellWidget(i, j, button)

            self.pdf_table.append(pdf_row)


    @Slot(int)   
    def __visualize_is_pressed(self, i):
        self.results = Results(
                file=self.file_addresses[i], 
                data=self.X_data[i], 
                bacteria=self.bacteria, 
                algorithm=self.algorithm, 
                bin_size=self.bin_size
            )
        self.results.show()

    
    def __generate_report(self):
        generate_table_pdf(self.pdf_table, self.bacteria, self.algorithm, self.bin_size)