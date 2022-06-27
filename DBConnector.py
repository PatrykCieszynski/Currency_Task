import pandas.io.sql as sql
from sqlalchemy import create_engine, exc


class DBConnector:
    def __init__(self, host, dbname, username, password):
        self.host = host
        self.dbname = dbname
        self.username = username
        self.password = password
        self.engine = None
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.engine = create_engine(f"mysql+mysqlconnector://"
                                        f"{self.username}:{self.password}@{self.host}/{self.dbname}")
            self.connection = self.engine.connect()
            print("Connected to database at host", self.engine.url.host)
        except exc.SQLAlchemyError as err:
            raise SystemExit(err)

    def update_prices(self, rates):
        try:
            query = f"UPDATE product SET" \
                    f" UnitPriceUSD = ROUND(UnitPrice * {rates.USD}, 2)," \
                    f" UnitPriceEURO = ROUND(UnitPrice * {rates.EUR}, 2)"
            self.connection.execute(query)
            print("Update successful")
        except exc.SQLAlchemyError as err:
            print("Updating failed", err)

    def get_products(self):
        try:
            records = sql.read_sql(("select productid, departmentid, category, idsku, productname, quantity, unitprice,"
                                    " unitpriceusd,unitpriceeuro, ranking, productdesc, unitsinstock, unitsinorder"
                                    " from product"), self.connection)
            records.to_excel("products.xlsx")
            print("Created file products.xlsx")
        except exc.SQLAlchemyError as err:
            print("Query failed", err)

    def close(self):
        if self.connection is not None:
            self.connection.close()
            print("Connection to Database closed.")
