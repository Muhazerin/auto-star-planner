from PyQt5.QtWidgets import QLabel
import constants


def get_label(text):
    temp_label = QLabel(text)
    if 'LEC' in text:
        temp_label.setStyleSheet("background-color: lightskyblue; font-family: Arial; font-size: 22px")
    elif 'TUT' in text:
        temp_label.setStyleSheet("background-color: springgreen; font-family: Arial; font-size: 22px")
    elif 'LAB' in text:
        temp_label.setStyleSheet("background-color: salmon; font-family: Arial; font-size: 22px")
    else:
        temp_label.setStyleSheet("background-color: lightcoral; font-family: Arial; font-size: 22px")
    return temp_label


class PlannerMgr:
    def __init__(self, planner_table):
        self.__planner_table = planner_table

    # Attempt to plan the semester based on the selected modules and indexes
    def update(self, modules_list, index_node_list):
        self.__planner_table.clearContents()
        # Plan the lecture first as they are the more important one as they dont change based on index
        self.plan_lecture(modules_list, index_node_list)

    # Attempt to plan the lecture to planner table
    def plan_lecture(self, modules_list, index_node_list):
        # Loop through the length of modules_list
        for i in range(len(modules_list)):
            # Get the course code from modules list
            course_code = modules_list[i].split(':')[0]
            # Loop through the info that an "indexed" index_node
            for info in index_node_list[i].info:
                # Get the info start and end time
                start_time = info['TIME'].split('-')[0]
                end_time = info['TIME'].split('-')[1]
                # Translate start and end time to start and end time index
                start_time_index, end_time_index = constants.get_time_range(start_time, end_time)
                # Translate the day to day index
                day_index = constants.get_day_index(info['DAY'])
                self.update_table(day_index, start_time_index, end_time_index, info, course_code)

    # Update the planner table
    def update_table(self, day_index, start_time_range, end_time_range, info, course_code):
        for row in range(start_time_range, end_time_range):
            if info['TYPE'] == 'LAB':
                if info['REMARK'] == 'Teaching Wk1,3,5,7,9,11,13':
                    self.__planner_table.setCellWidget(row, day_index, get_label(f'{course_code}: Odd {info["TYPE"]}'))
                elif info['REMARK'] == 'Teaching Wk2,4,6,8,10,12':
                    self.__planner_table.setCellWidget(row, day_index, get_label(f'{course_code}: Even {info["TYPE"]}'))
                else:
                    self.__planner_table.setCellWidget(row, day_index, get_label(f'{course_code}: All {info["TYPE"]}'))
            else:
                self.__planner_table.setCellWidget(row, day_index, get_label(f'{course_code}: {info["TYPE"]}'))
