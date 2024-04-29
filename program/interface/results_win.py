from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PIL.ImageQt import ImageQt

from Interface.num_delegate import NumDelegate
from Interface.resource_handler import resource_path

from CV.cv_manager import CVManager

from Database.db_handler import DBHandler
from Database.pill_manager import PillManager

from Summarizer.pdf_generator import generate_report


# TODO: On change of combo pill item, update resistance
class ComboPills(QComboBox):
    def __init__(self, pill_manager):
        super().__init__()
        self.addItems(pill_manager.get_pill_acronyms())


class Results(QDialog):
    def __init__(self, image_addresses, patient_name, config, real_pill_size_mm, cv_manager):
        super().__init__()
        loadUi(resource_path("Resources/qt5-tools/ResultsWindow.ui"), self)
        self.setWindowTitle("Results")

        self.results_table.itemClicked.connect(self.table_updated)
        self.report_button.clicked.connect(self.generate_report)
        self.next_button.clicked.connect(self.next_image)

        # Set delegate so that modifiable field only accepts numbers
        num_delegate = NumDelegate(self.results_table)
        self.results_table.setItemDelegate(num_delegate)

        self.config = config
        self.db = DBHandler()
        self.pill_manager = PillManager(self.db, config)

        self.patient_name = patient_name

        self.image_addresses = image_addresses
        self.image_address = self.image_addresses[0]
        self.image_index = 1
        self.real_pill_size_mm = real_pill_size_mm
        if len(image_addresses) == 1:
            self.next_button.setEnabled(False)
        self.page_number.setText(str(self.image_index) + "/" + str(len(self.image_addresses)))

        # Requesting data of the circles in the image
        self.cv_manager = cv_manager
        pil_image = self.cv_manager.output_image()
        diameters = self.cv_manager.halo_diameters_mm()
        initial_acronyms = self.cv_manager.initial_acronyms()
        qt_image = ImageQt(pil_image)
        pixmap = QPixmap.fromImage(qt_image)
        self.results_size = 700
        self.results_image.setPixmap(pixmap.scaled(self.results_size, self.results_size))

        self.fill_table(diameters, initial_acronyms)

    # TODO: Update to use threads
    def next_image(self):
        pixmap = QPixmap("")
        self.check.setPixmap(pixmap.scaled(self.check.height(), self.check.width()))
        if self.image_index < len(self.image_addresses):
            self.image_address = self.image_addresses[self.image_index]

            self.cv_manager = CVManager(self.image_address, self.real_pill_size_mm)
            pil_image = self.cv_manager.output_image()
            diameters = self.cv_manager.halo_diameters_mm()
            initial_acronyms = self.cv_manager.initial_acronyms()
            qt_image = ImageQt(pil_image)
            pixmap = QPixmap.fromImage(qt_image)
            self.results_size = 700
            self.results_image.setPixmap(pixmap.scaled(self.results_size, self.results_size))

            self.fill_table(diameters, initial_acronyms)

            self.image_index += 1
            self.page_number.setText(str(self.image_index) + "/" + str(len(self.image_addresses)))
        if self.image_index >= len(self.image_addresses):
            self.next_button.setEnabled(False)

    def fill_table(self, circle_diameters, acronyms):
        self.results_table.setRowCount(len(circle_diameters))
        for i in range(len(circle_diameters)):
            combo_pills = ComboPills(self.pill_manager)
            closest_match = self.pill_manager.find_closest_match(acronyms[i])
            self.results_table.setCellWidget(i, 0, combo_pills)
            acronym_index = self.results_table.cellWidget(i, 0).findText(closest_match, Qt.MatchFixedString)
            if acronym_index >= 0:
                self.results_table.cellWidget(i, 0).setCurrentIndex(acronym_index)
            diameter = QTableWidgetItem(str(circle_diameters[i]))
            self.results_table.setItem(i, 1, diameter)

            resistance = self.pill_manager.check_resistance(combo_pills.currentText(), circle_diameters[i])
            resistant = QTableWidgetItem(resistance)
            resistant.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.results_table.setItem(i, 2, resistant)

            checkbox = QTableWidgetItem()
            checkbox.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            checkbox.setCheckState(Qt.CheckState.Checked)
            self.results_table.setItem(i, 3, checkbox)

        self.results_table.itemChanged.connect(self.table_updated)

    def table_updated(self):
        pixmap = QPixmap("")
        self.check.setPixmap(pixmap.scaled(self.check.height(), self.check.width()))
        updated_circles = []
        for row in range(self.results_table.rowCount()):
            name = self.results_table.cellWidget(row, 0).currentText()
            diameter = float(self.results_table.item(row, 1).text())
            resistance = self.pill_manager.check_resistance(name, diameter)
            check_state = self.results_table.item(row, 3).checkState()
            if check_state == 2:
                show = True
            else:
                show = False
            self.results_table.item(row, 2).setText(resistance)
            circle = [diameter, show]
            updated_circles.append(circle)

        pil_image = self.cv_manager.update_data(updated_circles)
        qt_image = ImageQt(pil_image)
        pixmap = QPixmap.fromImage(qt_image)
        self.results_image.setPixmap(pixmap.scaled(self.results_image.size()))

    def generate_report(self):
        report_data = []
        for row in range(self.results_table.rowCount()):
            name = self.results_table.cellWidget(row, 0).currentText()
            diameter = self.results_table.item(row, 1).text()
            resistance = self.results_table.item(row, 2).text()
            row_of_data = [name, diameter, resistance]
            report_data.append(row_of_data)
        path = self.image_address.split("/")
        file = path[len(path) - 1]
        image_name = file.split(".")[0]
        pixmap = QPixmap("Resources/Images/check.png")
        self.check.setPixmap(pixmap.scaled(self.check.height(), self.check.width()))

        generate_report(report_data, self.patient_name, self.patient_name)
