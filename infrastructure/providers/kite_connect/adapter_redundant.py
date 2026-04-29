
# Role: Converts the "Kite language" into "Your language."

import logging
import os
from datetime import datetime, timezone
from kiteconnect import KiteConnect
from google.cloud import bigquery
from typing import List
from infrastructure.providers.kite_connect import API_SECRET

logger = logging.getLogger(__name__)


# kc_client = KiteConnect(api_key=API_KEY)
class KiteConnectAdapter:

    def __init__(self, api_key):
        self.client = KiteConnect(api_key=api_key)

        # attach sub-APIs
        self.login = LoginAdapter(self.client)
        self.token = TokenAdapter(self.client)
        self.portfolio = PortfolioAdapter(self.client)
        self.instruments = InstrumentsAdapter(self.client)

class InstrumentsAdapter:
    def __init__(self, client) -> None:
        self.client = client

    def get_all_stocks(self):
        data = self.client.instruments(exchange = None)   
        return data 


class LoginAdapter:
    def __init__(self, client):
        self.client = client

    def get_login_url(self):
        login_url = self.client.login_url()
        return login_url



class TokenAdapter:

    def __init__(self, client):
        self.client = client
    
    def attach_access_token(self, access_token):
        self.client.set_access_token(access_token)
        print(f"access_token attatched : {self.client.access_token}")
    
    def fetch_access_token(self,request_token):
        session_dets = self.client.generate_session(request_token, api_secret=API_SECRET)
        return session_dets["access_token"]

    

class PortfolioAdapter:

    def __init__(self, client):
        self.client = client

    def get_portfolio_holdings(self):
        holdings : List = self.client.holdings()
        return holdings




