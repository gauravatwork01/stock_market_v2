
from pydantic import BaseModel, Field, computed_field, ConfigDict
from pydantic import BaseModel
from typing import List


class Historical(BaseModel):

    symbol: str 
    open: float
    high: float
    low: float
    close: float
    interval : str 
    






