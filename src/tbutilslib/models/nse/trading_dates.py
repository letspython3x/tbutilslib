from copy import deepcopy
from datetime import datetime

from mongoengine import fields as mongoFields

from ..base import BaseCollection, BASE_META
from ...config import MongoConfig
from ...utils.enums import DateFormatEnum


class TradingDatesCollection(BaseCollection):
    """TRADING_DATES collection."""

    last_trading_date = mongoFields.DateField(format=DateFormatEnum.TB_DATE.value)
    current_trading_date = mongoFields.DateField(format=DateFormatEnum.TB_DATE.value)
    timestamp = mongoFields.DateTimeField(
        format=DateFormatEnum.FULL_TS.value, default=datetime.now
    )
    meta = deepcopy(BASE_META)
    meta["ordering"] = ["-timestamp"]
    meta["collection"] = MongoConfig.TRADING_DATES
