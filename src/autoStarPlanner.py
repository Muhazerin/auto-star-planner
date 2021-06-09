# TODO:
#  1) Create plan function (dfs based on IndexNodeClass)
#  2) MainPlan only receives a list of plannable indexes
#  3) Observer pattern to update the planner table

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot
import copy

from ui import mainwindow
from selectAcadSemDialog import SelectAcadSemDialog
import jsonLoader as Loader
from mainPlan import MainPlan
from plannerMgr import PlannerMgr
import indexNode
import constants


class AutoStarPlanner(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super(AutoStarPlanner, self).__init__()
        self.setupUi(self)
        self.select_acad_sem_dialog = SelectAcadSemDialog()
        self.__possible_plans = []
        self.__planner_mgr = PlannerMgr(self.plannerTable)
        self.__main_plan = MainPlan()
        self.__main_plan.attach(self.__planner_mgr)

        # Used to temporarily mark day_time for normal planning
        self.__day_time = []
        # Used to temporarily mark day_time for lab planning
        self.__day_time_even_odd = []
        for i in range(0, 31):
            self.__day_time.append([0] * 6)
            # NIL, A = All week, E = Even week, O = Odd Week, EO = Even and Odd Week
            self.__day_time_even_odd.append(["NIL"] * 6)

        self.select_acad_sem_dialog.signal_save_and_load.connect(self.load_from_disk)
        self.actionFrom_Website.triggered.connect(self.select_acad_sem_dialog.run)
        self.actionFrom_Disk.triggered.connect(self.load_from_disk)

    # Function to run when load from disk is click or successful outcome from load from website
    @pyqtSlot()
    def load_from_disk(self):
        # Load the modules_list and indexes_list from the loader
        modules_list, indexes_list = Loader.load()
        # Transform the indexes_list into list_of_index_node_list
        list_of_index_node_list = indexNode.create_list_of_index_node_list(indexes_list)
        # Try to plan using this indexes configuration
        self.plan(list_of_index_node_list)

    # Attempt to plan using the current indexes configuration
    def plan(self, list_of_index_node_list):
        # Clear all the necessary lists
        self.__possible_plans = []
        self.__day_time = []
        self.__day_time_even_odd = []
        for i in range(0, 31):
            self.__day_time.append([0] * 6)
            self.__day_time_even_odd.append(["NIL"] * 6)

        # Perform a dfs using the first index_node_list in order to plan
        self.dfs_main(list_of_index_node_list[0])

    # The entry point for the dfs
    def dfs_main(self, index_node_list):
        # Creates a temporary plan
        temp_plan = []
        # Loop through index_node_list
        for index_node in index_node_list:
            # Temporary mark the day time using the info stored in index_node
            self.temp_mark_day_time(index_node)
            # Append the current index to temp_plan
            temp_plan.append(index_node)
            # Enter a dfs loop
            self.dfs(index_node, temp_plan)
            # Remove index_node from temp_plan
            temp_plan.remove(index_node)
            # Unmark the day time using the info stored in index_node
        print('Hooray')

    # Function to run to temporary mark day_time and day_time_even_odd for non-lab lessons
    def temp_mark_day_time(self, index_node):
        # Loop through the info in index_node
        for info in index_node.info:
            # Get the non-lab start and end time
            start_time = info['TIME'].split('-')[0]
            end_time = info['TIME'].split('-')[1]
            # Translate start and end time to start and end time index
            start_time_index, end_time_index = constants.get_time_range(start_time, end_time)
            # Translate the day to day index
            day_index = constants.get_day_index(info['DAY'])

            # There is a separate function for marking day time for LAB
            if info['TYPE'] == 'LAB':
                self.temp_mark_day_time_for_lab(start_time_index, end_time_index, day_index, info)
            else:
                # For non-lab lesson, i assume lesson occurs all weeks
                # Therefore, loop through day_time and day_time_even_odd and mark them
                for row in range(start_time_index, end_time_index):
                    self.__day_time[row][day_index] = 1
                    self.__day_time_even_odd[row][day_index] = 'A'

    # Function to run to temporary mark day_time and day_time_even_odd for lab lessons
    def temp_mark_day_time_for_lab(self, start_time_index, end_time_index, day_index, info):
        for row in range(start_time_index, end_time_index):
            # Check if current day_time is unmark
            if self.__day_time[row][day_index] == 0:
                # Mark it
                self.__day_time[row][day_index] = 1
                # Check whether lab is Odd, Even, or All Week and mark accordingly
                if info['REMARK'] == 'Teaching Wk1,3,5,7,9,11,13':
                    self.__day_time_even_odd[row][day_index] = 'O'
                elif info['REMARK'] == 'Teaching Wk2,4,6,8,10,12':
                    self.__day_time_even_odd[row][day_index] = 'E'
                else:
                    self.__day_time_even_odd[row][day_index] = 'A'
            else:
                # If current day time is mark, check if day_time_even_odd does not clash with current index
                if (info['REMARK'] == 'Teaching Wk1,3,5,7,9,11,13' and self.__day_time_even_odd == 'E') or \
                        (info['REMARK'] == 'Teaching Wk2,4,6,8,10,12' and self.__day_time_even_odd == 'O'):
                    # Mark it as EO so as not to be confused with A
                    self.__day_time_even_odd = 'EO'

    # The dfs loop
    def dfs(self, index_node, temp_plan):
        pass
