from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import sys
import mysql.connector
from mysql.connector import errorcode

class login_db(QMainWindow):
    def __init__(self):
        super(login_db, self).__init__()
        loadUi("login.ui", self)
        self.pushButton.clicked.connect(self.login)

    def login(self):
        password = 'ace'
        entered_pass = self.lineEdit.text() 

        if password == entered_pass:
            print("Successfully logged in")
        else:
            print('unsucceful login')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = login_db()
    ui.show()
    app.exec_()