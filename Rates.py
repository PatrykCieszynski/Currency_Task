from decimal import *
import requests


class Rates:
    def __init__(self):
        self.USD = None
        self.EUR = None
        self.update_rates()

    def set_usd_rate(self):
        usd_url = "https://api.nbp.pl/api/exchangerates/rates/A/USD"
        self.USD = Decimal(requests.get(usd_url).json()["rates"][0]["mid"])

    def set_eur_rate(self):
        eur_url = "https://api.nbp.pl/api/exchangerates/rates/A/EUR"
        self.EUR = Decimal(requests.get(eur_url).json()["rates"][0]["mid"])

    def update_rates(self):
        try:
            self.set_usd_rate()
            self.set_eur_rate()
        except requests.exceptions.RequestException as err:
            print("Could not get rates from NBP")
            raise SystemExit(err)
