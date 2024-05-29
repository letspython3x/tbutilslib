"""Equity Related Schema."""
from datetime import datetime, date

from marshmallow import Schema, fields, pre_load

from ...utils.common import validate_quantity
from ...utils.dtu import (
    parse_timestamp,
    str_to_date,
    change_date_format,
    parse_timestamp_to_str,
)
from ...utils.enums import DateFormatEnum


class IndexSchema(Schema):
    """Index Schema."""

    id = fields.String(required=False)
    security = fields.String()
    identifier = fields.String()
    open = fields.Float()
    day_high = fields.Float()
    day_low = fields.Float()
    last_price = fields.Float()
    previous_close = fields.Float()
    change = fields.Float()
    p_change = fields.Float()
    ffmc = fields.Float()
    year_high = fields.Float()
    year_low = fields.Float()
    total_traded_volume = fields.Integer(validate=validate_quantity, default=0)
    total_traded_value = fields.Float()
    near_weak_high = fields.Float()
    near_weak_low = fields.Float()
    per_change_30d = fields.Float()
    per_change_365d = fields.Float()
    chart_30d_path = fields.String()
    chart_today_path = fields.String()
    chart_365d_path = fields.String()
    date_30d_ago = fields.Date(format=DateFormatEnum.TB_DATE.value)
    date_365d_ago = fields.Date(format=DateFormatEnum.TB_DATE.value)
    timestamp = fields.DateTime(DateFormatEnum.FULL_TS.value)
    last_update_time = fields.DateTime(DateFormatEnum.FULL_TS.value)
    on_date = fields.Date(format=DateFormatEnum.TB_DATE.value)

    @pre_load
    def marshal_fields(self, in_data: dict, **kwargs) -> dict:
        """Set a new key on_date and update date format for date30dAgo.

        Args:
            in_data: dict
        """
        is_nse = in_data.get("is_nse", False)
        if is_nse:
            timestamp: datetime = parse_timestamp(in_data["timestamp"])
            last_update_time: datetime = parse_timestamp(in_data["lastUpdateTime"])

            on_date: str = change_date_format(
                timestamp.date(), DateFormatEnum.TB_DATE.value
            )

            date_30d_ago: date = str_to_date(
                in_data["date30dAgo"], DateFormatEnum.NSE_DATE.value
            )
            date_30d_ago: str = change_date_format(
                date_30d_ago, DateFormatEnum.TB_DATE.value
            )

            date_365d_ago: date = str_to_date(
                in_data["date365dAgo"], DateFormatEnum.NSE_DATE.value
            )
            date_365d_ago: str = change_date_format(
                date_365d_ago, DateFormatEnum.TB_DATE.value
            )

            return {
                "security": in_data["symbol"],
                "identifier": in_data["identifier"],
                "open": in_data["open"],
                "day_high": in_data["dayHigh"],
                "day_low": in_data["dayLow"],
                "last_price": in_data["lastPrice"],
                "previous_close": in_data["previousClose"],
                "change": in_data["change"],
                "p_change": in_data["pChange"],
                "ffmc": in_data["ffmc"],
                "year_high": in_data["yearHigh"],
                "year_low": in_data["yearLow"],
                "total_traded_volume": in_data["totalTradedVolume"],
                "total_traded_value": in_data["totalTradedValue"],
                "near_weak_high": in_data["nearWKH"],
                "near_weak_low": in_data["nearWKL"],
                "per_change_30d": in_data["perChange30d"],
                "per_change_365d": in_data["perChange365d"],
                "chart_30d_path": in_data["chart30dPath"],
                "chart_today_path": in_data["chartTodayPath"],
                "chart_365d_path": in_data["chart365dPath"],
                "date_30d_ago": date_30d_ago,
                "date_365d_ago": date_365d_ago,
                "timestamp": parse_timestamp_to_str(
                    timestamp, DateFormatEnum.FULL_TS.value
                ),
                "last_update_time": parse_timestamp_to_str(
                    last_update_time, DateFormatEnum.FULL_TS.value
                ),
                "on_date": on_date,
            }

        return in_data


class IndexResponseSchema(Schema):
    """Index Response Schema."""

    index = fields.Boolean(default=True)
    possible_keys = fields.List(fields.String())
    total_items = fields.Integer()
    items = fields.List(fields.Nested(IndexSchema))


class IndexRequestSchema(Schema):
    """Index Request Schema."""

    security = fields.String()
