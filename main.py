from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.uic import loadUi
import mysql.connector
from mysql.connector import errorcode
import sys

class main(QMainWindow):
    def __init__(self):
        super(main, self).__init__()
        loadUi("main.ui", self)
        self.tableWidget.setColumnWidth(0,100)
        self.tableWidget.setColumnWidth(1,250)
        self.tableWidget.setColumnWidth(2,100)
        self.tableWidget.setColumnWidth(3,100)
        self.tableWidget.setColumnWidth(4,215)
        self.tableWidget.setHorizontalHeaderLabels(['movie_id',
                                                    'movie_name',
                                                    'release_year',
                                                    'genre_name',
                                                    'studio_name'])
        self.loaddata()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = main()
    ui.show()
    app.exec_()