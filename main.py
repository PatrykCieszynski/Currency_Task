from decimal import *
import requests
import mysql.connector


def get_usd_rates():
    usd_url = "https://api.nbp.pl/api/exchangerates/rates/A/USD"
    return Decimal(requests.get(usd_url).json()["rates"][0]["mid"])


def get_eur_rates():
    eur_url = "https://api.nbp.pl/api/exchangerates/rates/A/EUR"
    return Decimal(requests.get(eur_url).json()["rates"][0]["mid"])


def convert_to_usd(price, usd_rate):
    price = price / usd_rate
    return price.quantize(Decimal('.01'), ROUND_HALF_UP)


def convert_to_eur(price, eur_rate):
    price = price / eur_rate
    return price.quantize(Decimal('.01'), ROUND_HALF_UP)


if __name__ == '__main__':
    try:
        USD = get_usd_rates()
        EUR = get_eur_rates()
    except requests.exceptions.RequestException as err:
        print("Could not get rates from NBP")
        raise SystemExit(err)

    money = Decimal(12.53)
    usd = convert_to_usd(money, USD)
    eur = convert_to_eur(money, EUR)
    print(usd, eur)

    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(host="localhost",
                                             database="mydb",
                                             user="root")
        if connection.is_connected():
            try:
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                query = "select database();"
                cursor.execute(query)
                record = cursor.fetchone()
                print("You're connected to database: ", record)
            except mysql.connector.Error as err:
                print("Query failed")
                raise
            finally:
                cursor.close()
                print("Cursor closed.")
    except mysql.connector.Error as err:
        print("Error while connecting to Database.", err)
    finally:
        if connection is not None:
            connection.close()
            print("Connection to Database closed.")
