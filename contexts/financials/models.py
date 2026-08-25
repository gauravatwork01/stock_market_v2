
from pydantic import Field
from datetime import date
from typing import Optional

from pydantic import BaseModel



class Financials(BaseModel):

    symbol: str 
    company_name: Optional[str] = None
    results_meeting_date: date
    sebi_intimation_date: date = Field(
        description="Date when SEBI was formally intimated about the financial results meeting.",
    )
    scale : str = Field(
        description="unit of scale for the financials, e.g. 'in crores', 'in millions', etc.",
    )
    quarter : str = Field(
        description="Financial quarter for which the financials are reported",
    )
    






