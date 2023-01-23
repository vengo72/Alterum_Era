import sqlite3
import sys

from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QLabel, QStyledItemDelegate, \
    QTableWidget, QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtGui import QRegExpValidator, QPalette, QColor
from StartWindow import Ui_MainWindow
from test_City import main_cycle
from RecordsWindow import Ui_Form


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.leaderboard)
        self.pushButton_3.clicked.connect(self.other)

    def start(self):
        # self.hide()
        main_cycle()

    def leaderboard(self):
        if ax.isHidden() == True:
            ax.show()
        else:
            ax.hide()

    def other(self):
        pass


class MyWidget_2(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        DB_NAME = 'Alterum_Era_DB.db'
        self.con = sqlite3.connect(DB_NAME)
        self.model = QSqlTableModel()
        # self.tableWidget.setModel(self.model)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Имя Игрока', 'Очки', 'Место'])
        cur = self.con.cursor()
        data = cur.execute("SELECT * FROM Main").fetchall()
        self.tableWidget.setRowCount(5)
        self.tableWidget.setColumnCount(4)
        for i in range(len(data)):
            print(data)
            print(data[i])
            for j in range(len(data[i])):
                print(data[i][j])
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(data[i][j])))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    ax = MyWidget_2()
    ax.hide
    sys.exit(app.exec_())
    pygame.quit()
