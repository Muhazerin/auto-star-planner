class PotentialPlan:
    def __init__(self):
        self.__potentialPlan = []   # to hold the planned indexes
        self.__subjectList = []     # to hold the list of subjects
        self.__whoMadeTheChange = ''
        self.__planChanged = False
        self.__subjectListChanged = False
        self.__observers = []

    @property
    def potentialPlan(self):
        return self.__potentialPlan
    
    @potentialPlan.setter
    def potentialPlan(self, plan):
        self.__potentialPlan = plan
        self.__planChanged = True
        if self.__subjectListChanged and self.__planChanged:
            self.__subjectListChanged = False
            self.__planChanged = False
            for observer in self.__observers:
                observer.updatePlan()

    @property
    def subjectList(self):
        return self.__subjectList

    @subjectList.setter
    def subjectList(self, subjectList):
        self.__subjectList = subjectList
        self.__subjectListChanged = True
        if self.__subjectListChanged and self.__planChanged:
            self.__subjectListChanged = False
            self.__planChanged = False
            for observer in self.__observers:
                observer.updatePlan()

    @property
    def whoMadeTheChange(self):
        return self.__whoMadeTheChange

    @whoMadeTheChange.setter
    def whoMadeTheChange(self, name):
        self.__whoMadeTheChange = name

    def addObserver(self, observer):
        self.__observers.append(observer)

    def copyPotentialPlan(self):
        return self.__potentialPlan.copy()

    def copySubjectList(self):
        return self.__subjectList.copy()
