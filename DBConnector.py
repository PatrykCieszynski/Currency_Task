import mysql.connector


class DBConnector:
    def __init__(self, host, dbname, username, password):
        self.host = host
        self.dbname = dbname
        self.username = username
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(host=self.host,
                                                      database=self.dbname,
                                                      user=self.username,
                                                      password=self.password)
            print("Connected to MySQL Server version ", self.connection.get_server_info())
        except mysql.connector.Error as err:
            print("Error while connecting to Database.", err)
            raise SystemExit(err)

    def get_products(self):
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("select * from product")
            records = self.cursor.fetchall()
            for record in records:
                print(record)
        except mysql.connector.Error as err:
            print("Query failed", err)
        finally:
            if self.cursor is not None:
                self.cursor.close()
                print("Cursor closed.")

    def close(self):
        if self.connection is not None:
            self.connection.close()
            print("Connection to Database closed.")
