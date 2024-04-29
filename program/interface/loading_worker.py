import time

from PyQt5.QtCore import QObject, pyqtSignal


class LoadingWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, label):
        super().__init__()
        self.loading_label = label
        self.working = True

    def run(self):
        st = time.time()
        while self.working:
            ct = int(time.time() - st)
            if ct % 4 == 0:
                self.loading_label.setText("Loading")
            elif ct % 4 == 1:
                self.loading_label.setText("Loading.")
            elif ct % 4 == 2:
                self.loading_label.setText("Loading..")
            elif ct % 4 == 3:
                self.loading_label.setText("Loading...")
        self.finished.emit()