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
        except exc.SQLAlchemyError as err:
            raise SystemExit(err)
        else:
            print("Connected to database at host", self.engine.url.host)

    def update_prices(self, rates):
        try:
            query = f"UPDATE product SET" \
                    f" UnitPriceUSD = ROUND(UnitPrice * {rates.USD}, 2)," \
                    f" UnitPriceEURO = ROUND(UnitPrice * {rates.EUR}, 2)"
            self.connection.execute(query)
        except exc.SQLAlchemyError as err:
            print("Updating failed", err)
        else:
            print("Update successful")

    def get_products(self):
        try:
            records = sql.read_sql(("select ProductID, DepartmentID, Category, IDSKU, ProductName, Quantity, UnitPrice,"
                                    " UnitPriceUSD, UnitPriceEURO, Ranking, UnitsInStock, UnitsInOrder"
                                    " from product"), self.connection)
            try:
                records.to_excel("products.xlsx")
            except PermissionError as err:
                print("Saving to file failed", err)
            else:
                print("Created file products.xlsx")
        except exc.SQLAlchemyError as err:
            print("Query failed", err)

    def close(self):
        if self.connection is not None:
            self.connection.close()
            print("Connection to Database closed.")
