"""Common Utils."""
import logging
from datetime import datetime, timedelta

from marshmallow import ValidationError

from .dtu import parse_str_to_date_in_dict
from .enums import MarketTimingEnum

logger = logging.getLogger("tbutilslib." + __name__)


def indexed_data(index: str, data: list[dict]) -> dict:
    return {index.format(**datum): datum for datum in data}


def separate_by_index(index: str, cache: list[dict], live: list[dict]) -> tuple:
    """Separate by index.

    segregates the data for post and put to TbApi.
    Args:
        index: str
        cache: List[dict]
        live: List[dict]
    :return tuple
    """
    cache_indexed = indexed_data(index, cache)
    live_indexed = indexed_data(index, live)

    live_keys = set(live_indexed.keys())
    cache_keys = set(cache_indexed.keys())

    post_keys = live_keys.difference(cache_keys)
    put_keys = live_keys.intersection(cache_keys)

    post_data = [live_indexed[key] for key in post_keys]
    put_data = [live_indexed[key] for key in put_keys]
    return post_data, put_data


def filter_fno_securities(data: list[dict]) -> tuple:
    """
    Filter the securities depending on if the security is future & options
    enabled.
    """
    fno = list({item["security"] for item in data if item["is_fno"]})
    non_fno = list({item["security"] for item in data if not item["is_fno"]})
    return fno, non_fno


def get_next_thursday(dt):
    day_dict = {
        "monday": 3,
        "tuesday": 2,
        "wednesday": 1,
        "thursday": 0,
        "friday": 6,
        "saturday": 5,
        "sunday": 4,
    }
    dt = dt or datetime.today()
    expected_days = day_dict.get(dt.strftime("%A").lower())
    return (dt + timedelta(days=expected_days)).strftime("%d-%b-%Y")


def validate_quantity(number, valid_value=0):
    if not number or number <= valid_value:
        logger.warning(f"Value: {number} must be greater than {valid_value}.")
        return 0


def is_trading_hours_open() -> bool:
    return bool(
        MarketTimingEnum.PRE_OPEN.value
        < datetime.now().time()
        < MarketTimingEnum.CLOSE.value
    )


def is_valid_schema(schema, data):
    try:
        data = parse_str_to_date_in_dict(data)
        schema().load(data, many=isinstance(data, list))
        return True
    except ValidationError as err:
        print(f"Validation Error: {err.messages}")
