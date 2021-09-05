from app.utils.constants import DATE_FORMAT
from copy import deepcopy

from mongoengine import fields as mongoFields

from app.config import MongoConfig
from app.models.base import BaseCollection, BASE_META
from app.utils.common import not_empty


class EventsCalendarCollection(BaseCollection):
    """EVENTS_CALENDAR collection."""
    index = mongoFields.StringField()
    security = mongoFields.StringField(validation=not_empty)
    company = mongoFields.StringField()
    purpose = mongoFields.StringField()
    description = mongoFields.StringField()
    eventDate = mongoFields.DateField(format=DATE_FORMAT)
    fno = mongoFields.BooleanField()
    meta = deepcopy(BASE_META)
    meta['ordering'] = ["-eventDate"]
    meta = {'collection': MongoConfig.EVENTS_CALENDAR}
