class IndexCopy:
    def __init__(self, tempIndex):
        self.__indexNo = tempIndex.indexNo
        self.__indexInfoList = []
        for tempIndexInfo in tempIndex.indexInfoList:
            self.__indexInfoList.append(self.IndexInfoCopy(tempIndexInfo))
        self.__next = next

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

    class IndexInfoCopy:
        def __init__(self, tempIndexInfo):
            self.__day = tempIndexInfo.day
            self.__time = tempIndexInfo.time
            self.__indexInfoType = tempIndexInfo.indexInfoType
            self.__remarks = tempIndexInfo.remarks

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