from Rates import Rates
from DBConnector import DBConnector
from threading import Thread
from time import sleep


def update_prices_in_second_thread():
    global connected
    while True:
        if not connected:
            connected = True
            rates = Rates()
            connection = DBConnector("127.0.0.1", "mydb", "root", "")
            connection.connect()
            connection.update_prices(rates)
            connection.close()
            connected = False
        else:
            sleep(60)
            continue
        sleep(3600 * 12)


def update_prices():
    rates = Rates()
    connection = DBConnector("localhost", "mydb", "root", "")
    print(connection.connect())
    print(connection.update_prices(rates))
    print(connection.close())


def generate_excel():
    connection = DBConnector("localhost", "mydb", "root", "")
    print(connection.connect())
    print(connection.get_products())
    print(connection.close())


if __name__ == '__main__':
    connected = False
    t1 = Thread(target=update_prices_in_second_thread)
    t1.daemon = True
    t1.start()
    user_input = ""
    while user_input.lower() != 'q':
        print("Avaiable Commands:")
        print("u - Updates dabase with live exchange rates from NBP")
        print("g - Generate excel file with all products from database")
        print("q - Quits program")
        print("By default database is updated every 12 hours when this app is open.")
        user_input = input()
        match user_input.lower():
            case "u":
                if not connected:
                    update_prices()
                else:
                    print("App is updating database, try again in a few seconds")
            case "g":
                if not connected:
                    generate_excel()
                else:
                    print("App is updating database, try again in a few seconds")
            case "q":
                SystemExit()
            case _:
                print("Wrong command.")
