from datetime import datetime
from zoneinfo import ZoneInfo


IST = ZoneInfo("Asia/Kolkata")

class DatetimeHelper:

    def now_ist():
        return datetime.now(IST)

    

