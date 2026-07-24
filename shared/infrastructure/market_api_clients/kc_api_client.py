
from .I_market_api_client import I_MarketApiClient
from kiteconnect import KiteConnect
from datetime import datetime

API_KEY = "qjj8i06fi5r3s8ru"

class kc_api_client(I_MarketApiClient):

    def __init__(self) -> None:
        self.kc_client = KiteConnect(api_key = API_KEY)


    def set_access_token(self, access_token):
        self.kc_client.set_access_token(access_token)


    @property
    def access_token(self):
        return self.kc_client.access_token

    @property
    def api_key(self):
        return API_KEY


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



    def get_instruments_by_exchange(self, exchange = "all"):
        if exchange == "all":
            exch_val = None 
        else:
            exch_val = exchange 
        instruments = self.kc_client.instruments(exchange = exch_val)

        formatted_instrs = []
        for each_instr in instruments:
            if each_instr["segment"] == "INDICES":
                continue
            else:
                f_instr = {}
                f_instr["instr_token"] = each_instr["instrument_token"]
                f_instr["exchange"] = each_instr["exchange"]
                f_instr["symbol"] = each_instr["tradingsymbol"]
                f_instr["name"] = each_instr["name"]
                formatted_instrs.append(f_instr)

        return formatted_instrs



    def get_historicals(self,instr_token, st_dt:datetime, end_dt: datetime, interval):
        allowed_intervals = ["minute", "day", "3minute", "5minute", "10minute"]
        if interval not in allowed_intervals:
            raise ValueError(f"invalid interval provided : {interval}")
        
        historicals = self.kc_client.historical_data(
            instr_token,
            st_dt,
            end_dt,
            interval
        )

        f_instruments = []
        for each_hist in historicals:
            data = {
                "open": each_hist["open"],
                "high": each_hist["high"],
                "low": each_hist["low"],
                "close": each_hist["close"],
                "date_time": each_hist["date"]
            }
            f_instruments.append(data)

        return f_instruments



    def get_ohlc(self, instr_ids):

        data = self.kc_client.ohlc(instr_ids)
        pass 
