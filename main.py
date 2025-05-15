from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.uic import loadUi
import mysql.connector
from mysql.connector import errorcode
import sys

class main(QMainWindow):
    def __init__(self):
        super(main, self).__init__()
        loadUi("main.ui", self)