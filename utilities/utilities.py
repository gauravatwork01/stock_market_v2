

from datetime import datetime
from zoneinfo import ZoneInfo

def get_ist_date():
    return datetime.now(ZoneInfo("Asia/Kolkata")).date()








