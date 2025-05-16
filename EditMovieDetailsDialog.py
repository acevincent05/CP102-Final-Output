# EditMovieDetailsDialog.py
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi

class EditMovieDetailsDialog(QDialog):
    def __init__(self, db_connection, movie_data): # Receives pre-fetched movie_data
        super(EditMovieDetailsDialog, self).__init__()
        loadUi("AddMovieDialog.ui", self) # Reuses the same UI file
        self.db = db_connection
        self.movie_data = movie_data # Store the data for populating fields

        self.populate_fields() # Call this to fill the fields on dialog open

        # Change button text and connect to update function
        # Make sure 'add_movie_button' is the objectName of your Add/OK button in AddMovieDialog.ui
        self.buttonBox.clicked.connect(self.update_movie)

    def populate_fields(self):
        # Unpack the movie_data tuple.
        # IMPORTANT: Order MUST match the SELECT query in main_window.py's open_edit_movie_dialog
        (movie_id, movie_name, release_year, genre_id, genre_name, 
         studio_name, studio_id, founded_year, headquarters) = self.movie_data

        # Populate the QLineEdit fields
        # IMPORTANT: These object names MUST match your AddMovieDialog.ui
        self.add_movie_id.setText(str(movie_id))
        self.add_movie_id.setEnabled(False) # Movie ID usually shouldn't be editable
        self.add_movie_title.setText(movie_name)
        self.add_movie_year.setText(str(release_year))
        self.add_genre_id.setText(str(genre_id))
        self.add_genre_name.setText(genre_name)
        self.add_studio_id.setText(str(studio_id))
        self.add_studio_name.setText(studio_name)
        self.add_founded_year.setText(str(founded_year))
        self.add_headquarters.setText(headquarters)


    def update_movie(self):
        # Get updated data from the QLineEdit fields
        movie_id = self.add_movie_id.text() 
        movie_title = self.add_movie_title.text()
        release_year = self.add_movie_year.text()
        genre_id = self.add_genre_id.text()
        genre_name = self.add_genre_name.text()
        studio_id = self.add_studio_id.text()
        studio_name = self.add_studio_name.text()
        founded_year = self.add_founded_year.text()
        headquarters = self.add_headquarters.text()

        # Basic validation
        if not all([movie_id, movie_title, release_year, genre_id, genre_name, studio_id, studio_name, founded_year, headquarters]):
            QMessageBox.warning(self, "Missing Data", "Please fill in all fields.")
            return

        try:
            # Check if genre exists, if not, insert it. Otherwise, update it.
            self.db.cursor.execute("SELECT genre_id FROM genre WHERE genre_id = %s", (genre_id,))
            if not self.db.cursor.fetchone():
                self.db.cursor.execute("INSERT INTO genre (genre_id, genre_name) VALUES (%s, %s)", (genre_id, genre_name))
            else:
                self.db.cursor.execute("UPDATE genre SET genre_name = %s WHERE genre_id = %s", (genre_name, genre_id))

            # Check if studio exists, if not, insert it. Otherwise, update it.
            self.db.cursor.execute("SELECT studio_id FROM studio WHERE studio_id = %s", (studio_id,))
            if not self.db.cursor.fetchone():
                self.db.cursor.execute("INSERT INTO studio (studio_id, studio_name, founded_year, headquarters) VALUES (%s, %s, %s, %s)", (studio_id, studio_name, founded_year, headquarters))
            else:
                self.db.cursor.execute("UPDATE studio SET studio_name = %s, founded_year = %s, headquarters = %s WHERE studio_id = %s", (studio_name, founded_year, headquarters, studio_id))

            # Update movie data
            query = """
                UPDATE movie 
                SET movie_name = %s, release_year = %s, genre_id = %s, studio_id = %s
                WHERE movie_id = %s
            """
            self.db.cursor.execute(query, (movie_title, release_year, genre_id, studio_id, movie_id))

            self.db.con.commit() # Use self.db.con

            QMessageBox.information(self, "Success", "Movie updated successfully!")
            self.accept() # Close the dialog with Accepted status
        except Exception as e:
            self.db.con.rollback() # Use self.db.con
            QMessageBox.critical(self, "Error", f"Could not update movie: {str(e)}")