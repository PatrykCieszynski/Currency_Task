from unittest import TestCase, main as run_tests
from Rates import Rates
from DBConnector import DBConnector

from mock import patch
from decimal import Decimal
from pandas import DataFrame, read_excel
from os.path import exists
from os import remove

USD_URL = "https://api.nbp.pl/api/exchangerates/rates/A/USD"
EUR_URL = "https://api.nbp.pl/api/exchangerates/rates/A/EUR"


class TestRates(TestCase):
    @patch.object(Rates, "request_usd")
    @patch.object(Rates, "request_eur")
    def test_setters(self, fake_request_eur, fake_request_usd):
        usd = "4.44"
        eur = "5.3231313"
        fake_request_usd.return_value = usd
        fake_request_eur.return_value = eur
        rates = Rates("url1", "url2")
        self.assertIsInstance(rates, Rates)
        self.assertEqual(rates.USD, Decimal(usd))
        self.assertEqual(rates.EUR, Decimal(eur))

    def test_requests(self):
        self.assertIsNotNone(Rates.request_usd(USD_URL))
        self.assertIsNotNone(Rates.request_eur(EUR_URL))
        self.assertRaises(ConnectionError, lambda: Rates(USD_URL, "http://wrong_url"))
        self.assertRaises(ConnectionError, lambda: Rates("http://wrong_url", EUR_URL))
        self.assertRaises(ConnectionError, lambda: Rates("http://wrong_url", "wrong_url"))


class TestDBConnector(TestCase):
    def test_initialization(self):
        host = "localhost"
        dbname = "mydb"
        username = "root"
        password = ""
        db_connector = DBConnector(host, dbname, username, password)
        self.assertIsInstance(db_connector, DBConnector)
        self.assertEqual(db_connector.host, host)
        self.assertEqual(db_connector.dbname, dbname)
        self.assertEqual(db_connector.username, username)
        self.assertEqual(db_connector.password, password)
        self.assertIsNone(db_connector.engine)
        self.assertIsNone(db_connector.connection)

    def test_valid_connection(self):
        host = "localhost"
        dbname = "mydb"
        username = "root"
        password = ""
        db_connector = DBConnector(host, dbname, username, password)
        db_connector.connect()
        self.assertIsNotNone(db_connector.connection)
        db_connector.close()

    def test_invalid_port(self):
        host = "localhost:3000"
        dbname = "mydb"
        username = "root"
        password = ""
        db_connector = DBConnector(host, dbname, username, password)
        self.assertRaises(ConnectionError, db_connector.connect)

    def test_invalid_databse(self):
        host = "localhost"
        dbname = "mydbb"
        username = "root"
        password = ""
        db_connector = DBConnector(host, dbname, username, password)
        self.assertRaises(ConnectionError, db_connector.connect)

    def test_invalid_account(self):
        host = "localhost"
        dbname = "mydb"
        username = "roof"
        password = ""
        db_connector = DBConnector(host, dbname, username, password)
        self.assertRaises(ConnectionError, db_connector.connect)

    @patch.object(DBConnector, "get_products")
    def test_create_excel(self, fake_get_products):
        if exists("test_products.xlsx"):
            remove("test_products.xlsx")
        self.assertFalse(exists("test_products.xlsx"))
        fake_get_products.return_value = DataFrame({"ProductID": ["PR1"],
                                                    "DepartmentID": ["D1111"],
                                                    "Category": ["Tablet"],
                                                    "IDSKU": ["SKU1111"],
                                                    "ProductName": ["TabletName"],
                                                    "Quantity": [4],
                                                    "UnitPrice": [25],
                                                    "UnitPriceUSD": [33],
                                                    "UnitPriceEURO": [66],
                                                    "Ranking": [66],
                                                    "UnitsInStock": [233],
                                                    "UnitsInOrder": [111]}).set_index("ProductID")
        db_connector = DBConnector("", "", "", "")
        db_connector.create_excel("test_products")
        self.assertTrue(exists("test_products.xlsx"))
        df = read_excel("test_products.xlsx", sheet_name=0).set_index("ProductID")
        self.assertTrue(df.equals(db_connector.get_products()))


if __name__ == "__main__":
    run_tests()
