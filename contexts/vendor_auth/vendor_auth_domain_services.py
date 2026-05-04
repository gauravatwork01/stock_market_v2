

# from src.broker.kite_connect.client import VendorAPIClient
# from src.broker.kite_connect.auth.repository import TokenRepository
from infrastructure.repositories.token_repository import DBTokenRepository
from datetime import date, datetime, timedelta
from utilities import utilities
from zoneinfo import ZoneInfo
from typing import List
from domains.vendor_auth.models import Token

class VendorAuthDomainService:

    @staticmethod
    def create_update_token(request_token, access_token):
        ist_now_dt = utilities.get_ist_now_datetime()
        applicable_token_expiry_dt = TokenPolicy.get_applicable_ist_token_expiry(
            ist_dt= ist_now_dt
        )

        token_repo = DBTokenRepository()
        applicable_token = token_repo.get_token_by_date(
            utc_target_date= applicable_token_expiry_dt.date()
        )
        if applicable_token:
            # update token
            utc_updated_at = utilities.get_utc_now_datetime()
            token = Token(
                token_date = applicable_token_expiry_dt.date(),
                access_token = access_token,
                request_token = request_token,
                utc_updated_at = utc_updated_at,
                utc_token_expiry = applicable_token_expiry_dt
            )
            token_repo.update_token(
                token= token
            )
        else:
            # create token
            utc_updated_at = utilities.get_utc_now_datetime()
            token = Token(
                token_date = applicable_token_expiry_dt.date(),
                access_token = access_token,
                request_token = request_token,
                utc_updated_at = utc_updated_at,
                utc_token_expiry = applicable_token_expiry_dt
            )
            token_repo.create_token(
                token= token
            )
            

    




class TokenPolicy:

    @staticmethod
    def get_applicable_ist_token_expiry(ist_dt : datetime)->datetime:    
        ist_hour = ist_dt.hour 
        if ist_hour >= 6 and ist_hour <= 24:
            token_expiry_datetime = ist_dt + timedelta(days= 1)
            token_expiry_datetime = token_expiry_datetime.replace(hour=6, minute=0, second=0) 
        elif ist_hour < 6:
            token_expiry_datetime = ist_dt.replace(hour=6, minute=0, second=0)

        return token_expiry_datetime



