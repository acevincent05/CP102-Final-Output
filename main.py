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
        self.tableWidget.setHorizontalHeaderLabels(['movie_id',
                                                  'movie_name',
                                                  'release_year',
                                                  'genre_name',
                                                  'studio_name'])

    def load_data(self):
        query = '''SELECT 
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
            
        self.db.cursor.execute(query)

        results = self.db.cursor.fetchall() # Get all results
        
        # Set row count based on actual results
        self.tableWidget.setRowCount(len(results))
        
        for tablerow, row in enumerate(results):
            # Convert all values to strings for QTableWidgetItem
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(str(row[1])))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(str(row[2])))
            self.tableWidget.setItem(tablerow, 3, QTableWidgetItem(str(row[3])))
            self.tableWidget.setItem(tablerow, 4, QTableWidgetItem(str(row[4])))
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = main()
    ui.show()
    sys.exit(app.exec_())