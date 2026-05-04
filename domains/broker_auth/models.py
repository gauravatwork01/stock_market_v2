

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
    


    # @model_validator(mode="after")
    # def set_utc_token_expiry(self):
    #     ist_now_dt = utilities.get_ist_now_datetime()
    #     ist_hour = ist_now_dt.hour 
    #     if ist_hour >= 6 and ist_hour <= 24:
    #         ist_token_expiry = ist_now_dt + timedelta(days = 1)
    #         ist_token_expiry = ist_token_expiry.replace(hour = 6, minute=0, second=0) 
    #     elif ist_hour < 6:
    #         ist_token_expiry = ist_now_dt.replace(hour = 6, minute=0, second=0)

    #     self.utc_token_expiry = utilities.convert_ist_to_utc(ist_dt= ist_token_expiry)
    #     return self


    # @model_validator(mode="after")
    # def set_utc_updated_at(self):
    #     ist_now_dt = utilities.get_ist_now_datetime()
    #     self.utc_updated_at = utilities.convert_ist_to_utc(ist_dt= ist_now_dt)
    #     return self


    # @computed_field
    # @property
    # def ist_token_expiry(self) -> datetime | None:
    #     if not self.utc_token_expiry:
    #         return None

    #     utc_token_expiry = self.utc_token_expiry
    #     ist_token_expiry = utc_token_expiry.astimezone(ZoneInfo("Asia/Kolkata"))
    #     return ist_token_expiry
