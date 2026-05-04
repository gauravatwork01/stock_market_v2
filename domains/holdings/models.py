
from pydantic import BaseModel, Field, computed_field, ConfigDict
from pydantic import BaseModel
from typing import List


class Holding(BaseModel):
    symbol: str
    quantity: int
    avg_acquisition_price: float

    recent_trade_price: float = Field(
        gt = 0,
        description = "The most recent traded price, Changes continuously during market hours"
    )
    yesterdays_close_price: float = Field(
        gt = 0,
        description = "Yesterday's closing price, doesn’t change during the current trading day "
    )

    @computed_field
    @property
    def total_invested(self) -> float:
        total_invested = self.quantity * self.avg_acquisition_price
        total_invested = round(total_invested, 2)
        return total_invested

    @computed_field
    @property
    def total_current_value(self) -> float:
        total_current_value = self.quantity * self.recent_trade_price
        total_current_value = round(total_current_value, 2)
        return total_current_value

    @computed_field
    @property
    def percent_chg(self) -> float:
        diff = (self.total_current_value - self.total_invested)/(self.total_invested)
        diff = round(diff*100, 2)
        return diff 






