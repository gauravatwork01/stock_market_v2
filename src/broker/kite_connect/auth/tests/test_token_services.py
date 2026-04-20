

from src.broker.kite_connect.auth.service import TokenPolicy
from utilities import utilities
from datetime import datetime
from zoneinfo import ZoneInfo
import pytest
from unittest.mock import patch



@pytest.mark.parametrize("ist_datetime",  [
    (datetime(2026, 4, 19, 7,0,0, tzinfo=ZoneInfo("Asia/Kolkata"))),
    (datetime(2026, 4, 19, 14,0,0,  tzinfo=ZoneInfo("Asia/Kolkata"))),
    (datetime(2026, 4, 20, 5,0,0,  tzinfo=ZoneInfo("Asia/Kolkata"))),
])
def test_token_expiry(ist_datetime):

    token_expiry_datetime = TokenPolicy.get_token_expiry(
        ist_dt= ist_datetime
    )
    assert token_expiry_datetime.hour == 6
    assert token_expiry_datetime.date().day == 20






