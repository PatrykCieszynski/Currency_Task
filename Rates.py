import requests
from decimal import *
import logging

logger = logging.getLogger(__name__)


class Rates:
    def __init__(self, usd_rul, eur_rul):
        self.USD = None
        self.EUR = None
        self.update_rates(usd_rul, eur_rul)

    @staticmethod
    def request_usd(usd_url):
        logger.info("Getting USD rate from NBP")
        return requests.get(usd_url).json()["rates"][0]["mid"]

    @staticmethod
    def request_eur(eur_url):
        logger.info("Getting EUR rate from NBP")
        return requests.get(eur_url).json()["rates"][0]["mid"]

    def set_usd_rate(self, usd_url):
        self.USD = Decimal(self.request_usd(usd_url))
        logger.info("USD rate successfully set")

    def set_eur_rate(self, eur_url):
        self.EUR = Decimal(self.request_eur(eur_url))
        logger.info("EUR rate successfully set")

    def update_rates(self, usd_rul, eur_rul):
        try:
            self.set_usd_rate(usd_rul)
            self.set_eur_rate(eur_rul)
        except requests.exceptions.RequestException as err:
            logger.error(err)
            raise ConnectionError()
