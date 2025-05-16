from PyQt5.QtWidgets import (QMainWindow, QApplication, QMessageBox, 
                             QTableWidgetItem, QTableWidget, QLabel, QDialog) # for PyQt5 features
from PyQt5.uic import loadUi # directly loads the ui file
import sys #
from connect_database import ConnectDatabase #separate python file for DB connection
from MovieDetailsDialog import MovieDetailsDialog #separate python file movie details
from AddMovieDialog import AddMovieDetailsDialog #separate python file for inputting new movies
from EditMovieDetailsDialog import EditMovieDetailsDialog #separate python file for inputting movies to edit

class main_window(QMainWindow): # the main window
    def __init__(self): 
        super(main_window, self).__init__() # initializes the window's function
        loadUi("main.ui", self) # directly loads the main UI without converting it to a py file
        
        self.db = ConnectDatabase() # connect to MySQL DB

        self.display_all() # displays the current datas on the table

        self.show_all_movies.clicked.connect(self.display_all) # shows main table
        self.show_genres.clicked.connect(self.display_genres) # shows genres table
        self.show_studios.clicked.connect(self.display_studios) # shows studios table

        self.view_btn.clicked.connect(self.get_selected_data) #view button
        self.add_btn.clicked.connect(self.open_add_movie_dialog) # add button
        self.edit_btn.clicked.connect(self.open_edit_movie_dialog) # edit button
        self.delete_btn.clicked.connect(self.delete_movie)  # delete button

    # edit a certain movie in the DB 
    def open_edit_movie_dialog(self):
        selected_items = self.tableWidget.selectedItems() # select movie through clicking rows
        
        if not selected_items: # if nothing was selected or empty
            QMessageBox.warning(self, "No Selection", "Please select a movie to edit.")
            return

        # selects the specific cell
        row = selected_items[0].row() 
        movie_id_item = self.tableWidget.item(row, 0) 
        
        # handle error for invalid input
        if not movie_id_item:
            QMessageBox.warning(self, "Error", "Could not get movie ID for editing.")
            return

        # movie ID as text     
        movie_id = movie_id_item.text()

        try:
            if not self.db or not self.db.cursor: # handles DB connection error
                raise Exception("Database not connected.")
            
            cursor = self.db.cursor
            
            # DB query for fetching details later 
            query = ''' 
                SELECT 
                    m.movie_id,
                    m.movie_name,
                    m.release_year,
                    g.genre_id,  -- Make sure genre_id is selected
                    g.genre_name,
                    s.studio_name,
                    s.studio_id, -- Make sure studio_id is selected
                    s.founded_year,
                    s.headquarters
                FROM 
                    movie m
                JOIN 
                    genre g ON m.genre_id = g.genre_id
                JOIN 
                    studio s ON m.studio_id = s.studio_id
                WHERE 
                    m.movie_id = %s;
            '''
            # executing the query with the inputted primary key
            cursor.execute(query, (movie_id,))
            movie_data = cursor.fetchone() # fetching the selected movie
            
            if not movie_data: # handle invalid selection
                QMessageBox.warning(self, "Not Found", "No details found for selected movie to edit.")
                return

            # passes the fetched movie_data to the dialog
            dialog = EditMovieDetailsDialog(self.db, movie_data)
            if dialog.exec_() == QDialog.Accepted:
                self.display_all() # refresh table after successful edit
        
        except Exception as e: # handles error when loading data from DB
            QMessageBox.critical(self, "Error", f"Could not load movie data for editing:\n{str(e)}")

    # add a movie with its details
    def open_add_movie_dialog(self): 
        dialog = AddMovieDetailsDialog(self.db) # dialog for inputting details
        if dialog.exec_() == QDialog.Accepted:
            self.display_all() # refresh the main table after adding a movie

    # view a movie's details
    def get_selected_data(self):
        selected_items = self.tableWidget.selectedItems() # selecting row by just clicking
        
        if not selected_items: # handles invalid selections
            QMessageBox.warning(self, "No Selection", "Please select a movie first.")
            return None
        
        # selects the specific cell
        row = selected_items[0].row()
        movie_id_item = self.tableWidget.item(row, 0)
        
        # handle error for invalid input
        if not movie_id_item:
            QMessageBox.warning(self, "Error", "Could not get movie ID.")
            return None
        
        # movie ID as text
        movie_id = movie_id_item.text()
        
        try:
            if not self.db or not self.db.cursor: # handles DB connection error
                raise Exception("Database not connected.")
            
            # DB query for fetching details later 
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
            
            # executing the query with the inputted primary key
            cursor.execute(query, (movie_id,))
            row_data = cursor.fetchone() # fetching the selected movie
            
            if not row_data: # handles invalid selections
                QMessageBox.warning(self, "Not Found", "No details found for selected movie.")
                return None

            dialog = MovieDetailsDialog(row_data, self) # opens the details of the movie in a dialog
            dialog.exec_()
            return row_data
    
        except Exception as e: # handles error when loading data from DB
            QMessageBox.critical(self, "Error", f"Could not load data:\n{str(e)}")
            return None
        
    def delete_movie(self):
        selected_items = self.tableWidget.selectedItems() #Deletes the selected movie from the database after confirmation.

        if not selected_items: # handles invalid selections
            QMessageBox.warning(self, "No Selection", "Please select a movie to delete.")
            return

        row = selected_items[0].row()
        movie_id_item = self.tableWidget.item(row, 0)  # get Movie ID from the first column

        if not movie_id_item: # handles invalid inputs
            QMessageBox.warning(self, "Error", "Could not get movie ID for deletion.")
            return

        # movie ID as text
        movie_id = movie_id_item.text() 

        # Confirmation dialog
        confirmation = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete movie with ID {movie_id}?",
            QMessageBox.Yes | QMessageBox.No,  # use Yes and No buttons
            QMessageBox.No,  # default button is No
        )

        if confirmation == QMessageBox.Yes: # proceeds to deletion
            try:
                if not self.db or not self.db.cursor:
                    raise Exception("Database not connected.")

                cursor = self.db.cursor
                query = "DELETE FROM movie WHERE movie_id = %s" # uses primary to delete
                cursor.execute(query, (movie_id,))
                self.db.con.commit()  # Use self.db.con to commit

                QMessageBox.information(self, "Success", "Movie deleted successfully!")
                self.display_all()  # refresh the table after deletion

            except Exception as e:
                self.db.con.rollback()  # Use self.db.con to rollback
                QMessageBox.critical(self, "Error", f"Could not delete movie:\n{str(e)}")   

    # shows all current movies in the database
    def display_all(self):
        try:
            if not self.db or not self.db.cursor: # handles DB connection error
                raise Exception("Database not connected.")
            
            # DB query for fetching details later 
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
            # executing the query 
            self.db.cursor.execute(query)
            results = self.db.cursor.fetchall() # fetching all the datas in the table

            headers = ["ID", "Title", "Year", "Genre", "Studio"] # name of the headers that will be displayed
            self.tableWidget.setColumnCount(len(headers)) # counts columns
            self.tableWidget.setHorizontalHeaderLabels(headers) # assign the headers that will be shown
            self.tableWidget.setRowCount(len(results)) # counts rows

            # builds the table based on the number of columns and rows while also placing their data
            for row_idx, row_data in enumerate(results):
                for col_idx, value in enumerate(row_data):
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            self.tableWidget.resizeColumnsToContents() # resizes the columns based on text length

            # enables row selection
            self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
            self.tableWidget.setSelectionMode(QTableWidget.SingleSelection)

        except Exception as e: # handles error when loading data from DB
            QMessageBox.critical(self, "Error", f"Could not load data:\n{str(e)}")

    # display the genre table 
    def display_genres(self):
        try:
            if not self.db or not self.db.cursor: # handles database connection failure
                raise Exception("Database not connected.")

            query = 'SELECT * FROM genre' # query for selecting all contents in the table

            self.db.cursor.execute(query) # executing the query
            results = self.db.cursor.fetchall() # fetching the data

            headers = ["Genre ID", "Genre Name"] # for headers to be displayed 
            self.tableWidget.setColumnCount(len(headers)) # counts number of columns
            self.tableWidget.setHorizontalHeaderLabels(headers) # assign the headers that will be shown
            self.tableWidget.setRowCount(len(results)) # counts rows

            # builds the table based on the number of columns and rows while also placing their data
            for row_idx, row_data in enumerate(results):
                for col_idx, value in enumerate(row_data):
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            self.tableWidget.resizeColumnsToContents() # resizes the columns based on text length

        except Exception as e: # handles error when loading data from DB
            QMessageBox.critical(self, "Error", f"Could not load data:\n{str(e)}")

    # displays the studios table
    def display_studios(self):
        try:
            if not self.db or not self.db.cursor: # handles database connection failure
                raise Exception("Database not connected.") 

            query = 'SELECT * FROM studio' # query for selecting all contents in the table

            self.db.cursor.execute(query) # executing the query
            results = self.db.cursor.fetchall() # fetching the data

            headers = ["Studio ID", "Studio Name", "Year Founded", "Headquartes"] # for headers to be displayed
            self.tableWidget.setColumnCount(len(headers)) # counts number of columns
            self.tableWidget.setHorizontalHeaderLabels(headers) # assign the headers that will be shown
            self.tableWidget.setRowCount(len(results)) # counts rows

            # builds the table based on the number of columns and rows while also placing their data
            for row_idx, row_data in enumerate(results):
                for col_idx, value in enumerate(row_data):
                    self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            self.tableWidget.resizeColumnsToContents() # resizes the columns based on text length

        except Exception as e: # handles error when loading data from DB
            QMessageBox.critical(self, "Error", f"Could not load data:\n{str(e)}")

# executes the program in the main window
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec_())

