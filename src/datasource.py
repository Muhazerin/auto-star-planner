import requests
from bs4 import BeautifulSoup


# Visit NTU Class Schedule website and returns a dict of acadSem
def load_course_year():
    try:
        # Try to requests the content of this website
        response = requests.get('https://wish.wis.ntu.edu.sg/webexe/owa/aus_schedule.main')
        if response.status_code != 200:
            print(f'DataSource Error! Status Code: {response.status_code}')
            return {}
        else:
            # Parse the request to soup and get the first select tag's children
            course_year_list = BeautifulSoup(response.text, 'html.parser').find('select').contents
            # Remove the /n in the list
            course_year_list = [elem for elem in course_year_list if elem != '\n']
            # Get the value(key) and string(value) of every element in the list and store it as a dictionary
            course_year_dict = {elem['value']: elem.string for elem in course_year_list}
            return course_year_dict
    except Exception as err:
        print(f'DataSource load_course_year Exception Error! Error msg: {err}')
        return {}
