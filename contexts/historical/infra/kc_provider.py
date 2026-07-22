from contexts.broker_auth.application.services import get_access_token
from shared.infrastructure import get_kc_api_client
from ..models import Historical

class KiteConnectProvider():

    def fetch_historicals(self, instr_token, st_dt, end_dt, interval):
        kc_api_client = get_kc_api_client()
        access_token = get_access_token()
        kc_api_client.set_access_token(access_token)
        historicals = kc_api_client.get_historicals(
            instr_token= instr_token,
            st_dt= st_dt,
            end_dt= end_dt,
            interval= interval
        ) 

        hist_models = []
        for each_hist in historicals:
            hist_model = Historical(
                symbol= str(instr_token),
                open = each_hist["open"],
                high = each_hist["high"],
                low = each_hist["low"],
                close = each_hist["close"],
                interval = interval,
                datetime = each_hist["date_time"]
            )
            hist_models.append(hist_model)

        return hist_models

