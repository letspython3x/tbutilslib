"""Event collection."""
from copy import deepcopy

from mongoengine import fields as mongoFields
from tbutilslib.config.constants import TB_DATE_FORMAT
from tbutilslib.config.database import MongoConfig
from tbutilslib.models.base import BaseCollection, BASE_META


class EventsCollection(BaseCollection):
    """EVENTS collection."""

    index = mongoFields.StringField(default="equities")
    security = mongoFields.StringField(required=True)
    company = mongoFields.StringField()
    purpose = mongoFields.StringField()
    description = mongoFields.StringField()
    eventDate = mongoFields.DateField(required=True, format=TB_DATE_FORMAT)
    fno = mongoFields.BooleanField()
    meta = deepcopy(BASE_META)
    meta['ordering'] = ["-eventDate"]
    meta = {'collection': MongoConfig.EVENTS}
