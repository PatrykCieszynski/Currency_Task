import logging
from decimal import *
import requests

logger = logging.getLogger(__name__)


class Rates:
    def __init__(self):
        self.USD = None
        self.EUR = None
        self.update_rates()

    def set_usd_rate(self):
        logger.info("Getting USD rate from NBP")
        usd_url = "https://api.nbp.pl/api/exchangerates/rates/A/USD"
        self.USD = Decimal(requests.get(usd_url).json()["rates"][0]["mid"])
        logger.info("USD rate successfully set")

    def set_eur_rate(self):
        logger.info("Getting EUR rate from NBP")
        eur_url = "https://api.nbp.pl/api/exchangerates/rates/A/EUR"
        self.EUR = Decimal(requests.get(eur_url).json()["rates"][0]["mid"])
        logger.info("EUR rate successfully set")

    def update_rates(self):
        try:
            self.set_usd_rate()
            self.set_eur_rate()
        except requests.exceptions.RequestException as err:
            logger.error(err)
            print("Could not get rates from NBP")
            raise ConnectionError(err)
