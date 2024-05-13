"""Expiry Dates Collection."""
from copy import deepcopy

from mongoengine import fields as mongoFields

from ..base import BaseCollection, BASE_META
from ...config import MongoConfig
from ...utils.enums import DateFormatEnum


class ExpiryDatesCollection(BaseCollection):
    """Expiry Dates Collection."""

    security_type = mongoFields.StringField(required=True)
    expiry_dates = mongoFields.ListField(
        mongoFields.DateField(format=DateFormatEnum.TB_DATE.value)
    )
    timestamp = mongoFields.DateTimeField(format=DateFormatEnum.FULL_TS.value)
    meta = deepcopy(BASE_META)
    meta["ordering"] = ["-timestamp"]
    meta["collection"] = MongoConfig.EXPIRY_DATES
