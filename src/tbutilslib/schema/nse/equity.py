"""Equity Related Schema."""
from marshmallow import Schema, fields, pre_load

from ...utils.common import validate_quantity
from ...utils.dtu import parse_timestamp, str_to_date
from ...utils.enums import DateFormatEnum


class EquitySchema(Schema):
    """Equity Schema."""

    id = fields.String(required=False)
    security = fields.String()
    is_fno = fields.Bool()
    last_price = fields.Float()
    identifier = fields.String()
    series = fields.String()
    open = fields.Float()
    day_high = fields.Float()
    day_low = fields.Float()
    previous_close = fields.Float()
    change = fields.Float()
    p_change = fields.Float()
    total_traded_volume = fields.Integer(validate=validate_quantity)
    total_traded_value = fields.Float()
    year_high = fields.Float()
    year_low = fields.Float()
    near_weak_high = fields.Float()
    near_weak_low = fields.Float()
    per_change_365d = fields.Float()
    date_30d_ago = fields.Date(format=DateFormatEnum.TB_DATE.value)
    per_change_30d = fields.Float()
    chart_30d_path = fields.String()
    chart_today_path = fields.String()
    timestamp = fields.DateTime(DateFormatEnum.FULL_TS.value)
    on_date = fields.Date(format=DateFormatEnum.TB_DATE.value)
    last_update_time = fields.DateTime(DateFormatEnum.FULL_TS.value)

    @pre_load
    def slugify_date(self, in_data: dict, **kwargs) -> dict:
        """Set a new key on_date and update date format for date30dAgo.

        Args:
            in_data: dict
        """
        ts = parse_timestamp(in_data["timestamp"])
        in_data["on_date"] = ts.date().strftime(DateFormatEnum.TB_DATE.value)
        date_30d_ago = str_to_date(in_data["date30dAgo"], DateFormatEnum.NSE_DATE.value)
        in_data["date_30d_ago"] = date_30d_ago.strftime(DateFormatEnum.TB_DATE.value)
        return in_data


class EquityResponseSchema(Schema):
    """Equity Response Schema."""

    equity = fields.Boolean(default=True)
    possible_keys = fields.List(fields.String())
    total_items = fields.Integer()
    items = fields.List(fields.Nested(EquitySchema))


class EquityRequestSchema(Schema):
    """Equity Request Schema."""

    security = fields.String()


class AdvanceDeclineSchema(Schema):
    """Advance Decline Schema."""

    id = fields.String(required=False)
    advances = fields.Integer()
    declines = fields.Integer()
    unchanged = fields.Integer()
    timestamp = fields.DateTime(DateFormatEnum.FULL_TS.value)
    on_date = fields.Date(DateFormatEnum.TB_DATE.value)

    @pre_load
    def slugify_date(self, in_data: dict, **kwargs) -> dict:
        """Set a new key on_date.

        Args:
            in_data: dict
        """
        ts = parse_timestamp(in_data["timestamp"])
        in_data["on_date"] = ts.date().strftime(DateFormatEnum.TB_DATE.value)
        return in_data


class AdvanceDeclineResponseSchema(Schema):
    """Advance Decline Response Schema."""

    advance_decline = fields.Boolean(default=True)
    total_items = fields.Integer()
    items = fields.List(fields.Nested(AdvanceDeclineSchema))
