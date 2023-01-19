import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QLabel, QStyledItemDelegate, \
    QTableWidget, QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtGui import QRegExpValidator, QPalette, QColor
from StartWindow import Ui_MainWindow
from test_City import main_cycle


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.leaderboard)
        self.pushButton_3.clicked.connect(self.other)

    def start(self):
        self.hide()
        main_cycle()


    def leaderboard(self):
        pass

    def other(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
