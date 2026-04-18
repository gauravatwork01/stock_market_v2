

from src.broker.kite_connect.client import KiteConnectClient
from src.broker.kite_connect.auth.repository import TokenRepository
from datetime import date, datetime
from utilities import utilities
from zoneinfo import ZoneInfo
class KiteConnectService:

    @staticmethod
    def get_login_url():
        login_url = KiteConnectClient.get_login_url()
        return login_url

    @staticmethod
    def get_access_token(request_token):
        access_token = KiteConnectClient.get_access_token(request_token= request_token)
        return access_token




class VendorAuthService:

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
        
        return is_online


