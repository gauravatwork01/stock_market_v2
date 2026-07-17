
from contexts.broker_auth.infrastructure.providers.kite_auth_provider import KiteAuthProvider
from shared.infrastructure import kc_api_client
from contexts.broker_auth.infrastructure.repositories.bigquery_token_repository import BigQueryTokenRepository
from shared.infrastructure import BigQueryClient
from contexts.broker_auth.application.use_cases.kite_auth_use_case import KiteAuthUseCase
from flask import Blueprint, redirect, request, render_template 
from functools import wraps




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





