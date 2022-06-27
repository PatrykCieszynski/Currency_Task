import mysql.connector
import pandas.io.sql as sql


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

    def update_prices(self, rates):
        try:
            self.cursor = self.connection.cursor()
            query = f"UPDATE product SET" \
                    f" UnitPriceUSD = ROUND(UnitPrice * {rates.USD}, 2)," \
                    f" UnitPriceEURO = ROUND(UnitPrice * {rates.EUR}, 2)"
            self.cursor.execute(query)
            self.connection.commit()
        except mysql.connector.Error as err:
            print("Updating failed", err)
        finally:
            if self.cursor is not None:
                self.cursor.close()
                print("Cursor closed.")

    def get_products(self):
        try:
            records = sql.read_sql(("select productid, departmentid, category, idsku, productname, quantity, unitprice,"
                                    " unitpriceusd,unitpriceeuro, ranking, productdesc, unitsinstock, unitsinorder"
                                    " from product"), self.connection)
            records.to_excel("products.xlsx")
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
