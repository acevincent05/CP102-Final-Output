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
        user_input = self.lineEdit.text()
        pass_input = self.lineEdit_2.text()

        try:
            con = mysql.connector.connect(user = user_input, 
                                        password = pass_input, 
                                        host = 'localhost', 
                                        database = 'movie_manager')
            print('Connection successful')
            return con
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = login_db()
    ui.show()
    app.exec_()