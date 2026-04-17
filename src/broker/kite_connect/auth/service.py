

from src.broker.kite_connect.client import KiteConnectClient
from src.broker.kite_connect.auth.repository import TokenRepository
from datetime import date

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

        



