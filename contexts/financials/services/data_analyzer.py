from hashlib import new

import pandas as pd 
import polars as pl
from utilities.pandas_mgr import PandasHelper
from contexts.financials.models import FinancialReport
from collections import defaultdict


def analyze(data: list[FinancialReport]):

    new_data = defaultdict(dict)


    for name, field in FinancialReport.model_fields.items():
        extra = field.json_schema_extra or {}
        category = extra.get("category")
        if category != "lineitem":
            continue
        # if not extra:
        #     continue  # skip fields with no lineitem metadata (isin, symbol, etc.)

        row = {
            "expense_category": extra.get("expense_category"),
            "statement_category": extra.get("statement_category"),
            "operating_nature": extra.get("operating_nature"),
            "cash_flow_nature": extra.get("cash_flow_nature"),
        }
        
        new_data[name] = row


    for each_report in data:
        year_quarter = str(each_report.fin_year) + each_report.quarter

        # for name, field in FinancialReport.model_fields.items():
        #     field_metadata = field.json_schema_extra
        #     if field_metadata:
        #         category = field_metadata.get("category")
        #         if category == "lineitem":
        #             line_items.append(name)

        for each_key in each_report.model_fields:
            if each_key in new_data:
                line_item_key = each_key
                value = getattr(each_report, each_key)
                if value:
                    value = (value / 10_000_000)
                    value = round(value, 2)
                new_data[line_item_key][year_quarter] = value

    df = pd.DataFrame(new_data).T
    # df.index.name = "line_item"   
    html_data = df.to_html(classes='data', index=True)
    return html_data
     


def analyze_with_polars(data):

    pl_df = pl.DataFrame(data)
    pl_df = pl_df.sort(['fin_year', 'quarter'], descending=[False, False])
    pl_df = pl_df.filter(pl.col('nature_of_report') == "Consolidated")

    pl_df = pl_df.with_columns(
        pl.col('fin_year').cast(pl.Utf8).alias('fin_year_str')
    )
    pl_df = pl_df.with_columns(
        (pl.col('fin_year_str') + "-" + pl.col('quarter')).alias('year_quarter')
    )
    numeric_cols = ['depreciation_amortization', 'employee_benefits_expense', 
                    'finance_costs', 'professional_charges']

    pl_df = pl_df.with_columns([
        (pl.col(c) / 10_000_000).round(2) for c in numeric_cols
    ])

    melted = pl_df.unpivot(
        index = ["year_quarter"],
        on = numeric_cols + ['nature_of_report'],
        variable_name='line_item',
        value_name='value1'
    )

    pivoted = melted.pivot(
        values='value1',
        index='line_item',
        on='year_quarter'
    )

    html_data = pivoted.to_pandas().to_html(classes='data', index=False) 
    return html_data







