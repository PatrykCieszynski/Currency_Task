import threading

from Rates import Rates
from DBConnector import DBConnector
from threading import Thread
from time import sleep
import os
import logging


def update_prices_in_second_thread():
    global is_connected_lock
    while True:
        connection = None
        success = False
        logger.info("Trying to update prices as cyclic task")
        is_connected_lock.acquire()
        try:
            rates = Rates()
            connection = DBConnector("127.0.0.1", "mydb", "root", "")
            connection.connect()
            connection.update_prices(rates)
            success = True
        except:
            print("Updating prices as cyclic task FAILED")
            print("Retraing in 5 minutes")
            logger.error("Updating prices as cyclic task FAILED")
            logger.error("Retrying in 5 minutes")
        finally:
            if connection is not None:
                connection.close()
            is_connected_lock.release()
            if not success:
                sleep(60 * 5)
                continue
        logger.info("Sleeping 12 hours")
        sleep(3600 * 12)


def update_prices():
    connection = DBConnector("localhost", "mydb", "root", "")
    try:
        rates = Rates()
        connection.connect()
        connection.update_prices(rates)
    except ConnectionError:
        print("Updating failed")
    else:
        print("Updating successful")
    finally:
        connection.close()


def generate_excel():
    connection = DBConnector("localhost", "mydb", "root", "")
    try:
        connection.connect()
        connection.get_products()
    except ConnectionError:
        print("Creating Excel file failed")
    else:
        print("Creating Excel successful")
    finally:
        connection.close()


if __name__ == '__main__':
    path = "./logs"
    if not os.path.exists(path):
        os.makedirs("logs")
    logger = logging
    logger.basicConfig(filename="./logs/mainlog.log",
                       level=logging.INFO,
                       format="%(asctime)s | %(name)s | %(levelname)s  | %(message)s")

    is_connected_lock = threading.Lock()
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
        logger.info(f"Got '{user_input}' from user")
        match user_input.lower():
            case "u":
                is_connected_lock.acquire()
                logger.info("Trying to update prices on demand")
                update_prices()
                is_connected_lock.release()
            case "g":
                is_connected_lock.acquire()
                logger.info("Trying to create Excel on demand")
                generate_excel()
                is_connected_lock.release()
            case "q":
                logger.info("Closing app")
                SystemExit()
            case _:
                print("Wrong command.")
