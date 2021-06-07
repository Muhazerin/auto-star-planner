import json


# Load the data from json files
def load():
    # Load indexes_list from indexes_data.json
    with open('indexes_data.json', 'r') as json_file:
        indexes_list = json.load(json_file)
    # Load modules_list from modules_data.json
    with open('modules_data.json', 'r') as json_file:
        modules_list = json.load(json_file)
    # Return both lists
    return modules_list, indexes_list
