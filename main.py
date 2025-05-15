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

    def loaddata(self):
        con = mysql.connector.connect(user = 'root', 
                                        password = 'CS2025EU', 
                                        host = 'localhost', 
                                        database= 'movie_manager')
        cur = con.cursor()
        sqlstr = '''SELECT 
                        m.movie_id,
                        m.movie_name,
                        m.release_year,
                        g.genre_name,
                        s.studio_name
                    FROM 
                        movie m
                    JOIN 
                        genre g ON m.genre_id = g.genre_id
                    JOIN 
                        studio s ON m.studio_id = s.studio_id
                    ORDER BY 
                        m.movie_id;'''
        
        tablerow=0
        results = cur.execute(sqlstr)
        self.tableWidget.setRowCount(40)
        for row in results:
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            tablerow+=1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = main()
    ui.show()
    app.exec_()