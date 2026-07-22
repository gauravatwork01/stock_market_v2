from contexts.broker_auth.application.services import get_access_token
from shared.infrastructure import get_kc_api_client
from datetime import datetime
from zoneinfo import ZoneInfo
from ..infra.kc_provider import KiteConnectProvider


def get_historicals(
    instr_token, from_dt: datetime, to_dt: datetime, interval: str
):
    kc_api_client = get_kc_api_client()
    access_token = get_access_token()
    kc_api_client.set_access_token(access_token)

    kc_provider = KiteConnectProvider()
    hists = kc_provider.fetch_historicals(
        instr_token=instr_token, st_dt=from_dt, end_dt=to_dt, interval=interval
    )
    return hists
