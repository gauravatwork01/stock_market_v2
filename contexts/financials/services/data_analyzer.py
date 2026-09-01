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
    # df = add_totals(df)
    quarter_cols = [col for col in df.columns if col[0].isdigit()]
    df = add_calculations(df,quarter_cols)
    return df


def add_colors(df,quarter_cols):
    styled_df = df.style.set_properties(subset=quarter_cols, **{"background-color": "#f5f5f5","color": "black",})
    return styled_df


def add_calculations(df,quarter_cols):
    

    calculated_cols = {}
    for col in quarter_cols:
        # total_expense = df.groupby("expense_category")[col].sum()
        total_expense = df.groupby("expense_category")[col].transform("sum").astype(float)
        pct = (df[col].astype(float) / total_expense * 100).round(2)
        calculated_cols[f"{col}_exp_pct"] = pct

        col_index = df.columns.get_loc(col)
        df.insert(
            col_index + 1,
            f"{col}_exp_pct",
            pct
        ) 
    return df


def add_totals(df):
    quarter_cols = [col for col in df.columns if col[0].isdigit()]
    result_frames = []

    for category, group in df.groupby("expense_category"):
        result_frames.append(group)

        subtotal_data = {}
        for col in df.columns:
            if col in quarter_cols:
                subtotal_data[col] = group[col].sum()
            elif col == "expense_category":
                subtotal_data[col] = category
            else:
                subtotal_data[col] = group[col].iloc[0]

        subtotal = pd.DataFrame([subtotal_data], index=[f"Total {category}"])
        result_frames.append(subtotal)

    final_df = pd.concat(result_frames)
    return final_df

# st.dataframe(final_df, use_container_width=True)

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







