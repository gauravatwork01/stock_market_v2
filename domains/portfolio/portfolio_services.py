

from src.broker.kite_connect.client import VendorAPIClient
from typing import List 
import polars as pl 
# from src.broker.kite_connect.portfolio.models import Holding
from domains.portfolio.models import Holding
from src.broker.kite_connect.auth.repository import TokenRepository
# from src.broker.kite_connect.auth.service import TokenPolicy
from domains.vendor_auth.auth_services import TokenPolicy
from utilities import utilities
from datetime import datetime, timezone

class PortfolioService:


    def get_holdings():

        if VendorAPIClient.client.access_token is None:
            applicable_ist_token_expiry = TokenPolicy.get_applicable_ist_token_expiry(
                ist_dt= utilities.get_ist_now_datetime()
            )
            token_repo = TokenRepository()
            token_dets = token_repo.get_token_by_date(
                utc_target_date= applicable_ist_token_expiry.astimezone(timezone.utc).date()
            )
            VendorAPIClient.attach_access_token(
                access_token= token_dets.access_token
            )

        holdings:List = VendorAPIClient.get_portfolio_holdings()

        holding_models = []
        for each_holding in holdings:
            each_holding_model = Holding(**each_holding)
            holding_models.append(each_holding_model)

        return holding_models
        # holdings_df = pl.DataFrame(holdings)


        # pass 








