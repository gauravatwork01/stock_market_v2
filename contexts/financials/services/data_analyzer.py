import pandas as pd 
import polars as pl
from utilities.pandas_mgr import PandasHelper




def analyze(data):
    df = pd.DataFrame(data)
    df = PandasHelper.sort(df, ["fin_year", "quarter"], ascending=[False, False])

    
    pass 



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







