"""Common Utils."""
import time
from datetime import datetime, timedelta, date
from typing import List, Dict, Any

from tbutilslib.config.constants import (TB_DATE_FORMAT,
                                         START_TIME, END_TIME,
                                         FULL_TS_FORMAT,
                                         NSE_DATE_FORMAT,
                                         TB_DT_MAPPING)

TODAY = datetime.today().strftime(TB_DATE_FORMAT)


def parse_timestamp(timestamp: str, format: str = FULL_TS_FORMAT) -> datetime:
    """Convert a string timestamp to datetime.

    Args:
        timestamp: str
        format: str
    Returns datetime
    """
    return datetime.strptime(timestamp, format)


def str_to_date(strDate: str, format: str = None) -> date:
    """Convert a date string to actual date.

    Args:
        strDate: str
        format: str
    Returns date
    """
    format = format or NSE_DATE_FORMAT
    try:
        _date = datetime.strptime(strDate, format).date()
    except ValueError:
        _date = datetime.strptime(strDate, TB_DATE_FORMAT).date()
    return _date


def date_to_str(val: date, format: str) -> str:
    """Convert a date or datetime to a string.

    Args:
        val: date
        format: str
    Returns date
    """
    return val.strftime(format)


def parse_dates_to_str(dates: List[Dict]) -> List[Dict]:
    """Convert List of datetime values to string date values.

    Args:
        dates: List[Dict]
    Returns: List[Dict]
    """
    data = dates if isinstance(dates, list) else [dates]
    payload = [{key: (date_to_str(val, TB_DT_MAPPING[key])
                      if key in TB_DT_MAPPING else val)
                for key, val in datum.items()}
               for datum in data]

    return payload


def parse_str_to_date(dateQuery: dict) -> dict:
    """Convert a date string to actual date.

    Args:
        dateQuery: dict
    Returns date
    """
    newQuery = dateQuery.copy()
    for key, val in dateQuery.items():
        newQuery[key] = (str_to_date(val, TB_DT_MAPPING[key])
                         if key in TB_DT_MAPPING and isinstance(val, str)
                         else val)
    return newQuery


def change_date_format(val: Any, reqFormat: str = TB_DATE_FORMAT):
    """Expects a date-string or a date/datetime and converts it to new
    dateformat.
    """
    _date = str_to_date(val) if isinstance(val, str) else val
    return _date.strftime(reqFormat)


def is_month_same(_date1: date, _date2: date) -> bool:
    """Compare dates to check if the month is same."""
    _date1 = str_to_date(_date1) if isinstance(_date1, str) else _date1
    _date2 = str_to_date(_date2) if isinstance(_date2, str) else _date2
    return _date1.month == _date2.month


def indexed_data(index: str, data: List[Dict]) -> Dict:
    return {index.format(**datum): datum for datum in data}


def separate_by_index(index: str, cache: List[Dict], live: List[Dict]) -> tuple:
    """Separate by index.

    segregates the data for post and put to TbApi.
    Args:
        index: str
        cache: List[dict]
        live: List[dict]
    :return tuple
    """
    cacheInd = indexed_data(index, cache)
    liveInd = indexed_data(index, live)

    liveKeys = set(liveInd.keys())
    cacheKeys = set(cacheInd.keys())

    postKeys = liveKeys.difference(cacheKeys)
    putKeys = liveKeys.intersection(cacheKeys)

    postData = [liveInd[key] for key in postKeys]
    putData = [liveInd[key] for key in putKeys]
    return postData, putData


def filter_fno_securities(data: list = None) -> tuple:
    """
    Filter the securities depending on if the security is future & options
    enabled.
    """
    print("Separate securities if FnO enabled...")
    fno = list({item['security'] for item in data if item['fno']})
    nonFno = list({item['security'] for item in data if not item['fno']})
    print(f"Securities Separated-> FNO: {len(fno)} : NON-FNO: {len(nonFno)}")
    return fno, nonFno


def parse_dates_to_str_old(data, key, format=TB_DATE_FORMAT):
    if data and key in data[0].keys():
        return [{**item, key: item.get(key).strftime(format)}
                for item in data]
    return data


def get_next_thursday(dt):
    print("\n" + "*" * 25)
    dayDict = {
        'monday': 3,
        'tuesday': 2,
        'wednesday': 1,
        'thursday': 0,
        'friday': 6,
        'saturday': 5,
        'sunday': 4,
    }
    dt = dt or datetime.today()
    expectedDays = dayDict.get(dt.strftime('%A').lower())
    nextDt = (dt + timedelta(days=expectedDays)).strftime('%d-%b-%Y')
    # print(f"Expected Days: {expectedDays}")
    # print(f"Next Day: {nextDt}")
    return nextDt


def liner(symbol='*', count=80):
    return f'{symbol * count}'


def is_trading_hours_open() -> bool:
    STARS = liner()
    flag = True
    currTime = time.strftime("%H:%M:%S", time.localtime())
    print(f"Current Time: {currTime}")
    if currTime < START_TIME:
        print(f"{STARS} Day is yet to start {STARS}")
        time.sleep(600)
    elif currTime > END_TIME:
        print(f"{STARS} Day is Over {STARS}")
        flag = False
    return flag
