
import time
import functools
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

def get_ist_date():
    return datetime.now(ZoneInfo("Asia/Kolkata")).date()

def get_ist_now_datetime():
    # return datetime.now(ZoneInfo("Asia/Kolkata"))
    return datetime.now(ZoneInfo("Asia/Kolkata")).replace(microsecond=0, tzinfo=None)

def get_utc_now_datetime():
    return datetime.now()


def convert_ist_to_utc(ist_dt):
    utc_dt = ist_dt.astimezone(ZoneInfo("UTC"))  
    return utc_dt


def log_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            msg = f"{func.__qualname__} took {elapsed:.4f}s"
            print(msg)
    return wrapper




