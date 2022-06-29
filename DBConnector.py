import pandas.io.sql as sql
from sqlalchemy import create_engine, exc
import logging

logger = logging.getLogger(__name__)


class DBConnector:
    def __init__(self, host, dbname, username, password):
        self.host = host
        self.dbname = dbname
        self.username = username
        self.password = password
        self.engine = None
        self.connection = None

    def connect(self):
        try:
            logger.info(f"Trying to connect to {self.host}/{self.dbname} as {self.username}")
            self.engine = create_engine(f"mysql+mysqlconnector://"
                                        f"{self.username}:{self.password}@{self.host}/{self.dbname}")
            self.connection = self.engine.connect()
        except exc.SQLAlchemyError as err:
            logger.error(err)
            raise ConnectionError()
        else:
            logger.info("Connection successfully set")

    def update_prices(self, rates):
        try:
            logger.info(f"Trying to update prices with USD {rates.USD}, EUR {rates.EUR}")
            query = f"UPDATE product SET" \
                    f" UnitPriceUSD = ROUND(UnitPrice * {rates.USD}, 2)," \
                    f" UnitPriceEURO = ROUND(UnitPrice * {rates.EUR}, 2)"
            self.connection.execute(query)
        except exc.SQLAlchemyError as err:
            logger.error(err)
            print("Updating failed")
        else:
            logger.info("Prices successfully updated")

    def get_products(self):
        logger.info("Trying to query products from database")
        return sql.read_sql(("select ProductID, DepartmentID, Category, IDSKU, ProductName, Quantity, UnitPrice,"
                             " UnitPriceUSD, UnitPriceEURO, Ranking, UnitsInStock, UnitsInOrder"
                             " from product"), self.connection)

    def create_excel(self, filename):
        try:
            logger.info("Trying to query products from database")
            records = self.get_products()
        except exc.SQLAlchemyError as err:
            logger.error(err)
            print("Query failed")
        else:
            logger.info("Products successfully queried")
            try:
                records.to_excel(f"{filename}.xlsx")
            except PermissionError as err:
                logger.error(err)
                print("Saving to file failed")
            else:
                logger.info("Excel file successfully created")

    def close(self):
        if self.connection is not None:
            self.connection.close()
            logger.info(f"Closing connection to {self.host}/{self.dbname} as {self.username}")
