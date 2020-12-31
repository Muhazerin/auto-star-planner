# Auto Star Planner
Why take 1 hour to plan your semester when someone took 1 month to automate that task for you  
![](https://img.shields.io/badge/platform-Windows%2010-blue) ![](https://img.shields.io/badge/language-Python%203-yellow)
![](https://i.imgur.com/iBGLqNN.gif)

## About the project
The project is separated into different modules. The bare skeleton of the project (without the modules) is simple mainwindow 
![](https://i.imgur.com/ZuSmVFT.png)
This way, each module can be independent from other modules. This makes it easier to add more functionalities to the application in the future.   
All the possible timetable(plan) is communicated across different modules via the [observer pattern](https://en.wikipedia.org/wiki/Observer_pattern). The plan is the subject and the modules are the observer.  
### Modules
If loaded successfully, the modules will appear in the "Extension" tab  
* [Add/Remove Subjects](https://github.com/Muhazerin/auto-star-planner/tree/main/src/ui/dialog/addRemoveSubjectsDialog)  
    * This module enables the user to add and remove subjects   
  
* [Filter Subjects](https://github.com/Muhazerin/auto-star-planner/tree/main/src/ui/dialog/filterSubjectsDialog)  
    * This module enables the user to filter each subjects to a specific index
    
* [Plan with Friends](https://github.com/Muhazerin/auto-star-planner/tree/main/src/ui/dialog/planWithFriendsDialog)
    * This module allows the user to add in their friend's plan and filter the common indexes
### Tips for creating new module
The module are to be created with pyqt  
1. Place your exampleModule.py inside exampleModuleDialog folder
2. Inside your exampleModule.py, you will need,
    1. A class called Dialog, taking mainPotentialPlan as parameter
    2. updatePlan() method
    3. getWindowName() method

## Project Setup
### Requirements
* Python 3  

After installing python, install these packages
```
pip install -r requirements.txt
```

## Source Code
The source code can be found in the src folder.  
The entry point of the application is app.py in the src folder

## Attributes
Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
