import json
import time
from datetime import datetime, timedelta
from enum import Enum

from bson import json_util
from mongoengine import ValidationError

from .constants import (DATE_FORMAT, CE, PE, START_TIME, END_TIME,
                        FULL_TS_FORMAT, NSE_DATE_FORMAT, DATE_FORMAT_MAP)

TODAY = datetime.today().strftime(DATE_FORMAT)


def parse_timestamp(timestamp, format=FULL_TS_FORMAT):
    return datetime.strptime(timestamp, format)


def str_to_date(strDate, format=None):
    format = format or NSE_DATE_FORMAT
    try:
        _date = datetime.strptime(strDate, format).date()
    except ValueError:
        # print("Invalid Date format: %s" % str(exc))
        _date = datetime.strptime(strDate, DATE_FORMAT).date()
    return _date


def parse_dates_to_str(data):
    payload = []
    if isinstance(data, dict):
        payload = {
            key: (val.strftime(DATE_FORMAT_MAP[key])
                  if key in DATE_FORMAT_MAP else val)
            for key, val in data.items()}
    elif isinstance(data, list):
        payload = [
            {key: (val.strftime(DATE_FORMAT_MAP[key])
                   if key in DATE_FORMAT_MAP else val)
             for key, val in datum.items()} for datum in data]
    return payload


def parse_dates_to_str_old(data, key, format=DATE_FORMAT):
    if data and key in data[0].keys():
        return [{**item, key: item.get(key).strftime(format)}
                for item in data]
    return data


def parse_str_to_date(query):
    newQuery = query.copy()
    for key, val in query.items():
        newQuery[key] = (str_to_date(val, DATE_FORMAT_MAP[key])
                         if key in DATE_FORMAT_MAP and isinstance(val, str)
                         else val)
    return newQuery


def parse_json(data):
    return json.loads(json_util.dumps(data))


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
