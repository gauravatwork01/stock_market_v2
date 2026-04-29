


# from domains.instruments.models import Instrument


class KiteAuthProvider:
    
    def __init__(self, kite_client):
        self.kite_client = kite_client

    def get_login_url(self):
        login_url = self.kite_client.login_url()
        return login_url

    def attach_access_token(self, access_token):
        self.kite_client.set_access_token(access_token)
        print(f"access_token attatched : {self.client.access_token}")
    
    def fetch_access_token(self,request_token, API_SECRET):
        session_dets = self.kite_client.generate_session(request_token, api_secret=API_SECRET)
        return session_dets["access_token"]





