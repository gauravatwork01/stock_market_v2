
from .I_market_api_client import I_MarketApiClient
from kiteconnect import KiteConnect


API_KEY = "qjj8i06fi5r3s8ru"

class kc_api_client(I_MarketApiClient):

    def __init__(self) -> None:
        self.kc_client = KiteConnect(api_key = API_KEY)


    def set_access_token(self, access_token):
        self.kc_client.set_access_token(access_token)


    @property
    def access_token(self):
        return self.kc_client.access_token


    def holdings(self):
        return self.kc_client.holdings()
        

    def get_all_stocks():
        pass
    

    def generate_session(self, request_token):
        API_SECRET = "hxqjy14n6rvk6vkqcllefhlabkbv13yx"
        session_dets = self.kc_client.generate_session(request_token, api_secret=API_SECRET)
        return session_dets

    def login_url(self):
        return self.kc_client.login_url()


    def set_access_token(self,access_token):
        self.kc_client.set_access_token(access_token)






