from ui.dialog.filterSubjectsDialog.model import (subjectCopy, indexCopy)

class PotentialPlanCopy:
    def __init__(self, mainPotentialPlan):
        self.__potentialPlan = []
        for plan in mainPotentialPlan.potentialPlan:
            tempPlan = []
            for tempIndex in plan:
                tempPlan.append(indexCopy.IndexCopy(tempIndex))
            self.__potentialPlan.append(tempPlan.copy())
        self.__subjectList = []
        for subject in mainPotentialPlan.subjectList:
            self.__subjectList.append(subjectCopy.SubjectCopy(subject))

    @property
    def potentialPlan(self):
        return self.__potentialPlan

    @potentialPlan.setter
    def potentialPlan(self, plan):
        self.__potentialPlan = plan

    @property
    def subjectList(self):
        return self.__subjectList

    @subjectList.setter
    def subjectList(self, subjectList):
        self.__subjectList = subjectList

    def getSubjectListCopy(self):
        tempSubjectList = []
        for subject in self.__subjectList:
            tempSubjectList.append(subjectCopy.SubjectCopy(subject))
        return tempSubjectList