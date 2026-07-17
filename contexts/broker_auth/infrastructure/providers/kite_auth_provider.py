

from shared.infrastructure import kc_api_client


class KiteAuthProvider:
    
    def __init__(self, kite_client: kc_api_client):
        self.kite_client = kite_client

    def get_login_url(self):
        login_url = self.kite_client.login_url()
        return login_url

    def attach_access_token(self, access_token):
        self.kite_client.set_access_token(access_token)
        print(f"access_token attatched : {self.kite_client.access_token}")
    
    def fetch_access_token(self,request_token):
        session_dets = self.kite_client.generate_session(request_token)
        return session_dets["access_token"]





