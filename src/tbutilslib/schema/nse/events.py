"""Events Schema."""
from marshmallow import Schema, fields, pre_load
from tbutilslib.config.constants import TB_DATE_FORMAT, NSE_DATE_FORMAT
from tbutilslib.utils.common import str_to_date


class EventsSchema(Schema):
    """Events Schema."""

    security = fields.Str(required=True)
    eventDate = fields.Date(required=True, format=TB_DATE_FORMAT)
    index = fields.Str(required=False, default="equities")
    company = fields.Str()
    purpose = fields.Str()
    description = fields.Str()
    fno = fields.Bool(default=False)

    @pre_load
    def slugify_date(self, in_data: dict, **kwargs) -> dict:
        """Update format for eventDate.

        Args:
            in_data: dict
        """
        eventDate = str_to_date(in_data['eventDate'], NSE_DATE_FORMAT)
        in_data["eventDate"] = eventDate.strftime(TB_DATE_FORMAT)
        return in_data


class EventsResponseSchema(Schema):
    """Events Response Schema."""

    events = fields.Boolean(default=True)
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Int()
    items = fields.List(fields.Nested(EventsSchema))


class EventsRequestSchema(Schema):
    """Events Request Schema."""

    security = fields.Str()
