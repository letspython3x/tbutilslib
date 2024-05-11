"""Security in Focus collection."""
from copy import deepcopy
from datetime import date, datetime

from mongoengine import fields as mFields
from tbutilslib.config.constants import TB_DATE_FORMAT, FULL_TS_FORMAT
from tbutilslib.config.database import MongoConfig
from tbutilslib.models.base import BaseCollection, BASE_META


class SecurityInFocusCollection(BaseCollection):
    """SECURITY_IN_FOCUS collection."""

    security = mFields.StringField(required=True)
    strikePrices = mFields.ListField(mFields.IntField())
    fno = mFields.BooleanField(default=False)
    onDate = mFields.DateField(format=TB_DATE_FORMAT, default=date.today())
    timestamp = mFields.DateTimeField(format=FULL_TS_FORMAT, default=datetime.now)
    meta = deepcopy(BASE_META)
    meta["ordering"] = ["-timestamp"]
    meta["collection"] = MongoConfig.SECURITY_IN_FOCUS
