from enum import Enum

CE = "CE"
DATE_FORMAT = '%d-%m-%Y'  # 21-01-2021
END_TIME = '15:33:10'
FULL_TS_FORMAT = "%d-%b-%Y %H:%M:%S"
FULL_TS_FORMAT_TZ = "%Y-%m-%dT%H:%M:%S.%fZ"
MARKET_NAMES = ["Capital Market", "Currency", "Commodity", "Debt"]
NSE_DATE_FORMAT = "%d-%b-%Y"
PE = "PE"
PERCENT_INDEX = 4
PERCENT_EQUITY = 10
START_TIME = '09:00:00'
STOCK_FUTURES = "stock futures"
INDEX_FUTURES = "index futures"
VALID_CODES = [200, 201, 202]

DATE_FORMAT_MAP = {'expiryDate': DATE_FORMAT,
                   'eventDate': DATE_FORMAT,
                   'onDate': DATE_FORMAT,
                   'date30dAgo': DATE_FORMAT,
                   'timestamp': FULL_TS_FORMAT,
                   'lastUpdateTime': FULL_TS_FORMAT, }
OPTIONS_TYPE = {
    "call": CE,
    "put": PE,
    "-": "futures"
}


class EnumIndicator(Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    LONG_UNWINDING = "LONG UNWINDING"
    SHORT_COVERING = "LONG COVERING"
