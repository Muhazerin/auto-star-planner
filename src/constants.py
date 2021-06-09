# Dictionary to translate day to planner_table index
day_dict = {
    "MON": 0,
    "TUE": 1,
    "WED": 2,
    "THU": 3,
    "FRI": 4,
    "SAT": 5
}
# Dictionary to translate time to planner_table index
time_dict = {
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


def get_time_range(start_time, end_time):
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
    return time_dict[start_time], time_dict[end_time]


def get_day_index(day):
    return day_dict[day]
