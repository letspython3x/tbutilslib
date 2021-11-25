"""Trading Dates Schema."""
from datetime import datetime

from marshmallow import Schema, fields
from tbutilslib.config.constants import TB_DATE_FORMAT, FULL_TS_FORMAT


class TradingDatesSchema(Schema):
    """Trading Dates Schema."""

    id = fields.Str(required=False)
    lastTradingDate = fields.Date(TB_DATE_FORMAT)
    currentTradingDate = fields.Date(TB_DATE_FORMAT)
    timestamp = fields.DateTime(FULL_TS_FORMAT, default=datetime.now)


class TradingDatesResponseSchema(Schema):
    """Trading Dates Response Schema."""

    tradingDates = fields.Boolean(default=True)
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(TradingDatesSchema))
