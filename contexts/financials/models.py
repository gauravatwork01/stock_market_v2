
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


class OperatingNature(str):
    OPERATING = "operating"
    NON_OPERATING = "non_operating"


class CashNature(str):
    CASH = "cash"
    NON_CASH = "non_cash"


class FinancialReport(BaseModel):
    isin : str
    source_link: str = Field(
        description="whether nse-xbrl or nse-xlsx or any other 3rd pty etc.",
    )
    type_of_report_period: str = Field(
        description="Type of the report period, e.g., 'quarterly' or 'annual'.",
    )
    report_period_end_date : str = Field(
        description="End date of the financial report period.",
    )
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
            "category": "lineitem",
            "expense_category": LineItemCategory.EXPENSE, 
            "statement_category": StatementCategory.INCOME_STATEMENT
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
            "category": "lineitem",
            "expense_category": LineItemCategory.EXPENSE, 
            "operating_nature": OperatingNature.OPERATING,  
            "cash_flow_nature": CashNature.CASH,
            "statement_category": StatementCategory.INCOME_STATEMENT
        }
    )

    depreciation_amortization: Optional[float] = Field(
        description="""expense on assets incurred by the company during the financial period.
            or value lost by a thing during a period
            or value spent on assets only during the period
            or amount/life(5yrs) * the period
        """,
        json_schema_extra={
            "category": "lineitem",
            "expense_category": LineItemCategory.EXPENSE, 
            "operating_nature": OperatingNature.OPERATING, 
            "cash_flow_nature": CashNature.NON_CASH, 
            "statement_category": StatementCategory.INCOME_STATEMENT
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
            "category": "lineitem",
            "expense_category": LineItemCategory.EXPENSE, 
            "operating_nature": OperatingNature.OPERATING, 
            "cash_flow_nature": CashNature.CASH, 
            "statement_category": StatementCategory.INCOME_STATEMENT
        }
    )

    other_production_expenses: Optional[float] = Field(
        description="""
            costs directly tied to delivering the company's core services/products
            e.g 1. software-licenses and tools used on client projects 
            (like cursor subscription, copilot, jeera-for ticket mgmt)
            2. cloud infrastructure-service subscriptions etc. etc. 
        """,
        json_schema_extra={
            "category": "lineitem",
            "expense_category": LineItemCategory.EXPENSE, 
            "operating_nature": OperatingNature.OPERATING, 
            "cash_flow_nature": CashNature.CASH, 
            "statement_category": StatementCategory.INCOME_STATEMENT
        }
    )

    other_expenses: Optional[float] = Field(
        description="""It puts together small expenses all together that aren't big enough to get 
            their own seperate line-item
            like 1. office rent
            2. markesting cost,
            3. repair and maintenance 
            4. utilities (electricity, water, internet)
        """,
        json_schema_extra={
            "category": "lineitem",
            "expense_category": LineItemCategory.EXPENSE, 
            "operating_nature": OperatingNature.OPERATING, 
            "cash_flow_nature": CashNature.CASH, 
            "statement_category": StatementCategory.INCOME_STATEMENT
        }
    )
    cost_of_materials_consumed: Optional[float] = Field(
        description="""cost of raw materials and components consumed by the company during the financial period.""",
        json_schema_extra={
            "category": "lineitem",
            "expense_category": LineItemCategory.EXPENSE, 
            "operating_nature": OperatingNature.OPERATING, 
            "cash_flow_nature": CashNature.CASH, 
            "statement_category": StatementCategory.INCOME_STATEMENT
        }
    )

    # other_production_expenses

    
    






