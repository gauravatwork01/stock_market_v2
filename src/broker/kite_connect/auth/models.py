

from pydantic import BaseModel, Field
from datetime import date


class Token(BaseModel):
    date: date = Field(default_factory = date.today)
    access_token: str
    request_token: str




