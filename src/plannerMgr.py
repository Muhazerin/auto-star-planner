from PyQt5.QtWidgets import QLabel


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
        # Dictionary to translate day to planner_table index
        self.__day_dict = {
            "MON": 0,
            "TUE": 1,
            "WED": 2,
            "THU": 3,
            "FRI": 4,
            "SAT": 5
        }
        # Dictionary to translate time to planner_table index
        self.__time_dict = {
            "0800": 0,
            "0830": 1,
            "0900": 2,
            "0930": 3,
            "1000": 4,
            "1030": 5,
            "1100": 6,
            "1130": 7,
            "1200": 8,
            "1230": 9,
            "1300": 10,
            "1330": 11,
            "1400": 12,
            "1430": 13,
            "1500": 14,
            "1530": 15,
            "1600": 16,
            "1630": 17,
            "1700": 18,
            "1730": 19,
            "1800": 20,
            "1830": 21,
            "1900": 22,
            "1930": 23,
            "2000": 24,
            "2030": 25,
            "2100": 26,
            "2130": 27,
            "2200": 28,
            "2230": 29,
            "2300": 30
        }

    # Attempt to plan the semester based on the selected modules and indexes
    def update(self, modules_list, indexes_list):
        self.__planner_table.clearContents()
        # Plan the lecture first as they are the more important one as they dont change based on index
        self.plan_lecture(modules_list, indexes_list)

    # Attempt to plan the lecture to planner table
    def plan_lecture(self, modules_list, indexes_list):
        # Loop through all the modules
        for i in range(len(modules_list)):
            # Get the module's first index info
            first_module_index_info = indexes_list[i][0]['info']
            # Get the course code from modules list
            course_code = modules_list[i].split(':')[0]
            # Loop through the info list
            for info in first_module_index_info:
                # Check if info is 'LEC/STUDIO'
                if info['TYPE'] == 'LEC/STUDIO':
                    # Get the lecture start and end time
                    start_time = info['TIME'].split('-')[0]
                    end_time = info['TIME'].split('-')[1]
                    # Translate start and end time to start and end time index
                    start_time_index, end_time_index = self.get_time_range(start_time, end_time)
                    # Translate the day to day index
                    day_index = self.get_day_index(info['DAY'])
                    self.update_table(day_index, start_time_index, end_time_index, info, course_code)
                    # print(day_index, start_time_index, end_time_index)

    # Translate the start and end time to range
    def get_time_range(self, start_time, end_time):
        # Naive way to correct for errors as Acad Yr 2021 Sem 1 end time is '20', like 1320.
        if start_time[2] != '0':
            # Change string to list
            start_time_list = list(start_time)
            # Do the update
            start_time_list[2] = '3'
            # Change list to string
            start_time = ''.join(start_time_list)
        if end_time[2] != '0':
            # Change string to list
            end_time_list = list(end_time)
            # Do the update
            end_time_list[2] = '3'
            # Change list to string
            end_time = ''.join(end_time_list)
        return self.__time_dict[start_time], self.__time_dict[end_time]

    # Translate the day to day index
    def get_day_index(self, day):
        return self.__day_dict[day]

    # Attempts to update the planner table
    def update_table(self, day_index, start_time_range, end_time_range, info, course_code):
        for row in range(start_time_range, end_time_range):
            if self.__planner_table.cellWidget(row, day_index):
                text = self.__planner_table.cellWidget(row, day_index).text()
                if 'LAB' in text:
                    print(text)
                else:
                    print('got clash')
            else:
                self.__planner_table.setCellWidget(row, day_index, get_label(f'{course_code}: {info["TYPE"]}'))
