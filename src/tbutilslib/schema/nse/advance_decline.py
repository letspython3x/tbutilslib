from marshmallow import Schema, fields, pre_load

from app.utils.common import parse_timestamp
from app.utils.constants import (DATE_FORMAT, FULL_TS_FORMAT)


class AdvanceDeclineSchema(Schema):
    advances = fields.Int()
    declines = fields.Int()
    unchanged = fields.Int()
    timestamp = fields.DateTime(FULL_TS_FORMAT)
    onDate = fields.Date(DATE_FORMAT)

    @pre_load
    def slugify_date(self, in_data, **kwargs):
        ts = parse_timestamp(in_data["timestamp"])
        in_data["onDate"] = ts.date().strftime(DATE_FORMAT)
        return in_data


class AdvanceDeclineResponseSchema(Schema):
    advanceDecline = fields.Boolean(default=True)
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(AdvanceDeclineSchema))
