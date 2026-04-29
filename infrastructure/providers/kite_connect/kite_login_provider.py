


# from domains.instruments.models import Instrument


class KiteLoginProvider:
    
    def __init__(self, kite_client):
        self.kite_client = kite_client

    def get_login_url(self):
        login_url = self.kite_client.login_url()
        return login_url





