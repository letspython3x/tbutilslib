from app.utils.constants import FULL_TS_FORMAT, DATE_FORMAT
from copy import deepcopy

from mongoengine import fields as mongoFields

from app.config import MongoConfig
from app.models.base import BaseCollection, BASE_META
from app.utils.common import not_empty


class NiftyEquityCollection(BaseCollection):
    """NIFTY_EQUITY collection."""
    security = mongoFields.StringField(validation=not_empty)
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
    date30dAgo = mongoFields.DateField(format=DATE_FORMAT)
    perChange30d = mongoFields.FloatField()
    chart30dPath = mongoFields.StringField()
    chartTodayPath = mongoFields.StringField()
    onDate = mongoFields.DateField(format=DATE_FORMAT)
    timestamp = mongoFields.DateTimeField(format=FULL_TS_FORMAT)
    meta = deepcopy(BASE_META)
    meta['ordering'] = ["-timestamp"]
    meta['collection'] = MongoConfig.NIFTY_EQUITY
