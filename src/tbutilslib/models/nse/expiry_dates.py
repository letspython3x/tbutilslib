"""Expiry Dates Collection."""
from copy import deepcopy

from mongoengine import fields as mongoFields
from tbutilslib.config.constants import TB_DATE_FORMAT, FULL_TS_FORMAT
from tbutilslib.config.database import MongoConfig
from tbutilslib.models.base import BaseCollection, BASE_META


class ExpiryDatesCollection(BaseCollection):
    """Expiry Dates Collection."""

    index = mongoFields.BooleanField(default=False)
    expiryDates = mongoFields.ListField(
        mongoFields.DateField(format=TB_DATE_FORMAT))
    timestamp = mongoFields.DateTimeField(format=FULL_TS_FORMAT)
    meta = deepcopy(BASE_META)
    meta['ordering'] = ["-timestamp"]
    meta['collection'] = MongoConfig.EXPIRY_DATES
