from copy import deepcopy
from app.utils.constants import DATE_FORMAT, FULL_TS_FORMAT

from mongoengine import fields as mongoFields

from app.config import MongoConfig
from app.models.base import BaseCollection, BASE_META


class SecurityInFocusCollection(BaseCollection):
    """SECURITY IN FOCUS collection."""
    security = mongoFields.StringField(required=True)
    expiryDates = mongoFields.ListField(mongoFields.DateField(format=DATE_FORMAT))
    strikePrices = mongoFields.ListField(mongoFields.IntField())
    timestamp = mongoFields.DateTimeField(format=FULL_TS_FORMAT)
    onDate = mongoFields.DateField(format=DATE_FORMAT)
    meta = deepcopy(BASE_META)
    meta['ordering'] = ["-timestamp"]
    meta['collection'] = MongoConfig.SECURITY_IN_FOCUS
