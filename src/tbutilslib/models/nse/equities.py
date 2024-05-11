"""Nifty Equity Collection."""
from copy import deepcopy

from mongoengine import fields as mongoFields
from tbutilslib.config.constants import FULL_TS_FORMAT, TB_DATE_FORMAT
from tbutilslib.config.database import MongoConfig
from tbutilslib.models.base import BaseCollection, BASE_META


class NiftyEquityCollection(BaseCollection):
    """NIFTY_EQUITY collection."""

    security = mongoFields.StringField(required=True)
    isFNOSec = mongoFields.BooleanField()
    lastPrice = mongoFields.FloatField()
    identifier = mongoFields.StringField()
    series = mongoFields.StringField()
    open = mongoFields.FloatField()
    dayHigh = mongoFields.FloatField()
    dayLow = mongoFields.FloatField()
    previousClose = mongoFields.FloatField()
    change = mongoFields.FloatField()
    pChange = mongoFields.FloatField()
    totalTradedVolume = mongoFields.IntField()
    totalTradedValue = mongoFields.FloatField()
    lastUpdateTime = mongoFields.DateTimeField(format=FULL_TS_FORMAT)
    yearHigh = mongoFields.FloatField()
    yearLow = mongoFields.FloatField()
    nearWKH = mongoFields.FloatField()
    nearWKL = mongoFields.FloatField()
    perChange365d = mongoFields.FloatField()
    date30dAgo = mongoFields.DateField(format=TB_DATE_FORMAT)
    perChange30d = mongoFields.FloatField()
    chart30dPath = mongoFields.StringField()
    chartTodayPath = mongoFields.StringField()
    onDate = mongoFields.DateField(format=TB_DATE_FORMAT)
    timestamp = mongoFields.DateTimeField(format=FULL_TS_FORMAT)
    meta = deepcopy(BASE_META)
    meta["ordering"] = ["-timestamp"]
    meta["collection"] = MongoConfig.NIFTY_EQUITY


class AdvanceDeclineCollection(BaseCollection):
    """ADVANCE_DECLINE collection."""

    declines = mongoFields.IntField()
    advances = mongoFields.IntField()
    unchanged = mongoFields.IntField()
    onDate = mongoFields.DateField(format=TB_DATE_FORMAT)
    timestamp = mongoFields.DateTimeField(format=FULL_TS_FORMAT)
    meta = deepcopy(BASE_META)
    meta["ordering"] = ["-timestamp"]
    meta["collection"] = MongoConfig.ADVANCE_DECLINE
