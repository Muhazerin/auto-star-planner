from ui.dialog.filterSubjectsDialog import indexCopy

class SubjectCopy:
    def __init__(self, tempSubject):
        self.__courseCode = tempSubject.courseCode
        self.__courseName = tempSubject.courseName
        self.__indexList = []
        for tempIndex in tempSubject.indexList:
            self.__indexList.append(indexCopy.IndexCopy(tempIndex))
        self.__courseType = tempSubject.courseType

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