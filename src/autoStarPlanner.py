# TODO:
#  1) Create ModuleNode and IndexNode class
#  2) Create plan function (dfs based on IndexNodeClass)
#  3) MainPlan only receives a list of plannable indexes
#  4) Observer pattern to update the planner table

from PyQt5.QtWidgets import QMainWindow

from ui import mainwindow
from PyQt5.QtCore import pyqtSlot

from selectAcadSemDialog import SelectAcadSemDialog
import jsonLoader as Loader
from mainPlan import MainPlan
from plannerMgr import PlannerMgr


class AutoStarPlanner(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super(AutoStarPlanner, self).__init__()
        self.setupUi(self)
        self.select_acad_sem_dialog = SelectAcadSemDialog()
        self.__modules_list = []
        self.__indexes_list = []
        self.__planner_mgr = PlannerMgr(self.plannerTable)
        self.__main_plan = MainPlan()
        self.__main_plan.attach(self.__planner_mgr)

        self.select_acad_sem_dialog.signal_save_and_load.connect(self.load_from_disk)
        self.actionFrom_Website.triggered.connect(self.select_acad_sem_dialog.run)
        self.actionFrom_Disk.triggered.connect(self.load_from_disk)

    # Function to run when load from disk is click or successful outcome from load from website
    @pyqtSlot()
    def load_from_disk(self):
        # Load the modules_list and indexes_list from the loader
        self.__main_plan.modules_list, self.__main_plan.indexes_list = Loader.load()
