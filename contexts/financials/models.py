
from turtle import st

from pydantic import Field
from datetime import date
from typing import Optional

from pydantic import BaseModel
from enum import Enum

class StatementCategory(str):
    BALANCE_SHEET = "balance_sheet"
    INCOME_STATEMENT = "income_statement"
    CASH_FLOW = "cash_flow"


class LineItemCategory(str):
    INCOME = "income"
    EXPENSE = "expense"


# class ExpenseCategory(str):
#     OPERATING = "operating"
#     NON_OPERATING = "non_operating"


class OperatingNature(str, Enum):
    OPERATING = "operating"
    NON_OPERATING = "non_operating"


class CashNature(str, Enum):
    CASH = "cash"
    NON_CASH = "non_cash"


class FinancialReport(BaseModel):
    isin : str
    source_link: str 
    source: str 
    symbol: str 
    company_name: Optional[str] = None
    sebi_intimation_date: str = Field(
        description="Date when SEBI was formally intimated about the financial results meeting.",
    )
    results_approval_date: str = Field(
        description="Date when the board meeting was held to approve the financial results.",
    )
    
    quarter : str = Field(
        description="Financial quarter for which the financials are reported",
    )

    fin_year : int = Field(
        description="Financial year for which the financials are reported",
    )
    nature_of_report : str = Field(
        description="Nature of the financial report, e.g., 'standalone' or 'consolidated' ",
    )
    finance_costs: Optional[float] = Field(
        description="Interests incurred on borrowings during the financial period.",
        json_schema_extra={
            "lineitem_category": LineItemCategory.EXPENSE, 
            "statement": StatementCategory.INCOME_STATEMENT
        }
    )
    employee_benefits_expense: Optional[float] = Field(
        description="""
                    Employee benefits expense incurred by the company during the financial period, like 
                    1. salaries
                    2. gratuity
                    3. PF
                    4. outing/trips etc. etc. 
                    5. ESOPs (non-cash)
                    """,
        json_schema_extra={
            "lineitem_category": LineItemCategory.EXPENSE, 
            "operating_nature": OperatingNature.OPERATING,  
            "cash_flow_nature": CashNature.CASH,
            "statement": StatementCategory.INCOME_STATEMENT
        }
    )

    depreciation_amortization: Optional[float] = Field(
        description="""expense on assets incurred by the company during the financial period.
            or value lost by a thing during a period
            or value spent on assets only during the period
            or amount/life(5yrs) * the period
        """,
        json_schema_extra={
            "lineitem_category": LineItemCategory.EXPENSE, 
            "operating_nature": OperatingNature.OPERATING, 
            "cash_flow_nature": CashNature.NON_CASH, 
            "statement": StatementCategory.INCOME_STATEMENT
        }
    )

    professional_charges : Optional[float] = Field(
        description="""payments made to external professionals for their services to the company like
            1.Consultant fees, 
            2.advisory fees, 
            3. Equipment rental charges (e.g kiosk machines)
            etc.
        """,
        json_schema_extra={
            "lineitem_category": LineItemCategory.EXPENSE, 
            "operating_nature": OperatingNature.OPERATING, 
            "cash_flow_nature": CashNature.CASH, 
            "statement": StatementCategory.INCOME_STATEMENT
        }
    )
    






