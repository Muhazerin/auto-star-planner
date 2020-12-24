class Friend:
    def __init__(self, name, tempList):
        self.__name = name
        self.__courseList = tempList

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def courseList(self):
        return self.__courseList

    @courseList.setter
    def courseList(self, tempList):
        self.__courseList = tempList