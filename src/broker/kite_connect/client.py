

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


class VendorAPIClient:

    client = KiteConnect(api_key = API_KEY )

    # def __init__(self) -> None:
    #     token_repo = TokenRepository()
    #     existing_token = token_repo.get_todays_token()
    #     if 
        
    #     pass

    @classmethod
    def attach_access_token(cls, access_token):
        cls.client.set_access_token(access_token)
        print(f"access_token attatched : {cls.client.access_token}")

    @classmethod
    def get_login_url(cls):
        login_url = cls.client.login_url()
        return login_url

    @classmethod
    def get_access_token(cls,request_token):
        access_token = cls.client.generate_session(request_token, api_secret=API_SECRET)
        return access_token


    # @classmethod
    # def attach_access_token_from_db(cls):
    #     token_repo = TokenRepository()
    #     existing_token = token_repo.get_token_by_date(
    #         target_date= 
    #     )
    #     if existing_token:
    #         cls.client.set_access_token(existing_token.access_token)
    #         print(f"access_token attatched from db : {cls.client.access_token}")
    #     else:
    #         raise RuntimeError("access token is not available in db, login-again")


    @classmethod
    def get_portfolio_holdings(cls):
        # if cls.client.access_token is None:
        #     cls.attach_access_token_from_db()
        holdings : List = cls.client.holdings()
        return holdings

        # holdings_resp = []
        # count = 0 
        # for each_holding in holdings:
        #     count += 1 
        #     holdings_resp.append({
        #         "sr_num" : count,
        #         "stock" : each_holding["tradingsymbol"],
        #         "quantity" : each_holding["quantity"],
        #         "buying_avg_price" : each_holding["average_price"],
        #         "last_price_in_market" : each_holding["last_price"],
        #     })

        # return holdings_resp


# vendor_api_client = VendorAPIClient()


