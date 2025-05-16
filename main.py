from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QTableWidget, QLabel, QDialog, QFormLayout
from PyQt5.uic import loadUi
import sys
from connect_database import ConnectDatabase

class main_window(QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        loadUi("main.ui", self)
        
        self.db = ConnectDatabase()

        self.display_all()

        #initializes buttons
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
            return  # No selection
        
        # Get all data from the selected row
        row = selected_items[0].row()
        row_data = []
        for col in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(row, col)
            row_data.append(item.text() if item else "")
        
        # Create and show the details dialog
        dialog = MovieDetailsDialog(row_data, self)
        dialog.exec_()
 
    
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

class MovieDetailsDialog(QDialog):
    def __init__(self, movie_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Movie Details")
        self.setModal(True)  # Makes the dialog modal
        self.resize(300, 200)
        
        layout = QFormLayout()
        
        # Create labels for each piece of data
        layout.addRow("ID:", QLabel(movie_data[0]))
        layout.addRow("Title:", QLabel(movie_data[1]))
        layout.addRow("Year:", QLabel(movie_data[2]))
        layout.addRow("Genre:", QLabel(movie_data[3]))
        layout.addRow("Studio:", QLabel(movie_data[4]))
        
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())

