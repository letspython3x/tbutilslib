from copy import deepcopy
from datetime import datetime

from mongoengine import fields as mongoFields
from tbutilslib.config.constants import TB_DATE_FORMAT, FULL_TS_FORMAT
from tbutilslib.config.database import MongoConfig
from tbutilslib.models.base import BaseCollection, BASE_META


class OrdersCollection(BaseCollection):
    """TRADING_DATES collection."""

    orderId = mongoFields.IntField(required=True, unique=True)
    security = mongoFields.StringField(required=True)
    status = mongoFields.StringField()
    action = mongoFields.StringField()
    limitPrice = mongoFields.FloatField()
    auxPrice = mongoFields.FloatField()
    totalQuantity = mongoFields.FloatField()
    filled = mongoFields.FloatField()
    remaining = mongoFields.FloatField()
    onDate = mongoFields.DateField(format=TB_DATE_FORMAT)
    timestamp = mongoFields.DateTimeField(format=FULL_TS_FORMAT,
                                          default=datetime.now)
    meta = deepcopy(BASE_META)
    meta['ordering'] = ["-timestamp"]
    meta['collection'] = MongoConfig.TRADING_DATES
