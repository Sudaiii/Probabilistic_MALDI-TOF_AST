import sys

from PyQt5.QtCore import QTranslator, QEvent, QThread, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import loadUi

from Interface.results_win import Results
from Interface.config_win import Config
from Interface.resource_handler import resource_path
from Interface.results_worker import ResultsWorker
from Interface.loading_worker import LoadingWorker

from Database.db_handler import DBHandler

from CV.cv_manager import CVManager

try:
    from ctypes import windll  # Only exists on Windows.
    my_app_id = 'andry.test.0.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
except ImportError(windll):
    pass


class Start(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(resource_path("Resources/qt5-tools/StartWindow2.ui"), self)
        self.setWindowTitle("Main Menu")

        self.db = DBHandler()

        self.image_addresses = []
        self.pill_size = 6.22
        self.pill_size_label.setText("Pill size: " + str(self.pill_size))

        self.results_thread = QThread()
        self.results_worker = None
        self.loading_worker = QThread()
        self.loading_thread = None

        self.results = None
        self.config = None

        self.tl = QTranslator(self)

        self.__load_combo_boxes()

        self.browse_button.clicked.connect(self.browse_files)
        self.start_button.clicked.connect(self.old_open_results_window)
        self.config_button.clicked.connect(self.deploy_config)
        self.language_select.currentIndexChanged.connect(self.change_func)
        self.family_select.currentIndexChanged.connect(self.family_changed)
        self.patient_name_edit.textChanged.connect(self.patient_name_edited)

        self.start_button.setEnabled(False)

        self.translate_ui()

    def __load_combo_boxes(self):
        languages = [
            ('English', ''),
            ('Português', 'en-pr'),
            ('Español', 'en-es')
        ]
        for i, (text, lang) in enumerate(languages):
            self.language_select.addItem(text)
            self.language_select.setItemData(i, lang)
        infection = self.db.get_infection()
        self.__load_combo_box(self.infection_select, infection)
        families = self.db.get_family()
        self.__load_combo_box(self.family_select, families)
        bacteria = self.db.get_family_bacteria(self.family_select.itemData(0))
        self.__load_combo_box(self.bacteria_select, bacteria)

    @staticmethod
    def __load_combo_box(combo_box, lst):
        for i in range(len(lst)):
            combo_box.addItem(lst[i][1])
            combo_box.setItemData(i, lst[i][0])

    def family_changed(self):
        self.bacteria_select.setCurrentIndex(0)
        self.bacteria_select.clear()
        bacteria = self.db.get_family_bacteria(self.family_select.currentData())
        self.__load_combo_box(self.bacteria_select, bacteria)

    def patient_name_edited(self):
        if len(self.image_addresses) > 0:
            self.start_button.setEnabled(True)
        if len(self.patient_name_edit.text()) <= 0:
            self.start_button.setEnabled(False)

    def browse_files(self):
        self.image_addresses = QFileDialog.getOpenFileNames(
            self,
            'Open file',
            '',
            'Images (*.png *.jpg *.jpeg);;PNG (*.png);;JPEG (*.jpg *.jpeg)'
        )[0]
        if len(self.image_addresses) > 0:
            if len(self.image_addresses) == 1:
                path = self.image_addresses[0].split("/")
                file = path[len(path)-1]
                self.file_name.setText(file)
                pixmap = QPixmap(self.image_addresses[0])
            else:
                number_of_images = str(len(self.image_addresses))
                self.file_name.setText(number_of_images + " images")
                pixmap = QPixmap(resource_path("Resources/Images/more.png"))
            self.image_label.setPixmap(pixmap.scaled(self.image_label.height(), self.image_label.width()))
            if len(self.patient_name_edit.text()) > 0:
                self.start_button.setEnabled(True)

    def old_open_results_window(self):
        config = [
            self.family_select.currentData(), self.bacteria_select.currentData(), self.infection_select.currentData()
        ]
        cv_manager = CVManager(self.image_addresses[0], self.pill_size)
        self.results = Results(self.image_addresses, self.patient_name_edit.text(), config, self.pill_size, cv_manager)
        self.results.show()

    def deploy_results(self):
        # TODO: change to disable ALL buttons (make a method)
        # TODO: Implement new loading process
        self.start_button.setEnabled(False)

        self.results_worker = ResultsWorker(self.image_addresses[0], self.pill_size)
        self.results_thread = QThread()
        self.link_worker_thread(self.results_worker, self.results_thread)
        self.results_thread.finished.connect(self.__open_results_window)

        self.loading_worker = LoadingWorker(self.loading_label)
        self.loading_thread = QThread()
        self.link_worker_thread(self.loading_worker, self.loading_thread)

        self.results_thread.start()
        self.loading_thread.start()

    def __open_results_window(self):
        self.loading_worker.working = False

        config = [
            self.family_select.currentData(), self.bacteria_select.currentData(), self.infection_select.currentData()
        ]
        cv_manager = self.results_worker.cv_manager
        self.results = Results(self.image_addresses, self.patient_name_edit.text(), config, self.pill_size, cv_manager)
        self.results.show()
        self.loading_label.setText("")

        self.start_button.setEnabled(True)

        self.results_worker.deleteLater()
        self.results_thread.deleteLater()

    @staticmethod
    def link_worker_thread(worker, thread):
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)



    def deploy_config(self):
        self.config = Config(self.pill_size, self)
        self.config.show()

    def update_config(self, pill_size):
        self.pill_size = pill_size
        self.pill_size_label.setText("Pill size: " + str(self.pill_size))

    @pyqtSlot(int)
    def change_func(self, index):
        lan = self.language_select.itemData(index)
        if lan:
            self.tl.load(resource_path(lan))
            QApplication.instance().installTranslator(self.tl)
        else:
            QApplication.instance().removeTranslator(self.tl)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.translate_ui()
        super(Start, self).changeEvent(event)

    def translate_ui(self):
        self.browse_button.setText(QApplication.translate('Start', 'Browse'))
        self.start_button.setText(QApplication.translate('Start', 'Start'))


def launch():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path('placeholder.ico')))
    win = Start()
    win.show()
    sys.exit(app.exec_())
