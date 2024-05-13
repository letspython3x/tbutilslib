from copy import deepcopy
from datetime import datetime

from mongoengine import fields as mongoFields

from ..base import BaseCollection, BASE_META
from ...config import MongoConfig
from ...utils.enums import DateFormatEnum


class OrdersCollection(BaseCollection):
    """ORDERS collection."""

    order_id = mongoFields.IntField(required=True)
    security = mongoFields.StringField(required=True)
    sec_type = mongoFields.StringField(required=True)
    order_type = mongoFields.StringField(required=True)
    status = mongoFields.StringField()
    action = mongoFields.StringField()
    limit_price = mongoFields.FloatField()
    aux_price = mongoFields.FloatField()
    total_quantity = mongoFields.FloatField()
    filled = mongoFields.FloatField()
    remaining = mongoFields.FloatField()
    avg_fill_price = mongoFields.FloatField()
    on_date = mongoFields.DateField(format=DateFormatEnum.TB_DATE.value)
    timestamp = mongoFields.DateTimeField(
        format=DateFormatEnum.FULL_TS.value, default=datetime.now
    )
    meta = deepcopy(BASE_META)
    meta["ordering"] = ["-timestamp"]
    meta["collection"] = MongoConfig.ORDERS
