from copy import deepcopy

from mongoengine import fields as mongoFields

from app.config import MongoConfig
from app.models.base import BaseCollection, BASE_META
from app.utils.constants import DATE_FORMAT
from app.utils.common import not_empty


class FiiDiiCollection(BaseCollection):
    """FII DII Collection."""
    category = mongoFields.StringField(validation=not_empty)
    buyValue = mongoFields.FloatField()
    sellValue = mongoFields.FloatField()
    netValue = mongoFields.FloatField()
    onDate = mongoFields.DateField(format=DATE_FORMAT)
    meta = deepcopy(BASE_META)
    meta['ordering'] = ["+onDate"]
    meta = {'collection': MongoConfig.FII_DII}
