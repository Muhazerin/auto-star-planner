# Auto Star Planner
Why take 1 hour to plan your semester when someone took more than 1 week to automate that task for you  
![](https://img.shields.io/badge/platform-Windows%2010-blue) ![](https://img.shields.io/badge/language-Python%203-yellow)
![](https://i.imgur.com/iBGLqNN.gif)

## About the project
The project is separated in different modules. The bare skeleton of the project (without the modules) is simple mainwindow 
![](https://i.imgur.com/ZuSmVFT.png)
This way, each dialog can be independent from other dialogs. This makes it easier to add more functionalities to the application in the future.   
All the possible timetable(plan) is communicated across different dialog via the [observer pattern](https://en.wikipedia.org/wiki/Observer_pattern). The plan is the subject and the dialogs are the observer.  
### Modules
####[Add/Remove Subjects](https://github.com/Muhazerin/auto-star-planner/tree/main/src/ui/dialog/addRemoveSubjectsDialog)  
This module enables the user to add and remove subjects
####[Filter Subjects](https://github.com/Muhazerin/auto-star-planner/tree/main/src/ui/dialog/filterSubjectsDialog)
This module enables the user to filter each subjects to a specific index

## Project Setup
### Requirements
* Python 3  

After installing python, install these packages
```
pip install pyqt5  
pip install beautifulsoup4
```

## Source Code
The source code can be found in the src folder.  
The entry point of the application is main.py in the src folder

## Attributes
Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
