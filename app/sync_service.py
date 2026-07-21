
from shared.infrastructure import get_kc_api_client
from contexts.broker_auth.application.services import get_access_token
from datetime import datetime
from zoneinfo import ZoneInfo

class HistoricalsSyncAppService:




    def sync_historicals():
        kc_api_client = get_kc_api_client()
        access_token = get_access_token()
        kc_api_client.set_access_token(access_token)

        st_dt = datetime(2026, 7, 1, 9, 15, 0, tzinfo=ZoneInfo("Asia/Kolkata"))
        end_dt = datetime(2026, 7, 1, 15, 15, 0, tzinfo=ZoneInfo("Asia/Kolkata"))
        kc_api_client.get_historicals(
            id = 738561,
            st_dt = st_dt,
            end_dt = end_dt,
            interval = "5minute"
        )
        pass 




