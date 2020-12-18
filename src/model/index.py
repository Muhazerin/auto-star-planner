from enum import Enum

# Each index has an index number
# and the infomation that comes together with that index
# such as when is the tutorial, lab, etc
class Index:
    def __init__(self, indexNo):
        self.__indexNo = indexNo
        self.__indexInfoList = []
        self.__next = None    # used to create the indexGraph. value is None or another course's indexList

    @property
    def indexNo(self):
        return self.__indexNo

    @indexNo.setter
    def indexNo(self, indexNo):
        self.__indexNo = indexNo

    @property
    def indexInfoList(self):
        return self.__indexInfoList

    def addIndexInfo(self, day, time, indexInfoType):
        self.__indexInfoList.append(self.IndexInfo(day, time, indexInfoType))

    @property
    def next(self):
        return self.__next
    
    @next.setter
    def next(self, next):
        self.__next = next

    class IndexInfo:
        def __init__(self, day, time, indexInfoType):
            self.__day = day
            self.__time = time
            self.__indexInfoType = indexInfoType
            self.__remarks = None

        @property
        def day(self):
            return self.__day

        @day.setter
        def day(self, day):
            self.__day = day

        @property
        def time(self):
            return self.__time

        @time.setter
        def time(self, time):
            self.__time = time

        @property
        def indexInfoType(self):
            return self.__indexInfoType

        @indexInfoType.setter
        def indexInfoType(self, indexInfoType):
            self.__indexInfoType = indexInfoType
        
        @property
        def remarks(self):
            return self.__remarks

        @remarks.setter
        def remarks(self, remarks):
            self.__remarks = remarks

class typeIndexInfoEnum(Enum):
        LEC = 1
        TUT = 2
        LAB = 3
        SEM = 4