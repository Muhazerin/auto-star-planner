class Friend:
    def __init__(self, name):
        self.__name = name
        self.__courseList = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name