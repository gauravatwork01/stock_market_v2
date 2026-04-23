
from functools import wraps
# from flask import request, jsonify, g, current_app
from utilities import utilities
from infrastructure.token_repository import DBTokenRepository
from infrastructure.api_clients.kite_connect_client import KiteConnectAPIClient
from flask import Blueprint, redirect, request, render_template 

def app_authentication_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        is_app_authenticated = False
        
        ist_now = utilities.get_ist_now_datetime()
        token_repo = DBTokenRepository()
        latest_token = token_repo.get_latest_token()
        ist_token_expiry = latest_token.ist_token_expiry
        if ist_token_expiry:
            if ist_token_expiry > ist_now:
                is_app_authenticated = True 
        

        if is_app_authenticated is False:
            return redirect("/auth/login")
        else:
            kc_api_client = KiteConnectAPIClient() 
            kc_api_client.token.attach_access_token(
                access_token = latest_token.access_token
            )
            

        return f(*args, **kwargs)

    return wrapper










