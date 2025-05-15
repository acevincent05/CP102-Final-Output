import mysql.connector

class ConnectDatabase:
    def __init__(self):
        self._host = "127.0.0.1"
        self._port = 3306
        self._user = "root"
        self._password = "CS2025EU"
        self._database = "movie_manager"
        self.con = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.con = mysql.connector.connect(
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._password,
                database=self._database
            )
            self.cursor = self.con.cursor()
            print("Connected to database.")
        except mysql.connector.Error as err:
            print(f"Database connection failed: {err}")
