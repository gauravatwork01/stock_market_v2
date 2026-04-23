


import logging
import os
from datetime import datetime, timezone
from kiteconnect import KiteConnect
from google.cloud import bigquery
from typing import List
from src.broker.kite_connect.auth.repository import TokenRepository
# from src.broker.kite_connect.auth.service import VendorAuthFlowService

logger = logging.getLogger(__name__)

API_KEY = "qjj8i06fi5r3s8ru"
API_SECRET = "hxqjy14n6rvk6vkqcllefhlabkbv13yx"


class KiteConnectAPIClient:

    def __init__(self):
        self.client = KiteConnect(api_key=API_KEY)

        # attach sub-APIs
        self.login = LoginAPI(self.client)
        self.token = TokenAPI(self.client)
        self.portfolio = PortfolioAPI(self.client)



class LoginAPI:
    def __init__(self, client):
        self.client = client

    def get_login_url(self):
        login_url = self.client.login_url()
        return login_url



class TokenAPI:

    def __init__(self, client):
        self.client = client
    
    def attach_access_token(self, access_token):
        self.client.set_access_token(access_token)
        print(f"access_token attatched : {self.client.access_token}")
    
    def fetch_access_token(self,request_token):
        session_dets = self.client.generate_session(request_token, api_secret=API_SECRET)
        return session_dets["access_token"]

    

class PortfolioAPI:

    def __init__(self, client):
        self.client = client

    def get_portfolio_holdings(self):
        holdings : List = self.client.holdings()
        return holdings




