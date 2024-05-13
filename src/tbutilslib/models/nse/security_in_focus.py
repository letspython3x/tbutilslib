"""Security in Focus collection."""
from copy import deepcopy
from datetime import date, datetime

from mongoengine import fields as mFields

from ..base import BaseCollection, BASE_META
from ...config import MongoConfig
from ...utils.enums import DateFormatEnum


class SecurityInFocusCollection(BaseCollection):
    """SECURITY_IN_FOCUS collection."""

    security = mFields.StringField(required=True)
    strike_prices = mFields.ListField(mFields.IntField())
    is_fno = mFields.BooleanField(default=False)
    on_date = mFields.DateField(
        format=DateFormatEnum.TB_DATE.value, default=date.today()
    )
    timestamp = mFields.DateTimeField(
        format=DateFormatEnum.FULL_TS.value, default=datetime.now
    )
    meta = deepcopy(BASE_META)
    meta["ordering"] = ["-timestamp"]
    meta["collection"] = MongoConfig.SECURITY_IN_FOCUS
