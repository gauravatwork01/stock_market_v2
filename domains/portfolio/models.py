
from pydantic import BaseModel, Field, computed_field, ConfigDict

class Holding(BaseModel):
    model_config = ConfigDict(extra="allow")

    tradingsymbol: str
    quantity: int = Field(gt=0)
    average_price: float = Field(gt=0)
    last_price: float = Field(
        gt = 0,
        description = "Last traded market price of the instrument"
    )
    close_price: float = Field(
        gt = 0,
        description = "Closing price of the instrument from the last trading day"
    )

    @computed_field
    @property
    def total_invested(self) -> float:
        return self.quantity * self.average_price

    @computed_field
    @property
    def total_current_value(self) -> float:
        return self.quantity * self.last_price

    @computed_field
    @property
    def percent_chg(self) -> float:
        diff = (self.total_current_value - self.total_invested)/(self.total_invested)
        return round(diff*100, 2)

