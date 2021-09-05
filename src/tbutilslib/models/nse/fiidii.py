"""FII-DII collection."""
from copy import deepcopy

from mongoengine import fields as mongoFields
from tbutilslib.config.constants import TB_DATE_FORMAT
from tbutilslib.config.database import MongoConfig
from tbutilslib.models.base import BaseCollection, BASE_META


class FiiDiiCollection(BaseCollection):
    """FII_DII Collection."""

    category = mongoFields.StringField(required=True)
    buyValue = mongoFields.FloatField()
    sellValue = mongoFields.FloatField()
    netValue = mongoFields.FloatField()
    onDate = mongoFields.DateField(format=TB_DATE_FORMAT)
    meta = deepcopy(BASE_META)
    meta['ordering'] = ["+onDate"]
    meta = {'collection': MongoConfig.FII_DII}
