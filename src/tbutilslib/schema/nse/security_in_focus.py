"""Security in Focus Schema."""
from datetime import date, datetime

from marshmallow import Schema, fields, pre_load

from ...utils.dtu import parse_timestamp
from ...utils.enums import DateFormatEnum


class SecurityInFocusSchema(Schema):
    """Security in Focus Schema."""

    id = fields.String(required=False)
    security = fields.String(required=True)
    strike_prices = fields.List(fields.Int)
    is_fno = fields.Bool(default=False)
    on_date = fields.Date(DateFormatEnum.TB_DATE.value, default=date.today())
    timestamp = fields.DateTime(DateFormatEnum.FULL_TS.value, default=datetime.now)

    @pre_load
    def slugify_date(self, in_data: dict, **kwargs) -> dict:
        """Set a new key on_date.

        Args:
            in_data: dict
        """
        if "timestamp" in in_data:
            ts = parse_timestamp(in_data["timestamp"])
            in_data["on_date"] = ts.date().strftime(DateFormatEnum.TB_DATE.value)
        return in_data


class SecurityInFocusResponseSchema(Schema):
    """Security in Focus Response Schema."""

    security_in_focus = fields.Boolean(default=True)
    total_items = fields.Integer()
    securities = fields.List(fields.String)
    items = fields.List(fields.Nested(SecurityInFocusSchema))
