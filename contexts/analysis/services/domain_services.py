import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from shared.infrastructure import get_big_query_client
import polars as pl


table_id = "stock-market-452020.datawarehouse.{table_name}"

report_query = f"""
    SELECT h.instr_token, h.interval, h.open, h.high, h.low, h.close, h.datetime, i.symbol 
    FROM `{table_id.format(table_name="historical")}` AS h
    LEFT JOIN `{table_id.format(table_name="instrument")}` AS i
    ON h.instr_token = i.instr_token 
    -- WHERE h.instr_token IN (2939649, 2939649, 98049, 4359425, 519937, 738561)
    WHERE i.symbol IN (
        "AARON",
        "TECHNVISN",
        "ORIENTLTD",
        "CNL",
        "KCPSUGIND",
        "BTML",
        "INDOBORAX",
        "CREATIVEYE",
        "JINDWORLD",
        "MAXIND",
        "LASERPOWER",
        "SHALPAINTS",
        "AKG",
        "WENDT",
        "GAEL",
        "ESAFSFB",
        "KABRAEXTRU",
        "DBL",
        "CINELINE",
        "THOMASCOTT"
    )
    AND h.datetime >= DATETIME("2026-07-23 09:00:00")
    AND h.datetime <  DATETIME("2026-07-23 16:00:00")
    ORDER BY h.instr_token, h.datetime
"""


class Figure:

    def __init__(self):
        self.fig = None

    def create_figure(self, n_rows, n_cols, titles, vertical_spacing):
        self.fig = make_subplots(
            rows=n_rows,
            cols=n_cols,
            subplot_titles=titles,
            vertical_spacing=vertical_spacing,
        )
        return self.fig

    def add_candlestick(self, window, row, col):
        self.fig.add_trace(
            go.Candlestick(
                x=window["datetime"],
                open=window["open"],
                high=window["high"],
                low=window["low"],
                close=window["close"],
                showlegend=False,
            ),
            row=row, col=col,
        )
        self.fig.update_xaxes(rangeslider_visible=False, row=row, col=col)


    def add_scatter(self, window_df, row_num, col_num):
        y_axis_expression = (
            pl.when(pl.col("signal_flag") == 1)
            .then(pl.col("close") + 3)
            .otherwise(None)
        )
        window_df = window_df.with_columns(y_axis_expression.alias("scatter_y"))

        self.fig.add_trace(
            go.Scatter(
                x = window_df["datetime"],
                y = window_df["scatter_y"],
                mode = "markers",
                marker = dict(size=10, color="black", symbol="triangle-up"),
                showlegend = False,
            ),
            row = row_num,
            col = col_num,
        )

    def add_scatterplot(self, axis_values:dict, pos:dict, mode:str):

        if mode == "markers":
            values = {
                "x": axis_values["x"], 
                "y": axis_values["y"], 
                "mode": "markers", 
                "marker" : dict(size=10, color="black", symbol="triangle-up"),
                "showlegend" : False
            }
        elif mode == "lines":
            values = {
                "x": axis_values["x"], 
                "y": axis_values["y"], 
                "mode": "lines", 
                "line" : dict(color="blue", width=1),
                "showlegend" : False,
                "name" : "MA"
            }

        self.fig.add_trace(
            go.Scatter(
                **values 
            ),
            row = pos["row"],
            col = pos["col"],
        )

    def finalize(self, width, height, title_text):
        self.fig.update_layout(width=width, height=height, title_text=title_text)
        return self.fig

    def save(self, path):
        self.fig.write_html(path)


class PolarsManager:

    def __init__(self, df) -> None:
        self.df = df

    def group_by(self, columns: list):
        groups = self.df.partition_by(columns, maintain_order=True) 
        return groups



class Signal: 

    def flag_consecutive_bullish_candles(self, pol_df, window_size):
        
        pol_df = pol_df.with_columns(
            (pl.col("close") - pl.col("open")).alias("change")
        )  
        pol_df = pol_df.with_columns(
            pl.col("change")
            .rolling_min(window_size = window_size)
            .over("instr_token")
            .alias("rolling_windows_min")
        )
        pol_df = pol_df.with_columns(
            (pl.col("rolling_windows_min") > 0)
            .cast(pl.Int8)          # True/False → 1/0
            .alias("signal_flag")
        )

        return pol_df 


    def add_moving_avg(self, df, window_size):
        df = df.with_columns(
            pl.col("close").rolling_mean(window_size=window_size).over("instr_token").alias("ma")
        )
        return df  



def generate_report():
    bq_client = get_big_query_client()
    arrow_table = bq_client.execute_query_as_arrow(report_query)
    df = pl.from_arrow(arrow_table)

    df = df.sort(["instr_token", "datetime"])
    df = df.with_columns(pl.col("datetime").dt.date().alias("date"))

    signal = Signal()
    df= signal.flag_consecutive_bullish_candles(df, window_size = 3)
    df = signal.add_moving_avg(df, 9)

    pol_df = PolarsManager(df)
    groups = pol_df.group_by(columns = ["instr_token", "symbol", "date"])


    window_dfs = []
    titles = []

    for each_df in groups:
        symbol = each_df["symbol"][0]
        day = each_df["date"][0].strftime("%-d %b %y")
        window_dfs.append(each_df.sort("datetime"))
        titles.append(f"{symbol} — {day}") 

    chart = Figure()
    # vertical_spacing = 0.09
    vertical_spacing = (1 / (len(groups) - 1)) * 0.5  # half the max gap
    chart.create_figure(n_rows= len(groups), n_cols=1, titles=titles, vertical_spacing=vertical_spacing)

    for i, window_df in enumerate(window_dfs, start=1):
        chart.add_candlestick(window_df, row=i, col=1)
        chart.add_scatter(window_df, i, 1)
        chart.add_scatterplot(
            axis_values= {
                "x" : window_df["datetime"],
                "y" : window_df["ma"]
            },
            pos = {
                "row" : i,
                "col" : 1
            },
            mode = "lines"
        )

    chart.finalize(width=1000, height=300 * len(groups), title_text="All Signal Windows")
    output_dir = "charts"
    chart.save(f"{output_dir}/all_signals.html")

    pass 


def get_df_1():
    bq_client = get_big_query_client()
    arrow_table = bq_client.execute_query_as_arrow(report_query)
    df = pl.from_arrow(arrow_table)

    df = df.sort(["instr_token", "datetime"])
    df = df.with_columns(
        (pl.col("close") - pl.col("open")).alias("change")
    )
    window_size = 3
    df = df.with_columns(
        pl.col("change")
        .rolling_min(window_size=window_size)
        .over("instr_token")
        .alias("rolling_windows_min")
    )
    df = df.with_row_index("idx")

    signal_indices = (
        df.filter(pl.col("rolling_windows_min") > 0)
        .get_column("idx")
        .to_list()
    )

    MAX_SIGNALS = 20
    signal_indices = signal_indices[:MAX_SIGNALS]

    output_dir = "charts"
    os.makedirs(output_dir, exist_ok=True)

    windows = []
    titles = []

    for sig_idx in signal_indices:
        start = max(sig_idx - 4, 0)
        window = df.slice(start, 10)

        instr_token = df.filter(pl.col("idx") == sig_idx)["instr_token"][0]
        window = window.filter(pl.col("instr_token") == instr_token)

        windows.append(window)
        titles.append(f"Signal idx={sig_idx} (instr_token={instr_token})")

    n = len(windows)
    vertical_spacing = min(0.02, 1 / (n - 1)) if n > 1 else 0.1

    chart = Figure()
    chart.create_figure(n_rows=n, n_cols=1, titles=titles, vertical_spacing=vertical_spacing)

    for i, window in enumerate(windows, start=1):
        chart.add_candlestick(window, row=i)

    chart.finalize(width=500, height=300 * n, title_text="All Signal Windows")
    chart.save(f"{output_dir}/all_signals.html")

    pass 