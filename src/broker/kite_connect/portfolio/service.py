

from src.broker.kite_connect.client import VendorAPIClient
from typing import List 
import polars as pl 
from src.broker.kite_connect.portfolio.models import Holding

class PortfolioService:


    def get_holdings():
        holdings:List = VendorAPIClient.get_portfolio_holdings()

        holding_models = []
        for each_holding in holdings:
            each_holding_model = Holding(**each_holding)
            holding_models.append(each_holding_model)


        holdings_df = pl.DataFrame(holdings)


        pass 








