"""Equity Related Schema."""
from marshmallow import Schema, fields, pre_load
from tbutilslib.config.constants import (FULL_TS_FORMAT,
                                         NSE_DATE_FORMAT,
                                         TB_DATE_FORMAT)
from tbutilslib.utils.common import parse_timestamp, str_to_date


class EquitySchema(Schema):
    """Equity Schema."""

    id = fields.Str(required=False)
    security = fields.Str()
    isFNOSec = fields.Bool()
    lastPrice = fields.Float()
    identifier = fields.Str()
    series = fields.Str()
    open = fields.Float()
    dayHigh = fields.Float()
    dayLow = fields.Float()
    previousClose = fields.Float()
    change = fields.Float()
    pChange = fields.Float()
    totalTradedVolume = fields.Int()
    totalTradedValue = fields.Float()
    yearHigh = fields.Float()
    yearLow = fields.Float()
    nearWKH = fields.Float()
    nearWKL = fields.Float()
    perChange365d = fields.Float()
    date30dAgo = fields.Date(format=TB_DATE_FORMAT)
    perChange30d = fields.Float()
    chart30dPath = fields.Str()
    chartTodayPath = fields.Str()
    timestamp = fields.DateTime(FULL_TS_FORMAT)
    onDate = fields.Date(format=TB_DATE_FORMAT)
    lastUpdateTime = fields.DateTime(FULL_TS_FORMAT)

    @pre_load
    def slugify_date(self, in_data: dict, **kwargs) -> dict:
        """Set a new key onDate and update date format for date30dAgo.

        Args:
            in_data: dict
        """
        ts = parse_timestamp(in_data["timestamp"])
        in_data["onDate"] = ts.date().strftime(TB_DATE_FORMAT)
        date30dAgo = str_to_date(in_data['date30dAgo'], NSE_DATE_FORMAT)
        in_data["date30dAgo"] = date30dAgo.strftime(TB_DATE_FORMAT)
        return in_data


class EquityResponseSchema(Schema):
    """Equity Response Schema."""

    equity = fields.Boolean(default=True)
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(EquitySchema))


class EquityRequestSchema(Schema):
    """Equity Request Schema."""

    security = fields.Str()


class AdvanceDeclineSchema(Schema):
    """Advance Decline Schema."""

    id = fields.Str(required=False)
    advances = fields.Int()
    declines = fields.Int()
    unchanged = fields.Int()
    timestamp = fields.DateTime(FULL_TS_FORMAT)
    onDate = fields.Date(TB_DATE_FORMAT)

    @pre_load
    def slugify_date(self, in_data: dict, **kwargs) -> dict:
        """Set a new key onDate.

        Args:
            in_data: dict
        """
        ts = parse_timestamp(in_data["timestamp"])
        in_data["onDate"] = ts.date().strftime(TB_DATE_FORMAT)
        return in_data


class AdvanceDeclineResponseSchema(Schema):
    """Advance Decline Response Schema."""

    advanceDecline = fields.Boolean(default=True)
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(AdvanceDeclineSchema))
