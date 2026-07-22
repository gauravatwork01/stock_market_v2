
from pydantic import BaseModel, computed_field, field_serializer
from datetime import datetime
from zoneinfo import ZoneInfo


class Historical(BaseModel):

    symbol: str 
    open: float
    high: float
    low: float
    close: float
    interval: str 
    datetime: datetime

    @field_serializer("datetime")
    def serialize_datetime(self, dt: datetime) -> str:
        return (
            dt.astimezone(ZoneInfo("Asia/Kolkata"))
            .replace(tzinfo=None)
            .isoformat(sep=" ")
        )

    @computed_field
    @property
    def pct_change(self) -> float:
        if self.open == 0:
            return 0.0
        return ((self.close - self.open) / self.open) * 100


