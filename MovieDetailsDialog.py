from PyQt5.QtWidgets import QLabel, QDialog, QFormLayout, QPushButton

# for getting the details of a movie
class MovieDetailsDialog(QDialog):
    def __init__(self, movie_data, parent=None):
        super().__init__(parent) 
        self.setWindowTitle("Movie Details") # window name
        self.setModal(True) # blocks interaction with other windows in the application
        self.resize(400, 300) # windows size
        
        layout = QFormLayout() # for arrangement of the data
        
        # movie Information Section
        layout.addRow(QLabel("<b>Movie Information</b>"))
        layout.addRow("ID:", QLabel(str(movie_data[0])))
        layout.addRow("Title:", QLabel(str(movie_data[1])))
        layout.addRow("Release Year:", QLabel(str(movie_data[2])))
        
        # genre Information Section
        layout.addRow(QLabel("<b>Genre Information</b>"))
        layout.addRow("Genre ID:", QLabel(str(movie_data[3])))
        layout.addRow("Genre Name:", QLabel(str(movie_data[4])))
        
        # studio Information Section
        layout.addRow(QLabel("<b>Studio Information</b>"))
        layout.addRow("Studio Name:", QLabel(str(movie_data[5])))
        layout.addRow("Studio ID:", QLabel(str(movie_data[6])))
        layout.addRow("Founded Year:", QLabel(str(movie_data[7])))
        layout.addRow("Headquarters:", QLabel(str(movie_data[8])))
        
        # add a close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addRow(close_btn)
        
        self.setLayout(layout)