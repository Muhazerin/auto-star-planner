import requests

import bs4.element
from bs4 import BeautifulSoup


class DataSource:
    def __init__(self):
        self.__acad_sem_dict = None
        self.__chosen_acad_sem = None
        self.__course_year_value = None
        self.__course_year_key = None

    @property
    def acad_sem_dict(self):
        return self.__acad_sem_dict

    @property
    def chosen_acad_sem(self):
        return self.__chosen_acad_sem

    @chosen_acad_sem.setter
    def chosen_acad_sem(self, x):
        self.__chosen_acad_sem = x

    @property
    def course_year_value(self):
        return self.__course_year_value

    @property
    def course_year_key(self):
        return self.__course_year_key

    # Visit NTU Class Schedule website and try to save the acadSem to self.__acad_sem
    def load_acad_sem(self):
        try:
            # Try to requests the content of this website
            response = requests.get('https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main')
            if response.status_code != 200:
                self.__acad_sem_dict = f'DataSource load_acad_sem Error! Status Code: {response.status_code}'
            else:
                # Parse the request to soup and get the first select tag's children
                acad_sem_list = BeautifulSoup(response.text, 'html.parser').find('select').contents
                # Remove the /n in the list
                acad_sem_list = [elem for elem in acad_sem_list if elem != '\n']
                # Get the value(key) and string(value) of every element in the list and store it as a dictionary
                acad_sem_dict = {elem['value']: elem.string for elem in acad_sem_list}
                self.__acad_sem_dict = acad_sem_dict
        except Exception as err:
            self.__acad_sem_dict = f'DataSource load_acad_sem Exception Error! Error msg: {err}'

    # Visit NTU Class Schedule website and try to save the courseYear to self.__course_year
    def load_course_year(self, acad_sem):
        try:
            # The data to be POSTed
            data = {
                'acadsem': acad_sem,
                'r_subj_code': 'Enter Keywords or Course Code',
                'r_search_type': 'F',
                'boption': 'x',
                'staff_access': 'false'
            }
            # Create a POST requests with the data
            response = requests.post('https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display', data=data)
            if response.status_code != 200:
                self.__course_year_value = f'DataSource load_course_year Error! Status Code: {response.status_code}'
                self.__course_year_key = f'DataSource load_course_year Error! Status Code: {response.status_code}'
            else:
                # Parse the request to soup and get the select tag's siblings(Tags on the same level)
                select_siblings = BeautifulSoup(response.text, 'html.parser').find('select').next_siblings
                # Get the other select tag from the siblings and store its content to a list
                for sibling in select_siblings:
                    if type(sibling) is bs4.element.Tag and sibling.name == 'select':
                        course_year_list = sibling.contents
                # Remove the /n in the list
                course_year_list = [elem for elem in course_year_list if elem != '\n']
                # Separate the list into 2 lists (key, value)
                self.__course_year_value = [elem.string for elem in course_year_list]
                self.__course_year_key = [elem['value'] for elem in course_year_list]
        except Exception as err:
            self.__course_year_value = f'DataSource load_course_year Exception Error! Error msg: {err}'
            self.__course_year_key = f'DataSource load_course_year Exception Error! Error msg: {err}'


source = DataSource()
