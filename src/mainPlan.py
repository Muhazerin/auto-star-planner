# The subject class which contains the selected modules and indexes
class MainPlan:
    def __init__(self):
        self.__modules_list = []
        self.__index_node_list = []
        self.__observers_list = []

    @property
    def modules_list(self):
        return self.__modules_list

    # Whenever both modules and indexes list changed, notify the observers to update
    @modules_list.setter
    def modules_list(self, new_modules_list):
        self.__modules_list = new_modules_list

    @property
    def index_node_list(self):
        return self.__index_node_list

    # Whenever both modules and indexes list changed, notify the observers to update
    @index_node_list.setter
    def index_node_list(self, new_index_node_list):
        self.__index_node_list = new_index_node_list
        self.notify()

    # Add the observer to observers_list
    def attach(self, observer):
        self.__observers_list.append(observer)

    # Notify the observers in observers_list to update whenever there's changes to modules and indexes list
    def notify(self):
        for observer in self.__observers_list:
            observer.update(self.__modules_list, self.__index_node_list)
