from Rates import Rates
from DBConnector import DBConnector

import threading
from time import sleep
import os
import logging

USD_URL = "https://api.nbp.pl/api/exchangerates/rates/A/USD"
EUR_URL = "https://api.nbp.pl/api/exchangerates/rates/A/EUR"


def update_prices_in_second_thread(config):
    global is_connected_lock
    while True:
        connection = None
        success = False
        logger.info("Trying to update prices as cyclic task")
        is_connected_lock.acquire()
        try:
            rates = Rates(USD_URL, EUR_URL)
            connection = DBConnector(**config)
            connection.connect()
            connection.update_prices(rates)
            success = True
        except:
            print("Updating prices as cyclic task FAILED")
            print("Retraing in 5 minutes")
            logger.error("Updating prices as cyclic task FAILED")
            logger.info("Retrying in 5 minutes")
        finally:
            if connection is not None:
                connection.close()
            is_connected_lock.release()
            if not success:
                sleep(60 * 5)
                continue
        logger.info("Sleeping 12 hours")
        sleep(3600 * 12)


def update_prices(config):
    connection = DBConnector(**config)
    try:
        rates = Rates(USD_URL, EUR_URL)
        connection.connect()
        connection.update_prices(rates)
    except ConnectionError:
        print("Updating failed")
    else:
        print("Updating successful")
    finally:
        connection.close()


def generate_excel(config):
    connection = DBConnector(**config)
    try:
        connection.connect()
        connection.create_excel("products")
    except ConnectionError:
        print("Creating Excel file failed")
    else:
        print("Creating Excel successful")
    finally:
        connection.close()


if __name__ == '__main__':
    config = {
        "host": "localhost",
        "dbname": "mydb",
        "username": "root",
        "password": ""
    }

    path = "./logs"
    if not os.path.exists(path):
        os.makedirs("logs")
    logger = logging
    logger.basicConfig(filename="./logs/mainlog.log",
                       level=logging.INFO,
                       format="%(asctime)s | %(name)s | %(levelname)s  | %(message)s")

    is_connected_lock = threading.Lock()
    t1 = threading.Thread(target=update_prices_in_second_thread, args=[config])
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
        logger.info(f"Got '{user_input}' from user")
        match user_input.lower():
            case "u":
                is_connected_lock.acquire()
                logger.info("Trying to update prices on demand")
                update_prices(config)
                is_connected_lock.release()
            case "g":
                is_connected_lock.acquire()
                logger.info("Trying to create Excel on demand")
                generate_excel(config)
                is_connected_lock.release()
            case "q":
                logger.info("Closing app")
                SystemExit()
            case _:
                print("Wrong command.")
