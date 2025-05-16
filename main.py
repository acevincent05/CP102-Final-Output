from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QTableWidget, QLabel
from PyQt5.uic import loadUi
import sys
from connect_database import ConnectDatabase
from MovieDetailsDialog import MovieDetailsDialog

class main_window(QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        loadUi("main.ui", self)
        
        self.db = ConnectDatabase()

        self.display_all()

        #initialize buttons
        self.show_all_movies.clicked.connect(self.display_all)
        self.show_genres.clicked.connect(self.display_genres)
        self.show_studios.clicked.connect(self.display_studios)
        
        self.view_btn.clicked.connect(self.get_selected_data)
        
        
        # Button to get selected data
        #self.view_btn.clicked.connect(self.get_selected_data)
        
        # Label to display results
        self.result_label = QLabel('Selected data will appear here')

    def get_selected_data(self):
        selected_items = self.tableWidget.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a movie first.")
            return None
        
        row = selected_items[0].row()
        movie_id_item = self.tableWidget.item(row, 0)
        
        if not movie_id_item:
            QMessageBox.warning(self, "Error", "Could not get movie ID.")
            return None
        
        movie_id = movie_id_item.text()
        
        try:
            if not self.db or not self.db.cursor:
                raise Exception("Database not connected.")
            
            cursor = self.db.cursor
            query = '''
                SELECT 
                    m.movie_id,
                    m.movie_name,
                    m.release_year,
                    g.genre_id, 
                    g.genre_name,
                    s.studio_name,
                    s.studio_id,
                    s.founded_year,
                    s.headquarters
                FROM 
                    movie m
                JOIN 
                    genre g ON m.genre_id = g.genre_id
                JOIN 
                    studio s ON m.studio_id = s.studio_id
                WHERE 
                    m.movie_id = %s
                ORDER BY 
                    m.movie_id;
            '''
            
            # Note: Changed from ? to %s for MySQL and fixed parameter passing
            cursor.execute(query, (movie_id,))
            row_data = cursor.fetchone()
            
            if not row_data:
                QMessageBox.warning(self, "Not Found", "No details found for selected movie.")
                return None

            dialog = MovieDetailsDialog(row_data, self)
            dialog.exec_()
            return row_data
    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load data:\n{str(e)}")
            return None

    
    def display_all(self):
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

            # Enable row selection
            self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
            self.tableWidget.setSelectionMode(QTableWidget.SingleSelection)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load data:\n{str(e)}")

    def display_genres(self):
        try:
            if not self.db or not self.db.cursor:
                raise Exception("Database not connected.")

            query = 'SELECT * FROM genre'

            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()

            headers = ["Genre ID", "Genre Name"]
            self.tableWidget.setColumnCount(len(headers))
            self.tableWidget.setHorizontalHeaderLabels(headers)
            self.tableWidget.setRowCount(len(results))

            for row_idx, row_data in enumerate(results):
                for col_idx, value in enumerate(row_data):
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            self.tableWidget.resizeColumnsToContents()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load data:\n{str(e)}")

    def display_studios(self):
        try:
            if not self.db or not self.db.cursor:
                raise Exception("Database not connected.")

            query = 'SELECT * FROM studio'

            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall()

            headers = ["Studio ID", "Studio Name", "Year Founded", "Headquartes"]
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

