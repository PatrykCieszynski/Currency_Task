from decimal import *
from Rates import Rates
from DBConnector import DBConnector


if __name__ == '__main__':
    rates = Rates()
    money = Decimal(12.53)
    usd = rates.convert_to_usd(money)
    eur = rates.convert_to_eur(money)
    print(usd, eur)

    connection = DBConnector("localhost", "mydb", "root", "")
    connection.connect()
    connection.get_products()
    connection.close()
