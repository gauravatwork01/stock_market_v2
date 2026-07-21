


from pydantic import BaseModel, Field
from typing import Optional


class Instrument(BaseModel):
    instr_token: int = Field(
        description="Unique identifier for an instrument"
    )
    symbol: str
    name: str
    exchange: str
    sector: Optional[str] = None


    

