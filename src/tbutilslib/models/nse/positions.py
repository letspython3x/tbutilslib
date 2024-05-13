from copy import deepcopy
from datetime import datetime

from mongoengine import fields as mongoFields

from ..base import BaseCollection, BASE_META
from ...config import MongoConfig
from ...utils.enums import DateFormatEnum


class PositionsCollection(BaseCollection):
    """POSITIONS collection."""

    account = mongoFields.StringField(required=True)
    security = mongoFields.StringField(required=True)
    secType = mongoFields.StringField()
    currency = mongoFields.StringField()
    position = mongoFields.FloatField()
    avg_cost = mongoFields.FloatField()
    on_date = mongoFields.DateField(format=DateFormatEnum.TB_DATE.value)
    timestamp = mongoFields.DateTimeField(
        format=DateFormatEnum.FULL_TS.value, default=datetime.now
    )
    meta = deepcopy(BASE_META)
    meta["ordering"] = ["-timestamp"]
    meta["collection"] = MongoConfig.POSITIONS
