"""FII-DII collection."""
from copy import deepcopy

from mongoengine import fields as mongoFields

from ..base import BaseCollection, BASE_META
from ...config import MongoConfig
from ...utils.enums import DateFormatEnum


class FiiDiiCollection(BaseCollection):
    """FII_DII Collection."""

    category = mongoFields.StringField(required=True)
    buy_value = mongoFields.FloatField()
    sell_value = mongoFields.FloatField()
    net_value = mongoFields.FloatField()
    on_date = mongoFields.DateField(format=DateFormatEnum.TB_DATE.value)
    meta = deepcopy(BASE_META)
    meta["ordering"] = ["+on_date"]
    meta = {"collection": MongoConfig.FII_DII}
