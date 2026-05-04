from pydantic import BaseModel, field_validator
from typing import Optional


class Instrument(BaseModel):
    symbol: str
    name: str
    exchange: str
    sector: Optional[str] = None

    

