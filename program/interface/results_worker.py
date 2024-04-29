from PyQt5.QtCore import QObject, pyqtSignal

from CV.cv_manager import CVManager


class ResultsWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, image_address, pill_diameter_mm):
        super().__init__()
        self.image_address = image_address
        self.pill_diameter_mm = pill_diameter_mm
        self.cv_manager = None

    def run(self):
        self.cv_manager = CVManager(self.image_address, self.pill_diameter_mm)
        self.finished.emit()