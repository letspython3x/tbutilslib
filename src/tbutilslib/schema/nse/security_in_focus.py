"""Security in Focus Schema."""
from datetime import date, datetime

from marshmallow import Schema, fields, pre_load

from ...utils.dtu import parse_timestamp, str_to_date, change_date_format
from ...utils.enums import DateFormatEnum


class SecurityInFocusSchema(Schema):
    """Security in Focus Schema."""

    id = fields.String(required=False)
    security = fields.String(required=True)
    strike_prices = fields.List(fields.Int)
    is_fno = fields.Bool(default=False)
    on_date = fields.Date(DateFormatEnum.TB_DATE.value, default=date.today())
    expiry_dates = fields.List(fields.Date(format=DateFormatEnum.TB_DATE.value))
    timestamp = fields.DateTime(DateFormatEnum.FULL_TS.value, default=datetime.now)

    @pre_load
    def marshal_fields(self, in_data: dict, **kwargs) -> dict:
        """Marshal the fields."""

        is_nse = in_data.get("is_nse", False)
        if is_nse:
            timestamp: datetime = parse_timestamp(in_data["timestamp"])
            on_date: str = change_date_format(
                timestamp.date(), DateFormatEnum.TB_DATE.value
            )

            if "expiry_dates" in in_data:
                updated_expiry_dates = []
                for exp in in_data["expiry_dates"]:
                    ed = str_to_date(exp, DateFormatEnum.NSE_DATE.value)
                    ed = change_date_format(ed, DateFormatEnum.TB_DATE.value)
                    updated_expiry_dates.append(ed)

            return {
                "security": in_data["security"],
                "strike_prices": in_data["strike_prices"],
                "expiry_dates": updated_expiry_dates,
                "is_fno": in_data.get("is_fno", False),
                "on_date": on_date,
                "timestamp": in_data["timestamp"],
            }

        return in_data


class SecurityInFocusResponseSchema(Schema):
    """Security in Focus Response Schema."""

    security_in_focus = fields.Boolean(default=True)
    total_items = fields.Integer()
    securities = fields.List(fields.String)
    items = fields.List(fields.Nested(SecurityInFocusSchema))
