"""Constants."""
from enum import Enum

CE = "CE"
PE = "PE"
OPTIONS_TYPE = {"call": CE,
                "put": PE,
                "-": "futures"}

MARKET_NAMES = ["Capital Market", "Currency", "Commodity", "Debt"]

TB_DATE_FORMAT = "%d-%m-%Y"  # 21-01-2021
NSE_DATE_FORMAT = "%d-%b-%Y"  # 21-sep-2021
FULL_TS_FORMAT = "%d-%b-%Y %H:%M:%S"
FULL_TS_FORMAT_TZ = "%Y-%m-%dT%H:%M:%S.%fZ"
TB_DT_MAPPING = {'expiryDate': TB_DATE_FORMAT,
                 'eventDate': TB_DATE_FORMAT,
                 'onDate': TB_DATE_FORMAT,
                 'date30dAgo': TB_DATE_FORMAT,
                 'timestamp': FULL_TS_FORMAT,
                 'lastUpdateTime': FULL_TS_FORMAT, }

PERCENT_INDEX = 3
PERCENT_EQUITY = 5
RETRY_SEC = 150

START_TIME = "09:00:00"
END_TIME = "15:33:10"

STOCK_FUTURES = "stock futures"
INDEX_FUTURES = "index futures"
FUTURES = "FUTURES"
OPTIONS = "OPTIONS"

VALID_CODES = [200, 201, 202]


class Position(Enum):
    """Enum for Indicator."""

    LONG = "LONG POSITIONS"
    SHORT = "SHORT POSITIONS"
    LONG_UNWINDING = "LONG UNWINDING"
    SHORT_COVERING = "SHORT COVERING"
