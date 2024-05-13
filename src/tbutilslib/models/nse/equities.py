"""Nifty Equity Collection."""
from copy import deepcopy

from mongoengine import fields as mongoFields
from ...config.database import MongoConfig
from ..base import BaseCollection, BASE_META
from ...utils.enums import DateFormatEnum


class NiftyEquityCollection(BaseCollection):
    """NIFTY_EQUITY collection."""

    security = mongoFields.StringField(required=True)
    is_fno_sec = mongoFields.BooleanField()
    last_price = mongoFields.FloatField()
    identifier = mongoFields.StringField()
    series = mongoFields.StringField()
    open = mongoFields.FloatField()
    day_high = mongoFields.FloatField()
    day_low = mongoFields.FloatField()
    previous_close = mongoFields.FloatField()
    change = mongoFields.FloatField()
    p_Change = mongoFields.FloatField()
    total_traded_volume = mongoFields.IntField()
    total_traded_value = mongoFields.FloatField()
    last_update_time = mongoFields.DateTimeField(format=DateFormatEnum.FULL_TS.value)
    year_high = mongoFields.FloatField()
    year_low = mongoFields.FloatField()
    near_weak_high = mongoFields.FloatField()
    near_weak_low = mongoFields.FloatField()
    per_change_365d = mongoFields.FloatField()
    date_30d_ago = mongoFields.DateField(format=DateFormatEnum.TB_DATE.value)
    per_change_30d = mongoFields.FloatField()
    chart_30d_path = mongoFields.StringField()
    chart_today_path = mongoFields.StringField()
    on_date = mongoFields.DateField(format=DateFormatEnum.TB_DATE.value)
    timestamp = mongoFields.DateTimeField(format=DateFormatEnum.FULL_TS.value)
    meta = deepcopy(BASE_META)
    meta["ordering"] = ["-timestamp"]
    meta["collection"] = MongoConfig.NIFTY_EQUITY


class AdvanceDeclineCollection(BaseCollection):
    """ADVANCE_DECLINE collection."""

    declines = mongoFields.IntField()
    advances = mongoFields.IntField()
    unchanged = mongoFields.IntField()
    on_date = mongoFields.DateField(format=DateFormatEnum.TB_DATE.value)
    timestamp = mongoFields.DateTimeField(format=DateFormatEnum.FULL_TS.value)
    meta = deepcopy(BASE_META)
    meta["ordering"] = ["-timestamp"]
    meta["collection"] = MongoConfig.ADVANCE_DECLINE
