from PyQt5.QtWidgets import QLabel, QDialog, QFormLayout, QPushButton

class MovieDetailsDialog(QDialog):
    def __init__(self, movie_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Movie Details")
        self.setModal(True)
        self.resize(400, 300)  
        
        layout = QFormLayout()
        
        # Movie Information Section
        layout.addRow(QLabel("<b>Movie Information</b>"))
        layout.addRow("ID:", QLabel(str(movie_data[0])))
        layout.addRow("Title:", QLabel(str(movie_data[1])))
        layout.addRow("Release Year:", QLabel(str(movie_data[2])))
        
        # Genre Information Section
        layout.addRow(QLabel("<b>Genre Information</b>"))
        layout.addRow("Genre ID:", QLabel(str(movie_data[3])))
        layout.addRow("Genre Name:", QLabel(str(movie_data[4])))
        
        # Studio Information Section
        layout.addRow(QLabel("<b>Studio Information</b>"))
        layout.addRow("Studio Name:", QLabel(str(movie_data[5])))
        layout.addRow("Studio ID:", QLabel(str(movie_data[6])))
        layout.addRow("Founded Year:", QLabel(str(movie_data[7])))
        layout.addRow("Headquarters:", QLabel(str(movie_data[8])))
        
        # Add a close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addRow(close_btn)
        
        self.setLayout(layout)