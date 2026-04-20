

from pydantic import BaseModel, Field, computed_field
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

class Token(BaseModel):
    token_date: date = Field(default_factory = date.today)
    access_token: str
    request_token: str
    updated_at: datetime | None = None 
    token_expiry: datetime | None = None 


    @computed_field
    @property
    def ist_token_expiry(self) -> datetime | None:
        if not self.token_expiry:
            return None

        utc_token_expiry = self.token_expiry
        ist_token_expiry = utc_token_expiry.astimezone(ZoneInfo("Asia/Kolkata"))
        return ist_token_expiry
