import json
import requests
from config import keys

class APIException(Exception):
    pass

class CurrencyConvert:
    @staticmethod
    def get_price(base: str, quote: str, amount: float):
        if quote == base:
            raise APIException(f"Невозможно перевести одинаковые валюты {base}")

        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}")

        try:
            base_ticket = keys[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticket}&tsyms={base_ticket}")
        total_base = json.loads(r.content)[keys[base]]
        return total_base
