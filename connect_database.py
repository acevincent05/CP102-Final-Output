import mysql.connector
from mysql.connector import errorcode

class ConnectDatabase:
    def __init__(self):
        self._host = "127.0.0.1"
        self._port = 3306
        self._user = "root"
        self._password = "CS2025EU"
        self._database = "movie_manager"
        self.con = None
        self.cursor = None

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
            print("Database connection successful.")
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error: Invalid username or password.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Error: Database does not exist.")
            else:
                print(f"Error: {err}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.con:
            self.con.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.con.commit()
            return self.cursor
        except mysql.connector.Error as err:
            print(f"Query execution error: {err}")
            return None
