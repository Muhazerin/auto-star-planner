import requests
import re
from bs4 import BeautifulSoup


class DataSource:
    def __init__(self):
        self.__acad_sem_dict = None         # Dict
        self.__chosen_acad_sem = None       # String
        self.__course_year_value = None     # List
        self.__course_year_key = None       # List
        self.__modules = None               # List
        self.__indexes = None               # List of dict --> [{}, {}, {}]

    @property
    def acad_sem_dict(self):
        return self.__acad_sem_dict

    @property
    def chosen_acad_sem(self):
        return self.__chosen_acad_sem

    @chosen_acad_sem.setter
    def chosen_acad_sem(self, new_chosen_acad_sem):
        self.__chosen_acad_sem = new_chosen_acad_sem

    @property
    def course_year_value(self):
        return self.__course_year_value

    @property
    def course_year_key(self):
        return self.__course_year_key

    @property
    def modules(self):
        return self.__modules

    @property
    def indexes(self):
        return self.__indexes

    # Visit NTU Class Schedule website and try to save the acadSem to self.__acad_sem
    def load_acad_sem(self):
        try:
            # Create a GET request to this website
            response = requests.get('https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main')
            if response.status_code != 200:
                self.__acad_sem_dict = f'DataSource load_acad_sem Error!\nStatus Code: {response.status_code}'
            else:
                # Parse the request to soup and get the first select tag's children
                acad_sem_list = BeautifulSoup(response.text, 'html.parser').find('select').contents
                # Remove the /n in the list
                acad_sem_list = [elem for elem in acad_sem_list if elem != '\n']
                # Get the value(key) and string(value) of every element in the list and store it as a dictionary
                acad_sem_dict = {elem['value']: elem.string for elem in acad_sem_list}
                self.__acad_sem_dict = acad_sem_dict
        except Exception as err:
            self.__acad_sem_dict = f'DataSource load_acad_sem Exception Error!\nError msg: {err}'

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
            # Create a POST requests to this website with the data
            response = requests.post('https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display', data=data)
            if response.status_code != 200:
                self.__course_year_value = f'DataSource load_course_year Error!\nStatus Code: {response.status_code}'
                self.__course_year_key = f'DataSource load_course_year Error!\nStatus Code: {response.status_code}'
            else:
                # Parse the request to soup and find all the select tags
                selects = BeautifulSoup(response.text, 'html.parser').find_all('select')
                # The info that I'm looking for is the content of the second select tag
                course_year_list = selects[1].contents
                # Remove the /n in the list
                course_year_list = [elem for elem in course_year_list if elem != '\n']
                # Separate the list into 2 lists (key, value)
                self.__course_year_value = [elem.string for elem in course_year_list]
                self.__course_year_key = [elem['value'] for elem in course_year_list]
        except Exception as err:
            self.__course_year_value = f'DataSource load_course_year Exception Error!\nError msg: {err}'
            self.__course_year_key = f'DataSource load_course_year Exception Error!\nError msg: {err}'

    # Visit NTU Class Schedule website and try to load the modules using the course_year_key
    def load_modules(self, course_year_key):
        try:
            # The data to be POSTed
            data = {
                'acadsem': list(self.__acad_sem_dict.keys())[
                    list(self.__acad_sem_dict.values()).index(self.__chosen_acad_sem)],
                'r_course_yr': course_year_key,
                'r_subj_code': 'Enter Keywords or Course Code',
                'r_search_type': 'F',
                'boption': 'CLoad',
                'staff_access': 'false'
            }
            # Create a POST request to this website with this data
            response = requests.post('https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1', data=data)
            if response.status_code != 200:
                self.__modules = f'DataSource load_modules Error!\nStatus Code: {response.status_code}'
            else:
                # Initialize self.__modules to a list
                self.__modules = []
                # Parse the request to soup and find all the table tags
                tables = BeautifulSoup(response.text, 'html.parser').find_all('table')
                # Compile the regex to be used later
                regex = re.compile('[^a-zA-Z0-9\s]')
                # The table consists of 2 sections (course info, course timetable info)
                # Course info section
                for i in range(0, len(tables), 2):
                    # The data is stored in font tag
                    fonts = tables[i].find_all('font')
                    # Sometimes the course name has special chars(*,~), I want those removed
                    course_name = regex.split(fonts[1].string)[0]
                    # Append the information to self.__modules
                    self.__modules.append(f'{fonts[0].string}: {course_name}')
                # Course timetable info section
                for i in range(1, len(tables) + 1, 2):
                    # Split the info into indexes
                    self.retrieve_indexes(tables[i])

        except Exception as err:
            self.__modules = f'DataSource load_modules Exception Error\nError msg: {err}'

    # Split the info into indexes
    def retrieve_indexes(self, table):
        self.__indexes = []
        # Get all the rows in the table
        trs = table.find_all('tr')
        for i in range(1, len(trs)):
            self.__indexes.append({})
            # Get all the columns in a row. There are exactly 7 columns
            tds = trs[i].find_all('td')
            # Parse the respective columns
            self.parse_index(tds[0])
            self.parse_type(tds[1])
            self.parse_group(tds[2])
            self.parse_day(tds[3])
            self.parse_time(tds[4])
            self.parse_venue(tds[5])
            self.parse_remark(tds[6])

    def parse_index(self, td):
        pass

    def parse_type(self, td):
        pass

    def parse_group(self, td):
        pass

    def parse_day(self, td):
        pass

    def parse_time(self, td):
        pass

    def parse_venue(self, td):
        pass

    def parse_remark(self, td):
        pass


source = DataSource()
