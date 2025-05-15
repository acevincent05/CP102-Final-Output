from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.uic import loadUi
import mysql.connector
from mysql.connector import errorcode
import sys

class login_db(QMainWindow):
    def __init__(self):
        super(login_db, self).__init__()
        loadUi("login.ui", self)

        # Ensure these match the objectName in your login.ui
        self.pushButton.clicked.connect(self.login)

    def login(self):
        user_input = self.lineEdit.text()
        pass_input = self.lineEdit_2.text()

        if not user_input or not pass_input:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password")
            return

        try:
            con = mysql.connector.connect(
                user=user_input,
                password=pass_input,
                host='localhost',
                database='movie_manager'
            )
            QMessageBox.information(self, "Success", "Connection successful")
            print('Connection successful')
            return con

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                QMessageBox.critical(self, "Login Failed", "Incorrect username or password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                QMessageBox.critical(self, "Database Error", "Database does not exist.")
            else:
                QMessageBox.critical(self, "Connection Error", str(err))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = login_db()
    ui.show()
    app.exec_()