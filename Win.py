# -*- coding: utf-8 -*-
import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from StartWindow import Ui_Form
from PyQt5.QtWidgets import QMainWindow


class End(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def load(self, world, player_name):
        self.tableWidget.setItem(0, 0,  QTableWidgetItem(str(world.turn_count)))
        self.tableWidget.setItem(0, 1,  QTableWidgetItem(str(world.city_count)))
        score = world.city_count * 10 - world.turn_count
        self.tableWidget.setItem(0, 2,  QTableWidgetItem(str(score)))
        con = sqlite3.connect('Alterum_Era_DB.db')
        cur = con.cursor()
        que = "INSERT into Main(Player, Score) VALUES(?, ?)"
        cur.execute(que,
                    (player_name, score))
        con.commit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = End()
    ex.show()
    sys.exit(app.exec_())
