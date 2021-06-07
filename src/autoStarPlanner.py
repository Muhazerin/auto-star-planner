from PyQt5.QtWidgets import QMainWindow

from ui import mainwindow
from PyQt5.QtCore import pyqtSlot

from selectAcadSemDialog import SelectAcadSemDialog
import jsonLoader as Loader


class AutoStarPlanner(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super(AutoStarPlanner, self).__init__()
        self.setupUi(self)
        self.select_acad_sem_dialog = SelectAcadSemDialog()
        self.__modules_list = []
        self.__indexes_list = []

        self.select_acad_sem_dialog.signal_save_and_load.connect(self.load_from_disk)
        self.actionFrom_Website.triggered.connect(self.select_acad_sem_dialog.run)
        self.actionFrom_Disk.triggered.connect(self.load_from_disk)

    # Function to run when load from disk is click or successful outcome from load from website
    @pyqtSlot()
    def load_from_disk(self):
        # Load the modules_list and indexes_list from the loader
        self.__modules_list, self.__indexes_list = Loader.load()
