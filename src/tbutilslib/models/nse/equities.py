"""Nifty Equity Collection."""
from copy import deepcopy

from mongoengine import fields as mongoFields
from ...config.database import MongoConfig
from ..base import BaseCollection, BASE_META
from ...utils.enums import DateFormatEnum


class NiftyEquityCollection(BaseCollection):
    """NIFTY_EQUITY collection."""

    security = mongoFields.StringField(required=True)
    identifier = mongoFields.StringField()
    isin = mongoFields.StringField()
    series = mongoFields.StringField()
    open = mongoFields.FloatField()
    day_high = mongoFields.FloatField()
    day_low = mongoFields.FloatField()
    last_price = mongoFields.FloatField()
    previous_close = mongoFields.FloatField()
    change = mongoFields.FloatField()
    p_change = mongoFields.FloatField()
    total_traded_volume = mongoFields.IntField()
    total_traded_value = mongoFields.FloatField()
    year_high = mongoFields.FloatField()
    year_low = mongoFields.FloatField()
    ffmc = mongoFields.FloatField()
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
    on_date = mongoFields.DateField(format=DateFormatEnum.TB_DATE.value)
    last_update_time = mongoFields.DateTimeField(format=DateFormatEnum.FULL_TS.value)
    company_name = mongoFields.StringField()
    industry = mongoFields.StringField()
    active_series = mongoFields.ListField(mongoFields.StringField())
    debt_series = mongoFields.ListField(mongoFields.StringField())
    temp_suspended_series = mongoFields.ListField(mongoFields.StringField())
    is_fno_sec = mongoFields.BooleanField()
    is_ca_sec = mongoFields.BooleanField()
    is_slb_sec = mongoFields.BooleanField()
    is_debt_sec = mongoFields.BooleanField()
    is_suspended = mongoFields.BooleanField()
    is_etf_Sec = mongoFields.BooleanField()
    is_delisted = mongoFields.BooleanField()
    is_municipal_bond = mongoFields.BooleanField()
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


class EquityMetaCollection(BaseCollection):
    """STATIC_EQUITY collection."""

    security = mongoFields.StringField(required=True)
    company = mongoFields.StringField()
    industry = mongoFields.StringField()
    isin = mongoFields.StringField()
    series = mongoFields.StringField()
    is_fno = mongoFields.BooleanField(default=False)
    is_nifty_50 = mongoFields.BooleanField(default=False)
    is_nifty_100 = mongoFields.BooleanField(default=False)
    is_nifty_500 = mongoFields.BooleanField(default=False)
    meta = deepcopy(BASE_META)
    meta["ordering"] = ["-security"]
    meta["collection"] = MongoConfig.EQUITY_META
