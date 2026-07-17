
from contexts.holdings.application.use_cases.get_holdings_use_case import GetHoldingsUseCase
from contexts.holdings.infrastructure.repositories.bigquery_holdings_repository import BigQueryHoldingsRepository
from contexts.holdings.models import Holding
from contexts.holdings.infrastructure.providers.kite_holdings_provider import KiteHoldingsProvider
# from infrastructure.providers.kite_connect.kite_login_provider import KiteLoginProvider
from contexts.broker_auth.application.use_cases.kite_auth_use_case import KiteAuthUseCase

from contexts.broker_auth.infrastructure.providers.kite_auth_provider import KiteAuthProvider
from google.cloud import bigquery
from functools import wraps
from kiteconnect import KiteConnect
from utilities import utilities
from flask import Blueprint, redirect, request, render_template 
from contexts.broker_auth.infrastructure.repositories.bigquery_token_repository import BigQueryTokenRepository
from shared.infrastructure import BigQueryClient
from shared.infrastructure import kc_api_client


bigquery_client = bigquery.Client()
API_SECRET = "hxqjy14n6rvk6vkqcllefhlabkbv13yx"

def app_authentication_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        kite_auth_provider = KiteAuthProvider(
            kite_client = kc_api_client() 
        )
        bigquery_token_repo = BigQueryTokenRepository(
            bigquery_client= BigQueryClient()
        )
        kite_auth_service = KiteAuthUseCase(
            kite_auth_provider = kite_auth_provider,
            token_repo = bigquery_token_repo
        )
        is_app_authenticated, token = kite_auth_service.is_app_authenticated()

        if is_app_authenticated is False:
            return redirect("/auth/login")
        else:
            kite_auth_provider = KiteAuthProvider(
                kite_client= kc_api_client()
            )
            kite_auth_provider.attach_access_token(
                access_token = token.access_token
            )
            
        return f(*args, **kwargs)

    return wrapper


def kite_authentication_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        
        kite_auth_provider = KiteAuthProvider(
            kite_client = kc_api_client() 
        )
        bigquery_token_repo = BigQueryTokenRepository(
            bigquery_client= BigQueryClient()
        )
        kite_auth_service = KiteAuthUseCase(
            kite_auth_provider = kite_auth_provider,
            token_repo = bigquery_token_repo
        )
        is_app_authenticated, token = kite_auth_service.is_app_authenticated()

        if is_app_authenticated is False:
            return redirect("/auth/login")
        else:
            kite_auth_provider = KiteAuthProvider(
                kite_client= kc_api_client()
            )
            kite_auth_provider.attach_access_token(
                access_token = token.access_token
            )
            
        return f(*args, **kwargs)

    return wrapper


def get_holdings():
    bq_holdings_repo = BigQueryHoldingsRepository(
        bigquery_client = BigQueryClient()
    )
    kite_holdings_provider = KiteHoldingsProvider(
        kite_client = kc_api_client()
    )
    holdings = GetHoldingsUseCase(
        holdings_repo = bq_holdings_repo,
        kite_provider = kite_holdings_provider
    ).get_holdings()

    return holdings 




def get_kite_login_url():
    kite_auth_provider = KiteAuthProvider(
        kite_client = kc_api_client() 
    )
    bigquery_token_repo = BigQueryTokenRepository(
        bigquery_client= BigQueryClient()
    )
    kite_auth_service = KiteAuthUseCase(
        kite_auth_provider = kite_auth_provider,
        token_repo = bigquery_token_repo
    )
    login_url = kite_auth_service.get_login_url()
    return login_url


def fetch_and_store_token(request_token):
    kite_auth_provider = KiteAuthProvider(
        kite_client = kc_api_client() 
    )
    bigquery_token_repo = BigQueryTokenRepository(
        bigquery_client= BigQueryClient()
    )
    kite_auth_service = KiteAuthUseCase(
        kite_auth_provider = kite_auth_provider,
        token_repo = bigquery_token_repo
    )

    kite_auth_service.fetch_and_save_access_token(request_token)



from contexts.instrument.application.services.instrument_service import InstrumentService
from contexts.instrument.infrastructure.providers.kite_instrument_provider import KiteInstrumentProvider
from contexts.instrument.infrastructure.providers.finedge_instrument_provider import FinEdgeInstrumentProvider

def get_instruments():


    kite_instrument_provider = KiteInstrumentProvider(
        kite_client= kc_api_client()
    )
    # finedge_instrument_provider = FinEdgeInstrumentProvider(
    #     finedge_client= 
    # )
    pass 