from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi

class AddMovieDetailsDialog(QDialog):
    def __init__(self, db_connection):
        super(AddMovieDetailsDialog, self).__init__()
        loadUi("AddMovieDialog.ui", self)
        self.db = db_connection
        # Ensure this button name matches your .ui file (e.g., 'add_movie_button' or 'add_btn')
        self.buttonBox.clicked.connect(self.add_movie)

    def add_movie(self):
        # Get data from the QLineEdit fields
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
            # Check if genre exists, if not, insert it
            self.db.cursor.execute("SELECT genre_id FROM genre WHERE genre_id = %s", (genre_id,))
            if not self.db.cursor.fetchone():
                self.db.cursor.execute("INSERT INTO genre (genre_id, genre_name) VALUES (%s, %s)", (genre_id, genre_name))

            # Check if studio exists, if not, insert it
            self.db.cursor.execute("SELECT studio_id FROM studio WHERE studio_id = %s", (studio_id,))
            if not self.db.cursor.fetchone():
                self.db.cursor.execute("INSERT INTO studio (studio_id, studio_name, founded_year, headquarters) VALUES (%s, %s, %s, %s)", (studio_id, studio_name, founded_year, headquarters))

            # Insert movie data
            query = """
                INSERT INTO movie (movie_id, movie_name, release_year, genre_id, studio_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.db.cursor.execute(query, (movie_id, movie_title, release_year, genre_id, studio_id))
            
            # --- CHANGE THIS LINE ---
            # From: self.db.connection.commit()
            self.db.con.commit()
            
            QMessageBox.information(self, "Success", "Movie added successfully!")
            self.accept() # Close the dialog if successful
        except Exception as e:
            # --- CHANGE THIS LINE ---
            # From: self.db.connection.rollback()
            self.db.con.rollback() # Rollback in case of error
            QMessageBox.critical(self, "Error", f"Could not add movie: {str(e)}")