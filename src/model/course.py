from enum import Enum

# Each course have a course code,
# list of indexes attached to the course,
# and possibly a list of lecture timings
class Course:
    def __init__(self, courseCode, courseName):
        self.__courseCode = courseCode
        self.__courseName = courseName
        self.__indexList = []
        self.__courseType = None

    @property
    def courseCode(self):
        return self.__courseCode

    @courseCode.setter
    def courseCode(self, courseCode):
        self.__courseCode = courseCode

    @property
    def courseName(self):
        return self.__courseName

    @courseName.setter
    def courseName(self, courseName):
        self.__courseName = courseName
    
    @property
    def indexList(self):
        return self.__indexList

    def addIndex(self, index):
        self.__indexList.append(index)

    @property
    def courseType(self):
        return self.__courseType

    @courseType.setter
    def courseType(self, courseType):
        self.__courseType = courseType

class courseType(Enum):
    NON_ONLINE = 1
    ONLINE = 2