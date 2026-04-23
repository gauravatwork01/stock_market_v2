
from infrastructure.api_clients.kite_connect_client import KiteConnectAPIClient
from domains.vendor_auth.vendor_auth_domain_services import VendorAuthDomainService
from utilities import utilities
from infrastructure.token_repository import DBTokenRepository

class VendorAuthApplicationService:

    @staticmethod
    def get_vendor_login_url():
        kc_api_client = KiteConnectAPIClient()
        vendor_login_url = kc_api_client.login.get_login_url()
        return vendor_login_url
     

    @staticmethod
    def fetch_and_store_access_token(request_token):
        kc_api_client = KiteConnectAPIClient()
        access_token = kc_api_client.token.fetch_access_token(
            request_token= request_token
        )
        kc_api_client.token.attach_access_token(
            access_token= access_token
        )
        VendorAuthDomainService.create_update_token(
            request_token = request_token,
            access_token = access_token
        )



    @staticmethod 
    def is_app_authenticated():
        is_app_authenticated = False
        
        ist_now = utilities.get_ist_now_datetime()
        token_repo = DBTokenRepository()
        latest_token = token_repo.get_latest_token()
        ist_token_expiry = latest_token.ist_token_expiry
        if ist_token_expiry:
            if ist_token_expiry > ist_now:
                is_app_authenticated = True 
        
        return is_app_authenticated#, latest_token







