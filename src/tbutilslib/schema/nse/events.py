from marshmallow import Schema, fields, pre_load

from app.utils.common import str_to_date
from app.utils.constants import DATE_FORMAT, NSE_DATE_FORMAT


class EventsSchema(Schema):
    index = fields.Str(default="equities")
    security = fields.Str()
    company = fields.Str()
    purpose = fields.Str()
    description = fields.Str()
    eventDate = fields.Date(format=DATE_FORMAT)
    fno = fields.Bool(default=False)

    @pre_load
    def slugify_date(self, in_data, **kwargs):
        eventDate = str_to_date(in_data['eventDate'], NSE_DATE_FORMAT)
        in_data["eventDate"] = eventDate.strftime(DATE_FORMAT)
        return in_data


class EventsResponseSchema(Schema):
    events = fields.Boolean(default=True)
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Int()
    items = fields.List(fields.Nested(EventsSchema))


class EventsRequestSchema(Schema):
    security = fields.Str()
