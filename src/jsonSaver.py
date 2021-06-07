import json


class JsonSaver:
    def __init__(self, modules_list, indexes_list):
        self.__modules_list = modules_list
        self.__indexes_list = indexes_list

    # Save the data in list to json
    def save(self):
        # Save the modules_list to modules_data.json
        with open('modules_data.json', 'w') as json_data:
            json.dump(self.__modules_list, json_data)
        # Save the indexes_list to indexes_data.json
        with open('indexes_data.json', 'w') as json_data:
            json.dump(self.__indexes_list, json_data)
