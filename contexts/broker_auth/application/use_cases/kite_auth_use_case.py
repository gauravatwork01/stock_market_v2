from utilities import utilities

from contexts.broker_auth.infrastructure.providers.kite_auth_provider import KiteAuthProvider

from contexts.broker_auth.infrastructure.repositories.bigquery_token_repository import BigQueryTokenRepository
# from domains.broker_auth.models import Token
from contexts.broker_auth.models import Token
from datetime import date, datetime, timezone, timedelta

class TokenPolicy:

    @staticmethod
    def get_applicable_token_expiry(ist_dt: datetime):
        ist_hour = ist_dt.hour 
        if ist_hour >= 6 and ist_hour <= 24:
            ist_token_expiry = ist_dt + timedelta(days = 1)
            ist_token_expiry = ist_token_expiry.replace(hour = 6, minute=0, second=0) 
        elif ist_hour < 6:
            ist_token_expiry = ist_dt.replace(hour = 6, minute=0, second=0)
        return ist_token_expiry  








class KiteAuthUseCase:

    def __init__(self,kite_auth_provider: KiteAuthProvider, token_repo: BigQueryTokenRepository) -> None:
        self.kite_auth_provider = kite_auth_provider
        self.token_repo = token_repo

    def get_login_url(self):
        login_url = self.kite_auth_provider.get_login_url()
        return login_url 

    def fetch_and_save_access_token(self, request_token):
        access_token = self.kite_auth_provider.fetch_access_token(
            request_token = request_token
        )
        ist_dt = utilities.get_ist_now_datetime()
        applicable_ist_token_expiry = TokenPolicy.get_applicable_token_expiry(
            ist_dt= ist_dt
        )
        token = self.token_repo.get_token_by_expiry_datetime(
            ist_datetime = applicable_ist_token_expiry
        )
        
        if token:
            token.access_token = access_token
            token.request_token = request_token
            self.token_repo.update_token(
                token = token
            )
        else:
            token = Token(
                ist_expiry_dt = applicable_ist_token_expiry,
                request_token = request_token,
                access_token = access_token,
                updated_at_ts = datetime.now()
            )
            self.token_repo.create_token(
                token= token 
            )
            

    def is_app_authenticated(self):

        curr_ist_dt = utilities.get_ist_now_datetime()
        applicable_ist_token_expiry = TokenPolicy.get_applicable_token_expiry(
            ist_dt= curr_ist_dt
        )
        token = self.token_repo.get_token_by_expiry_datetime(
            ist_datetime = applicable_ist_token_expiry
        )
        
        is_app_authenticated = False 
        if token:
            if curr_ist_dt < token.ist_expiry_dt:
                is_app_authenticated = True 

        return is_app_authenticated, token 





















