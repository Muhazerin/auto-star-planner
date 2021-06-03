from PyQt5.QtWidgets import QMainWindow

from ui import mainwindow

from selectAcadSemDialog import SelectAcadSemDialog


class AutoStarPlanner(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        super(AutoStarPlanner, self).__init__()
        self.setupUi(self)

        self.select_acad_sem_dialog = SelectAcadSemDialog()

        self.actionFrom_Website.triggered.connect(self.select_acad_sem_dialog.run)
