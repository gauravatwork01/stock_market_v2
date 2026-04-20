

from pydantic import BaseModel, Field
from datetime import date, datetime, timezone


class Token(BaseModel):
    token_date: date = Field(default_factory = date.today)
    access_token: str
    request_token: str
    updated_at: datetime | None = None 
    token_expiry: datetime | None = None 




