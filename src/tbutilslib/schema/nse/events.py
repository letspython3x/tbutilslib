"""Events Schema."""
from marshmallow import Schema, fields, pre_load
from tbutilslib.config.constants import TB_DATE_FORMAT, NSE_DATE_FORMAT
from tbutilslib.utils.common import str_to_date


class EventsSchema(Schema):
    """Events Schema."""

    id = fields.String(required=False)
    security = fields.String(required=True)
    eventDate = fields.Date(required=True, format=TB_DATE_FORMAT)
    index = fields.String(required=False, default="equities")
    company = fields.String()
    purpose = fields.String()
    description = fields.String()
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
    possibleKeys = fields.List(fields.String())
    totalItems = fields.Int()
    items = fields.List(fields.Nested(EventsSchema))


class EventsRequestSchema(Schema):
    """Events Request Schema."""

    security = fields.String()
