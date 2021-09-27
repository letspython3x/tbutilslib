"""Derivatives Related Schema."""
from marshmallow import Schema, fields, pre_load
from tbutilslib.config.constants import (TB_DATE_FORMAT,
                                         FULL_TS_FORMAT,
                                         FULL_TS_FORMAT_TZ)
from tbutilslib.utils.common import parse_timestamp


class CumulativeDerivativesSchema(Schema):
    """Cumulative Derivatives Schema."""

    security = fields.Str(required=True)
    spotPrice = fields.Float()
    futurePrice = fields.Float(default=0)
    totOiCe = fields.Float()
    totVolCe = fields.Float()
    totOiPe = fields.Float()
    totVolPe = fields.Float()
    pcrOi = fields.Float()
    pcrVol = fields.Float()
    totalOiFut = fields.Int()
    totalVolFut = fields.Int()
    expiryDate = fields.Date(TB_DATE_FORMAT)
    onDate = fields.Date(TB_DATE_FORMAT)
    timestamp = fields.DateTime(FULL_TS_FORMAT)

    @pre_load
    def slugify_date(self, in_data: dict, **kwargs) -> dict:
        """Set a new key onDate.

        Args:
            in_data: dict
        """
        ts = parse_timestamp(in_data["timestamp"])
        in_data["onDate"] = ts.date().strftime(TB_DATE_FORMAT)
        return in_data


class CumulativeDerivativesResponseSchema(Schema):
    """Cumulative Derivatives Response Schema."""

    cumulative = fields.Boolean(default=True)
    security = fields.Str()
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(CumulativeDerivativesSchema))


class CumulativeRequestSchema(Schema):
    """Cumulative Derivatives Request Schema."""

    security = fields.Str()


class DerivativesSchemaCommonFields(Schema):
    """Derivatives Common Fields."""

    security = fields.Str(required=True)
    identifier = fields.Str()
    optionType = fields.Str()
    lastPrice = fields.Float()
    openInterest = fields.Int()
    impliedVolatility = fields.Float()
    changeinOpenInterest = fields.Int()
    pchangeinOpenInterest = fields.Float()
    change = fields.Float()
    pChange = fields.Float()
    strikePrice = fields.Float()
    instrumentType = fields.Str()
    openPrice = fields.Float()
    highPrice = fields.Float()
    lowPrice = fields.Float()
    closePrice = fields.Float()
    prevClose = fields.Float()
    numberOfContractsTraded = fields.Int()
    totalTurnover = fields.Float()
    tradedVolume = fields.Int()
    value = fields.Float()
    vmap = fields.Float()
    premiumTurnover = fields.Float()
    marketLot = fields.Int()
    settlementPrice = fields.Float()
    dailyvolatility = fields.Float()
    annualisedVolatility = fields.Float()
    clientWisePositionLimits = fields.Int()
    marketWidePositionLimits = fields.Int()
    spotPrice = fields.Float()
    expiryDate = fields.Date(TB_DATE_FORMAT)
    onDate = fields.Date(TB_DATE_FORMAT)
    timestamp = fields.DateTime(FULL_TS_FORMAT)

    @pre_load
    def slugify_date(self, in_data: dict, **kwargs) -> dict:
        """Set a new key onDate.

        Args:
            in_data: dict
        """
        ts = parse_timestamp(in_data["timestamp"])
        in_data["onDate"] = ts.date().strftime(TB_DATE_FORMAT)
        return in_data


class DerivativesSchemaResponseCommonFields(Schema):
    """Derivatives Response Schema."""

    derivatives = fields.Boolean(default=True)
    security = fields.Str()
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Integer()


class IndexDerivativesSchema(DerivativesSchemaCommonFields):
    """Index Derivatives Schema."""

    pass


class EquityDerivativesSchema(DerivativesSchemaCommonFields):
    """Equity Derivatives Schema."""

    pass


class IndexDerivativesResponseSchema(DerivativesSchemaResponseCommonFields):
    """Index Derivatives Response Schema."""

    items = fields.List(fields.Nested(IndexDerivativesSchema))


class EquityDerivativesResponseSchema(DerivativesSchemaResponseCommonFields):
    """Equity Derivatives Response Schema."""

    items = fields.List(fields.Nested(EquityDerivativesSchema))


class IndexRequestSchema(Schema):
    """Index Derivatives Request Schema."""

    security = fields.Str(required=True)


class EquityRequestSchema(Schema):
    """Equity Derivatives Request Schema."""

    security = fields.Str(required=True)


class HistoricalDerivativesSchema(Schema):
    """Historical Derivatives Schema."""

    security = fields.Str(required=True)
    instrument = fields.Str()
    marketType = fields.Str()
    marketLot = fields.Int()
    optionType = fields.Str()
    strikePrice = fields.Float()
    openPrice = fields.Float()
    closePrice = fields.Float()
    highPrice = fields.Float()
    lowPrice = fields.Float()
    lastPrice = fields.Float()
    settlePrice = fields.Float()
    prevClosePrice = fields.Float()
    tradedVolume = fields.Int()
    tradedValue = fields.Int()
    premiumValue = fields.Float()
    openInterest = fields.Int()
    changeInOI = fields.Int()
    onDate = fields.Date(format=TB_DATE_FORMAT)
    expiryDate = fields.Date(format=TB_DATE_FORMAT)
    timestamp = fields.DateTime(format=FULL_TS_FORMAT_TZ)
    positionType = fields.Str()


class HistoricalDerivativesResponseSchema(Schema):
    """Historical Derivatives Response Schema."""

    derivatives = fields.Boolean(default=True)
    security = fields.Str()
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(HistoricalDerivativesSchema))


class ExpiryDatesResponseSchema(Schema):
    """Expiry Dates Schema."""

    expiryDates = fields.Boolean(default=True)
    security = fields.Str()
    totalItems = fields.Integer()
    possibleKeys = fields.List(fields.Str())
    items = fields.List(fields.Date(format=TB_DATE_FORMAT))
