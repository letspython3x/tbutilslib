"""Event collection."""
from copy import deepcopy

from mongoengine import fields as mongoFields

from ..base import BaseCollection, BASE_META
from ...config import MongoConfig
from ...utils.enums import DateFormatEnum


class EventsCollection(BaseCollection):
    """EVENTS collection."""

    index = mongoFields.StringField(default="equities")
    security = mongoFields.StringField(required=True)
    company = mongoFields.StringField()
    purpose = mongoFields.StringField()
    description = mongoFields.StringField()
    event_date = mongoFields.DateField(
        required=True, format=DateFormatEnum.TB_DATE.value
    )
    meta = deepcopy(BASE_META)
    meta["ordering"] = ["-event_date"]
    meta = {"collection": MongoConfig.EVENTS}
