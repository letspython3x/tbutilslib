from app.utils.constants import FULL_TS_FORMAT, DATE_FORMAT
from copy import deepcopy

from mongoengine import fields as mongoFields

from app.config import MongoConfig
from app.models.base import BaseCollection, BASE_META


class AdvanceDeclineCollection(BaseCollection):
    """ADVANCE_DECLINE collection."""
    declines = mongoFields.IntField()
    advances = mongoFields.IntField()
    unchanged = mongoFields.IntField()
    onDate = mongoFields.DateField(format=DATE_FORMAT)
    timestamp = mongoFields.DateTimeField(format=FULL_TS_FORMAT)
    meta = deepcopy(BASE_META)
    meta['ordering'] = ["-timestamp"]
    meta['collection'] = MongoConfig.ADVANCE_DECLINE
