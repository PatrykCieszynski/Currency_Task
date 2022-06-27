from Rates import Rates
from DBConnector import DBConnector


if __name__ == '__main__':
    rates = Rates()

    connection = DBConnector("localhost", "mydb", "root", "")
    connection.connect()
    connection.update_prices(rates)
    connection.get_products()
    connection.close()
