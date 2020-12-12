from enum import Enum

# Each course have a course code,
# list of indexes attached to the course,
# and possibly a list of lecture timings
class Course:
    def __init__(self, courseCode):
        self.courseCode = courseCode
        self.indexList = []
        self.courseType = None

    def setCourseType(self, courseType):
        self.courseType = courseType

    def addIndex(self, index):
        self.indexList.append(index)
    
    def getCourseCode(self):
        return self.courseCode

    def getIndexList(self):
        return self.indexList

    def getCourseType(self):
        return self.courseType

class courseType(Enum):
    LECTUTLAB = 1
    LECTUT = 2
    TUT = 3
    ONLINE = 4