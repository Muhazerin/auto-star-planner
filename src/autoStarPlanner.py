from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QMessageBox

import constants
import indexNode
import jsonLoader as Loader
from mainPlan import MainPlan
from plannerMgr import PlannerMgr
from selectAcadSemDialog import SelectAcadSemDialog
from ui import mainwindow


class AutoStarPlanner(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super(AutoStarPlanner, self).__init__()
        self.setupUi(self)
        self.select_acad_sem_dialog = SelectAcadSemDialog()
        self.__possible_plans = []
        self.__modules_list = []
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
        self.overviewLbl.hide()

        self.select_acad_sem_dialog.signal_save_and_load.connect(self.load_from_disk)
        self.actionFrom_Website.triggered.connect(self.select_acad_sem_dialog.run)
        self.actionFrom_Disk.triggered.connect(self.load_from_disk)
        self.planSpinBox.valueChanged.connect(self.on_planSpinBox_value_changed)

    # Function to run when load from disk is click or successful outcome from load from website
    @pyqtSlot()
    def load_from_disk(self):
        # Load the modules_list and indexes_list from the loader
        self.__modules_list, indexes_list = Loader.load()
        # Set the main plan module list
        self.__main_plan.modules_list = self.__modules_list
        # Transform the indexes_list into list_of_index_node_list
        list_of_index_node_list = indexNode.create_list_of_index_node_list(indexes_list)
        # Try to plan using this indexes configuration
        self.plan(list_of_index_node_list)
        # Check the plan after trying to plan
        self.check_plan()

    @pyqtSlot()
    def on_planSpinBox_value_changed(self):
        index_text = ''
        for i in range(len(self.__modules_list)):
            # Get the course code from modules list
            course_code = self.__modules_list[i].split(':')[0]
            index_text += f'{course_code}: {self.__possible_plans[self.planSpinBox.value() - 1][i].index_no}          '
            self.overviewLbl.setText(index_text)
            self.__main_plan.index_node_list = self.__possible_plans[self.planSpinBox.value() - 1]

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
            self.unmark_day_time(index_node)

    # The dfs loop
    def dfs(self, index_node, temp_plan):
        # Check if temp_plan contains as many indexes as number of modules selected
        if len(temp_plan) == len(self.__modules_list):
            self.__possible_plans.append(temp_plan.copy())
        elif index_node.index_node_list:
            # If not, loop through the next index node in the index_node_list, and dfs if no clash
            for next_index_node in index_node.index_node_list:
                # Need to check if there is clash for every info in the index
                clash = False
                for next_index_node_info in next_index_node.info:
                    # Get the info start and end time
                    start_time = next_index_node_info['TIME'].split('-')[0]
                    end_time = next_index_node_info['TIME'].split('-')[1]
                    # Translate start and end time to start and end time index
                    start_time_index, end_time_index = constants.get_time_range(start_time, end_time)
                    # Translate the day to day index
                    day_index = constants.get_day_index(next_index_node_info['DAY'])

                    # Separate functions to check for clash for Lab and non-lab lesson
                    if next_index_node_info['TYPE'] == 'LAB':
                        clash = self.check_clash_for_lab(start_time_index, end_time_index, day_index,
                                                         next_index_node_info)
                    else:
                        clash = self.check_clash(start_time_index, end_time_index, day_index)

                print(next_index_node.index_no)
                print(clash)

                # If there is no clash, add to temp_plan and dfs
                if not clash:
                    # Temporary mark the day time using the info stored in index_node
                    self.temp_mark_day_time(next_index_node)
                    # Append the current index to temp_plan
                    temp_plan.append(next_index_node)
                    # Enter a dfs loop
                    self.dfs(next_index_node, temp_plan)
                    # Remove index_node from temp_plan
                    temp_plan.remove(next_index_node)
                    # Unmark the day time using the info stored in index_node
                    self.unmark_day_time(next_index_node)

                # If not, ignore and continue to next index node

    # Function to run to temporary mark day_time and day_time_even_odd for non-lab lessons
    def temp_mark_day_time(self, index_node):
        # Loop through the info in index_node
        for info in index_node.info:
            # Get the info start and end time
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
                if (info['REMARK'] == 'Teaching Wk1,3,5,7,9,11,13' and self.__day_time_even_odd[row][day_index] == 'E') or \
                        (info['REMARK'] == 'Teaching Wk2,4,6,8,10,12' and self.__day_time_even_odd[row][day_index] == 'O'):
                    # Mark it as EO so as not to be confused with A
                    self.__day_time_even_odd[row][day_index] = 'EO'

    # Function to run to unmark day_time and day_time_even_odd
    def unmark_day_time(self, index_node):
        # Loop through the info in index_node
        for info in index_node.info:
            # Get the info start and end time
            start_time = info['TIME'].split('-')[0]
            end_time = info['TIME'].split('-')[1]
            # Translate start and end time to start and end time index
            start_time_index, end_time_index = constants.get_time_range(start_time, end_time)
            # Translate the day to day index
            day_index = constants.get_day_index(info['DAY'])

            # Separate function to unmark day_time for lab lessons
            if info['TYPE'] == 'LAB':
                self.unmark_day_time_even_odd(start_time_index, end_time_index, day_index, info)
            else:
                # For non-lab lesson, i assume lesson occurs all weeks
                # Therefore, loop through day_time and day_time_even_odd and un mark them
                for row in range(start_time_index, end_time_index):
                    self.__day_time[row][day_index] = 0
                    self.__day_time_even_odd[row][day_index] = 'NIL'

    # Function to run to unmark day_time_even_odd of lab
    def unmark_day_time_even_odd(self, start_time_index, end_time_index, day_index, info):
        # Loop through the time range
        for row in range(start_time_index, end_time_index):
            if info['REMARK'] == 'Teaching Wk1,3,5,7,9,11,13' and self.__day_time_even_odd[row][day_index] == 'EO':
                # Unmark odd-week lab, leaving even-week lab
                self.__day_time_even_odd[row][day_index] = 'E'
            elif info['REMARK'] == 'Teaching Wk2,4,6,8,10,12' and self.__day_time_even_odd[row][day_index] == 'EO':
                # Unmark even-week lab, leaving odd-week lab
                self.__day_time_even_odd[row][day_index] = 'O'
            else:
                # Unamrk the rest that doesn't fall into either two category
                self.__day_time_even_odd[row][day_index] = 'NIL'
                self.__day_time[row][day_index] = 0

    # Function to run to check for clash for this lab
    def check_clash_for_lab(self, start_time_index, end_time_index, day_index, info):
        # Loop through the time range
        for row in range(start_time_index, end_time_index):
            # Some lab have no remarks so I assume it happens every week
            if not info['REMARK'] and self.__day_time_even_odd[row][day_index] != 'NIL':
                return True
            elif info['REMARK'] == 'Teaching Wk1,3,5,7,9,11,13' and (self.__day_time_even_odd[row][day_index] == 'A' or
                                                                     self.__day_time_even_odd[row][day_index] == 'O' or
                                                                     self.__day_time_even_odd[row][day_index] == 'EO'):
                # Return true if odd week lab and time slot is occupied
                return True
            elif info['REMARK'] == 'Teaching Wk2,4,6,8,10,12' and (self.__day_time_even_odd[row][day_index] == 'A' or
                                                                   self.__day_time_even_odd[row][day_index] == 'E' or
                                                                   self.__day_time_even_odd[row][day_index] == 'EO'):
                # Return true if even week lab and time slot is occupied
                return True
        return False

    def check_clash(self, start_time_index, end_time_index, day_index):
        # Loop through the time range
        for row in range(start_time_index, end_time_index):
            # Check if time slot is occupied
            if self.__day_time[row][day_index] == 1:
                return True
            return False

    def check_plan(self):
        # Check the possible plan
        if len(self.__possible_plans) == 0:
            # Reset the UI and send error msg to user
            self.totalPlanLbl.setText(0)
            self.totalPlanLbl.setText(0)
            self.planSpinBox.setValue(0)
            self.planSpinBox.setEnabled(False)
            self.overviewLbl.hide()
            QMessageBox.critical(self, self.windowTitle(),
                                 f'Unable to plan your semester with the current configuration')
        else:
            # Set some UI and update the planner table via observer pattern
            self.overviewLbl.show()
            self.totalPlanLbl.setText(str(len(self.__possible_plans)))
            self.planSpinBox.setEnabled(True)
            self.planSpinBox.setMinimum(1)
            self.planSpinBox.setMaximum(len(self.__possible_plans))
