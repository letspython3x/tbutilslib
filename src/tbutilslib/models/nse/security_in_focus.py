"""Security in Focus collection."""
from copy import deepcopy

from mongoengine import fields as mFields
from tbutilslib.config.constants import TB_DATE_FORMAT, FULL_TS_FORMAT
from tbutilslib.config.database import MongoConfig
from tbutilslib.models.base import BaseCollection, BASE_META


class SecurityInFocusCollection(BaseCollection):
    """SECURITY_IN_FOCUS collection."""

    security = mFields.StringField(required=True)
    strikePrices = mFields.ListField(mFields.IntField())
    timestamp = mFields.DateTimeField(format=FULL_TS_FORMAT)
    onDate = mFields.DateField(format=TB_DATE_FORMAT)
    expiryDates = mFields.ListField(mFields.DateField(format=TB_DATE_FORMAT))
    meta = deepcopy(BASE_META)
    meta['ordering'] = ["-timestamp"]
    meta['collection'] = MongoConfig.SECURITY_IN_FOCUS
