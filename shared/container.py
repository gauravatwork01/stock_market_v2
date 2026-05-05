

# API_SECRET = "hxqjy14n6rvk6vkqcllefhlabkbv13yx"
from google.cloud import bigquery
from kiteconnect import KiteConnect
# kc_client = KiteConnect(api_key=API_KEY)



class Container:

    def __init__(self):
        self._singletons = {}

    # ---------- CLIENTS (Singletons) ----------
    def kite_client(self):
        if "kite" not in self._singletons:
            API_KEY = "qjj8i06fi5r3s8ru"
            self._singletons["kite"] = KiteConnect(api_key= API_KEY)
        return self._singletons["kite"]

    def bigquery_client(self):
        if "bq" not in self._singletons:
            self._singletons["bq"] = bigquery.Client()
        return self._singletons["bq"]

    # ---------- MARKET DATA ----------
    def market_data_provider(self):
        return KiteMarketDataProvider(self.kite_client())






