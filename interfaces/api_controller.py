from application.use_cases.get_holdings_use_case import GetHoldingsUseCase
from infrastructure.repositories.bigquery_holdings_repository import BigQueryHoldingsRepository
from domains.holdings.models import Holding
from infrastructure.providers.kite_connect.kite_holdings_provider import KiteHoldingsProvider
from infrastructure.providers.kite_connect.kite_login_provider import KiteLoginProvider
from google.cloud import bigquery
from functools import wraps
from kiteconnect import KiteConnect
from utilities import utilities
from flask import Blueprint, redirect, request, render_template 
from infrastructure.repositories.bigquery_token_repository import BigQueryTokenRepository

bigquery_client = bigquery.Client()
API_KEY = "qjj8i06fi5r3s8ru"
kc_client = KiteConnect(api_key=API_KEY)
API_SECRET = "hxqjy14n6rvk6vkqcllefhlabkbv13yx"

def app_authentication_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        global bigquery_client

        is_app_authenticated = False
        
        ist_now = utilities.get_ist_now_datetime()
        token_table_path = f"{bigquery_client.project}.datawarehouse.tokens"
        token_repo = BigQueryTokenRepository(
            bigquery_client= bigquery_client,
            token_table_path= token_table_path
        )
        latest_token = token_repo.get_latest_token()
        ist_token_expiry = latest_token.ist_token_expiry
        if ist_token_expiry:
            if ist_token_expiry > ist_now:
                is_app_authenticated = True 
        

        if is_app_authenticated is False:
            return redirect("/auth/login")
        else:
            # kc_api_client = KiteConnectAPIClient() 
            kc_client.token.attach_access_token(
                access_token = latest_token.access_token
            )
            

        return f(*args, **kwargs)

    return wrapper


def get_holdings():
    global bigquery_client
    bq_holdings_repo = BigQueryHoldingsRepository(
        bigquery_client = bigquery_client
    )
    kite_holdings_provider = KiteHoldingsProvider(
        kite_client = kc_client
    )
    holdings = GetHoldingsUseCase(
        holdings_repo = bq_holdings_repo,
        kite_provider = kite_holdings_provider
    ).get_holdings()

    return holdings 




def get_kite_login_url():
    login_url = KiteLoginProvider(
        kite_client= kc_client
    ).get_login_url()
    return login_url