
from pydantic import BaseModel, computed_field, field_serializer, model_serializer, SerializationInfo
from datetime import datetime, date 
from zoneinfo import ZoneInfo


class Historical(BaseModel):

    instr_token : int  
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




    @model_serializer(mode="wrap")
    def _serialize(self, handler, info: SerializationInfo):
        data = handler(self)
        if info.context and info.context.get("include_only_table_columns"):
            for field_name in self.__class__.model_computed_fields:
                data.pop(field_name, None)
            
            data["created_at"] = data["updated_at"] = datetime.now(ZoneInfo("Asia/Kolkata"))

        return data

    



