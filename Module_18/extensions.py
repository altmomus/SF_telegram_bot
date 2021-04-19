import requests
import json


class RequestsToApi:
    data_from_api = requests.get("https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=RUB,USD,EUR")
    json_data_values = json.loads(data_from_api.text)

    def get_amount_values(self):
        rub_to_usd = int(self.json_data_values["RUB"]) / int(self.json_data_values["USD"])
        rub_to_eur = int(self.json_data_values["RUB"]) / int(self.json_data_values["EUR"])
        return rub_to_usd, rub_to_eur

    def get_price(self, base, quote, amount):
        convert = (int(self.json_data_values[quote]) / int(self.json_data_values[base])) * int(amount)
        return convert
      
