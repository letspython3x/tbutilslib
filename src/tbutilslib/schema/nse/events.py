"""Events Schema."""
from marshmallow import Schema, fields, pre_load

from ...utils.dtu import change_date_format, str_to_date
from ...utils.enums import DateFormatEnum


class EventsSchema(Schema):
    """Events Schema."""

    id = fields.String(required=False)
    company = fields.String()
    description = fields.String()
    event_date = fields.Date(required=True, format=DateFormatEnum.TB_DATE.value)
    index = fields.String(required=False, default="equities")
    purpose = fields.String()
    security = fields.String(required=True)

    @pre_load
    def marshal_nse(self, in_data: dict, **kwargs) -> dict:
        is_nse = in_data.get("is_nse", False)
        if is_nse:
            event_date = str_to_date(in_data["date"], DateFormatEnum.NSE_DATE.value)
            event_date = change_date_format(event_date, DateFormatEnum.TB_DATE.value)

            return {
                "security": in_data["symbol"],
                "event_date": event_date,
                "company": in_data["company"],
                "purpose": in_data["purpose"],
                "description": in_data["bm_desc"],
            }

        return in_data


class EventsResponseSchema(Schema):
    """Events Response Schema."""

    events = fields.Boolean(default=True)
    possible_keys = fields.List(fields.String())
    total_items = fields.Int()
    items = fields.List(fields.Nested(EventsSchema))


class EventsRequestSchema(Schema):
    """Events Request Schema."""

    security = fields.String()
