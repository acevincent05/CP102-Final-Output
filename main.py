from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import sys
from connect_database import ConnectDatabase

class main_window(QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        loadUi("main.ui", self)
        
        self.db = ConnectDatabase()

        # Optional column resizing if desired
        # self.main_table.setColumnWidth(0, 100)
        # self.main_table.setColumnWidth(1, 250)
        # self.main_table.setColumnWidth(2, 100)
        # self.main_table.setColumnWidth(3, 100)
        # self.main_table.setColumnWidth(4, 215)

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
            self.main_table.setColumnCount(len(headers))
            self.main_table.setHorizontalHeaderLabels(headers)
            self.main_table.setRowCount(len(results))

            for row_idx, row_data in enumerate(results):
                for col_idx, value in enumerate(row_data):
                    self.main_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            self.main_table.resizeColumnsToContents()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load data:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())
