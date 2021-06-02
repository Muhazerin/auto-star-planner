import sys
from PyQt5.QtWidgets import QApplication

from autoStarPlanner import AutoStarPlanner

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow =AutoStarPlanner()
    mainwindow.show()
    sys.exit(app.exec())
