import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from model import (course, index)

acadSem = None

# Load the list of courses and year from the website
# Returns the dictionary of results
# Returns a string if there's any error
def loadCourseYears():
    try:
        # do a get request to this url
        response = requests.get('https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main')
        if response.status_code != 200:
            return f'Error! Status Code: {response.status_code}'
        else:
            # if get is successful
            # add only the course and year into resultDict
            resultDict = {}
            separator = 1
            startAdding = False
            global acadSem
            acadSem = BeautifulSoup(response.text, 'html.parser').option['value']
            for option in BeautifulSoup(response.text, 'html.parser')("option"):
                if not startAdding:
                    # the first few parts in option are the acadsem
                    # the website naturally picks the current acadsem
                    # so there's no need to add that to the dict
                    if option.text == '---Select an Option---':
                        startAdding = True
                        resultDict[option.text] = option.text
                else:
                    # there are certain cases that we have to consider here
                    # the values are either empty or valid values
                    # 1) If the values are not empty, add it to the dict
                    # 2) If values are empty, use the separator int to add the separator
                    if option["value"]:
                        resultDict[option['value']] = option.text
                    else:
                        resultDict[f"separator{separator}"] = option.text
                        separator += 1
            if resultDict:
                return resultDict
            else:
                return "Empty dictionary"
    except HTTPError as http_err:
        return f'HTTP error occurred: {http_err}'
    except Exception as err:
        return f'Other error occurred: {err}'

# Checks the courseYear from loadCourse()
# Return a list if valid value; a list of course with its index filled
# Return a string if invalid value
def loadSubjects(courseYear):
    try:
        global acadSem
        # do a post request to this url with these data
        response = requests.post('https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1', data={
            'acadsem':acadSem,
            'r_course_yr':courseYear,
            'r_subj_code':'Enter Keywords or Course Code',
            'r_search_type':'F',
            'boption':'CLoad',
            'acadsem':acadSem,
            'staff_access':'false'
            })
        if response.status_code != 200:
            return f'Error, Status Code: {response.status_code}'
        else:
            # If successful, get the populate the courses and index list and 
            courseList = []
            i = 0
            for table in BeautifulSoup(response.text, 'html.parser')('table'):
                # the table is split into 2 parts, thus the i % 2 == 0 check
                # the top contains course info
                # the bottom contains the index info
                if i % 2 == 0:  # top part (course info)
                    if "".join(table('font')[1].findAll(text=True))[-1] == "*": # some course got '*' at the end of its name. Remove it
                        courseList.append(course.Course("".join(table('font')[0].findAll(text=True)), "".join(table('font')[1].findAll(text=True))[:-1]))
                    else:
                        courseList.append(course.Course("".join(table('font')[0].findAll(text=True)), "".join(table('font')[1].findAll(text=True))))
                else:   # bottom part (index info)
                    # add the indexes to the last course in the courseList
                    retrieveIndexes(table, courseList[-1])
                i += 1
            return courseList
    except HTTPError as http_err:
        return f'HTTP error occurred: {http_err}'
    except Exception as err:
        return f'Other error occurred: {err}'

# the index info could be
# 1: Online Course (from Remarks)
# 2: Lec (from type)
# 3: Tut (from type)
# 4: Even/Odd/All Week Lab (from type and Remarks)
# Doesn't return anything
def retrieveIndexes(table, tempCourse):
    col = 0 # the index info table only has 7 columns
    first = True    # check if first index as indexInfo are only stored at the next index
    for item in table("td"):
        if col % 7 == 0:    # Index Number resides here
            if "".join(item.findAll(text=True)):    # if index number is not empty
                if first:   # first index
                    first = False
                    tempIndex = index.Index("".join(item.findAll(text=True)))
                else:       # not the first index
                    tempCourse.addIndex(tempIndex)
                    tempIndex = index.Index("".join(item.findAll(text=True)))
        elif col % 7 == 1:  # Type column ((blank(for online courses), LEC/STUDIO, TUT, LAB, SEM))
            if "".join(item.findAll(text=True)) == 'LEC/STUDIO':
                indexInfoType = index.typeIndexInfoEnum.LEC
            elif "".join(item.findAll(text=True)) == 'TUT':
                indexInfoType = index.typeIndexInfoEnum.TUT
            elif "".join(item.findAll(text=True)) == 'LAB':
                indexInfoType = index.typeIndexInfoEnum.LAB
            elif "".join(item.findAll(text=True)) == 'SEM':
                indexInfoType = index.typeIndexInfoEnum.SEM
            else:
                indexInfoType = None
        elif col % 7 == 3:  # Day: (MON, TUE, WED, THU, FRI)
            day = "".join(item.findAll(text=True))
        elif col % 7 == 4:  # Time
            time = "".join(item.findAll(text=True))
        elif col % 7 == 6: # Remarks: (blank, Teaching Wk(tut and lab got its own teaching week), Online Course)
            if 'Online Course' in "".join(item.findAll(text=True)):
                tempCourse.courseType = course.courseType.ONLINE
            else:
                tempCourse.courseType = course.courseType.NON_ONLINE
                if "".join(item.findAll(text=True)) == "Teaching Wk2,4,6,8,10,12":
                    tempIndex.addIndexInfo(day, time, indexInfoType)
                    tempIndex.indexInfoList[-1].remarks = 'Even'
                elif "".join(item.findAll(text=True)) == 'Teaching Wk1,3,5,7,9,11,13':
                    tempIndex.addIndexInfo(day, time, indexInfoType)
                    tempIndex.indexInfoList[-1].remarks = 'Odd'
                else:   # Remarks is empty
                    tempIndex.addIndexInfo(day, time, indexInfoType)
                    if (indexInfoType == index.typeIndexInfoEnum.LAB):  # There exists a lab that occurs all week
                        tempIndex.indexInfoList[-1].remarks = 'All Week'
        col += 1
    tempCourse.addIndex(tempIndex)  # this is to add the last index as the algo above only add the index at the next index