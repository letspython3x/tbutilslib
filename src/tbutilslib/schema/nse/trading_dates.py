"""Trading Dates Schema."""
from datetime import datetime

from marshmallow import Schema, fields

from ...utils.enums import DateFormatEnum


class TradingDatesSchema(Schema):
    """Trading Dates Schema."""

    id = fields.String(required=False)
    last_trading_date = fields.Date(DateFormatEnum.TB_DATE.value)
    current_trading_date = fields.Date(DateFormatEnum.TB_DATE.value)
    timestamp = fields.DateTime(DateFormatEnum.FULL_TS.value, default=datetime.now)


class TradingDatesResponseSchema(Schema):
    """Trading Dates Response Schema."""

    trading_dates = fields.Boolean(default=True)
    possible_keys = fields.List(fields.String())
    total_items = fields.Integer()
    items = fields.List(fields.Nested(TradingDatesSchema))
