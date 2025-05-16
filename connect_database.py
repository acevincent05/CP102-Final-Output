import mysql.connector

# for database connection
class ConnectDatabase:
    def __init__(self): # intializes MySQL credentials
        self._user = "root"
        self._password = "CS2025EU"
        self._database = "movie_manager"
        self.con = None
        self.cursor = None
        self.connect()

    def connect(self): # connects to the database with credentials
        try:
            self.con = mysql.connector.connect(
                user=self._user,
                password=self._password,
                database=self._database
            )
            self.cursor = self.con.cursor()  
            print("Database connected.")
        except mysql.connector.Error as err:
            print(f"Failed to connect: {err}")
            self.cursor = None  
