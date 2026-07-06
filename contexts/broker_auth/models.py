

from pydantic import BaseModel, Field, computed_field, model_validator
from datetime import date, datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from utilities import utilities  

class Token(BaseModel):
    ist_expiry_dt: datetime = Field(
        description = "datetime values do not contain time-zone info"
    ) 
    request_token: str
    access_token: str
    updated_at_ts: datetime | None = Field(
        description = "timestamp values are always stored as UTC in big-query"
    ) 
    
