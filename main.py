from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import sys
from connect_database import ConnectDatabase

class main(QMainWindow):
    def __init__(self):
        super(main, self).__init__()
        loadUi("main.ui", self)
        
        self.db = ConnectDatabase()

        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 250)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 215)
        self.load_data()
        '''self.tableWidget.setHorizontalHeaderLabels(['movie_id',
                                                  'movie_name',
                                                  'release_year',
                                                  'genre_name',
                                                  'studio_name'])'''
        

    def load_data(self):
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
        
        try:
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()

            # Set up table structure
            headers = ["ID", "Title", "Year", "Genre", "Studio"]
            self.tableWidget.setColumnCount(len(headers))
            self.tableWidget.setHorizontalHeaderLabels(headers)
            self.tableWidget.setRowCount(len(results))

            # Insert data
            for row_idx, row_data in enumerate(results):
                for col_idx, value in enumerate(row_data):
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            self.tableWidget.resizeColumnsToContents()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load data:\n{str(e)}")
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = main()
    ui.show()
    sys.exit(app.exec_())