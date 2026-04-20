

from src.broker.kite_connect.client import VendorAPIClient
from src.broker.kite_connect.auth.repository import TokenRepository
from datetime import date, datetime, timedelta
from utilities import utilities
from zoneinfo import ZoneInfo
from typing import List
class VendorAPIClientService:

    @staticmethod
    def get_login_url():
        login_url = VendorAPIClient.get_login_url()
        return login_url

    @staticmethod
    def get_access_token(request_token):
        access_token = VendorAPIClient.get_access_token(request_token= request_token)
        return access_token

    @staticmethod
    def attach_access_token(access_token):
        VendorAPIClient.attach_access_token(access_token= access_token)

    @staticmethod
    def attach_access_token_from_db():
        token_repo = TokenRepository()
        ist_now = utilities.get_ist_datetime()
        token_repo.token_exists_for_date(
            target_date= ist_now.date()
        )




class VendorAuthFlowService:

    @staticmethod
    def save_token(token_date:date,request_token, access_token):
        token_repo = TokenRepository()
        token_repo.create_update_token(
            request_token= request_token,
            access_token= access_token,
            target_date= token_date
        )

    @staticmethod 
    def is_online():
        is_online = False
        ist_now = utilities.get_ist_datetime()
        token_repo = TokenRepository()
        existing_token = token_repo.token_exists_for_date(
            target_date= ist_now.date()
        )
        if existing_token:
            updated_at_utc = existing_token.updated_at
            updated_at_ist = updated_at_utc.astimezone(ZoneInfo("Asia/Kolkata"))
            if updated_at_ist >= ist_now.replace(hour=6, minute=1, second=1):
                is_online = True
        
        return is_online, existing_token




class TokenPolicy:

    @staticmethod
    def get_token_expiry(ist_dt : datetime):    
        ist_hour = ist_dt.hour 
        if ist_hour >= 6 and ist_hour <= 24:
            token_expiry_datetime = ist_dt + timedelta(days= 1)
            token_expiry_datetime = token_expiry_datetime.replace(hour=6, minute=0, second=0) 
        elif ist_hour < 6:
            token_expiry_datetime = ist_dt.replace(hour=6, minute=0, second=0)

        return token_expiry_datetime


class TokenService:

    @staticmethod
    def create_token():
        token_repo = TokenRepository()
        token_repo.create_token_for_date
        pass 

    @staticmethod
    def save_token(token_date:date,request_token, access_token):
        token_repo = TokenRepository()
        token_repo.create_update_token(
            request_token= request_token,
            access_token= access_token,
            target_date= token_date
        )

    def get_token():

        ist_now = utilities.get_ist_datetime()
        curr_date = ist_now.date()

        if curr_date.hour < 6:
            valid_token_date = curr_date - timedelta(days= 1)
        else:
            valid_token_date = curr_date

        token_repo = TokenRepository()
        existing_token = token_repo.get_token_for_date(
            target_date= valid_token_date
        )

        return valid_token_date 

