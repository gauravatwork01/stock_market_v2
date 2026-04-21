

from pydantic import BaseModel, Field, computed_field
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo

class Token(BaseModel):
    token_date: date = Field(default_factory = date.today)
    access_token: str
    request_token: str
    utc_updated_at: datetime | None = Field(
        description = "datetime values are always stored as UTC in big-query"
    ) 
    utc_token_expiry: datetime | None = Field(
        description = "datetime values are always stored as UTC in big-query"
    )


    @computed_field
    @property
    def ist_token_expiry(self) -> datetime | None:
        if not self.utc_token_expiry:
            return None

        utc_token_expiry = self.utc_token_expiry
        ist_token_expiry = utc_token_expiry.astimezone(ZoneInfo("Asia/Kolkata"))
        return ist_token_expiry
