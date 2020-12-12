from enum import Enum

# Each index has an index number
# and the infomation that comes together with that index
# such as when is the tutorial, lab, etc
class Index:
    def __init__(self, indexNo):
        self.indexNo = indexNo
        self.indexInfoList = []
        self.next = None    # used to create the indexGraph. value is None or another course's indexList

    def addIndexInfo(self, day, time, indexInfoType):
        self.indexInfoList.append(self.IndexInfo(day, time, indexInfoType))

    def getIndexNo(self):
        return self.indexNo

    def getIndexListInfo(self):
        return self.indexInfoList

    def getNext(self):
        return self.next

    class IndexInfo:
        def __init__(self, day, time, indexInfoType):
            self.day = day
            self.time = time
            self.indexInfoType = indexInfoType
            self.remarks = None

class typeIndexInfoEnum(Enum):
        LEC = 1
        TUT = 2
        LAB = 3