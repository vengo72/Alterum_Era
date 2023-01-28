import sqlite3
import sys
import config

from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QInputDialog
from PyQt5 import QtCore

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
        config.first_player_name = self.showDialog()
        config.second_player_name = self.showDialog()
        self.hide()
        main_cycle()

    def leaderboard(self):
        if ax.isHidden() == True:
            ax.show()
        else:
            ax.hide()
    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Выбор имени',
            'Введите имя игрока')

        if ok:
            return text

    def other(self):
        pass


class MyWidget_2(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        DB_NAME = 'Alterum_Era_DB.db'
        self.con = sqlite3.connect(DB_NAME)
        self.resize(600, 280)
        self.tableWidget.setGeometry(QtCore.QRect(70, 40, 450, 200))
        self.model = QSqlTableModel()
        # self.tableWidget.setModel(self.model)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Имя Игрока', 'Очки', 'Место'])
        cur = self.con.cursor()
        data = cur.execute("SELECT * FROM Main").fetchall()
        data.sort(key=lambda x: int(x[-2]), reverse=True)
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(4)
        for i in range(len(data)):
            for j in range(len(data[i]) - 1):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(data[i][j])))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(i + 1)))

        for i in range(len(data)):
            cur = self.con.cursor()
            que = "UPDATE Main\nSET"
            que += ' Leaderboard = ?\n'
            que += "WHERE id = ?"
            cur.execute(que,
                        (self.tableWidget.item(i, 3).text(), self.tableWidget.item(i, 0).text()))
            self.con.commit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    ax = MyWidget_2()
    ax.hide()
    sys.exit(app.exec_())
