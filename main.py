from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.uic import loadUi
import sys
from connect_database import ConnectDatabase

class main_window(QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        loadUi("main.ui", self)
        
        self.db = ConnectDatabase()

        self.load_data()

    def load_data(self):
        try:
            if not self.db or not self.db.cursor:
                raise Exception("Database not connected.")

            query = '''
                SELECT 
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
                    m.movie_id;
            '''

            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()

            headers = ["ID", "Title", "Year", "Genre", "Studio"]
            self.tableWidget.setColumnCount(len(headers))
            self.tableWidget.setHorizontalHeaderLabels(headers)
            self.tableWidget.setRowCount(len(results))

            for row_idx, row_data in enumerate(results):
                for col_idx, value in enumerate(row_data):
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            self.tableWidget.resizeColumnsToContents()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load data:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())
