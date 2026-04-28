

from typing import List 
import polars as pl 
from domains.portfolio.models import Holding

from utilities import utilities
from datetime import datetime, timezone
import polars as pl

class PortfolioDomainService:

    def compute_portfolio_metrics(holdings: list[dict]):
        polars_df = pl.DataFrame(holdings)
        polars_df = polars_df.with_columns(
            (pl.col("quantity") * pl.col("average_price")).round(2).alias("total_invested")
        )
        polars_df = polars_df.with_columns(
            (pl.col("quantity") * pl.col("last_price")).round(2).alias("total_current_value")
        )
        polars_df = polars_df.with_columns(
            (
                ((pl.col("total_current_value") - pl.col("total_invested")) / pl.col("total_invested"))*100
            ).round(2).alias("percent_chg")
        )
        return polars_df.to_dicts() 
     

