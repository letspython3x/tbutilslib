"""Index Data Collection."""
from copy import deepcopy

from mongoengine import fields as mongoFields
from ...config.database import MongoConfig
from ..base import BaseCollection, BASE_META
from ...utils.enums import DateFormatEnum


class IndexCollection(BaseCollection):
    """Index Data collection."""

    security = mongoFields.StringField(required=True)
    identifier = mongoFields.StringField()
    series = mongoFields.StringField()
    open = mongoFields.FloatField()
    day_high = mongoFields.FloatField()
    day_low = mongoFields.FloatField()
    last_price = mongoFields.FloatField()
    previous_close = mongoFields.FloatField()
    change = mongoFields.FloatField()
    p_change = mongoFields.FloatField()
    ffmc = mongoFields.FloatField()
    year_high = mongoFields.FloatField()
    year_low = mongoFields.FloatField()
    total_traded_volume = mongoFields.IntField()
    total_traded_value = mongoFields.FloatField()
    near_weak_high = mongoFields.FloatField()
    near_weak_low = mongoFields.FloatField()
    per_change_30d = mongoFields.FloatField()
    per_change_365d = mongoFields.FloatField()
    chart_30d_path = mongoFields.StringField()
    chart_today_path = mongoFields.StringField()
    chart_365d_path = mongoFields.StringField()
    date_30d_ago = mongoFields.DateField(format=DateFormatEnum.TB_DATE.value)
    date_365d_ago = mongoFields.DateField(format=DateFormatEnum.TB_DATE.value)
    timestamp = mongoFields.DateTimeField(format=DateFormatEnum.FULL_TS.value)
    last_update_time = mongoFields.DateTimeField(format=DateFormatEnum.FULL_TS.value)
    on_date = mongoFields.DateField(format=DateFormatEnum.TB_DATE.value)
    meta = deepcopy(BASE_META)
    meta["ordering"] = ["-timestamp"]
    meta["collection"] = MongoConfig.INDEX_DATA
