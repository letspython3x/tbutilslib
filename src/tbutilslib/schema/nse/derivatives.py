"""Derivatives Related Schema."""
from marshmallow import Schema, fields, pre_load
from tbutilslib.config.constants import (TB_DATE_FORMAT,
                                         FULL_TS_FORMAT,
                                         FULL_TS_FORMAT_TZ)
from tbutilslib.utils.common import parse_timestamp, validate_quantity


class CumulativeDerivativesSchema(Schema):
    """Cumulative Derivatives Schema."""

    id = fields.String(required=False)
    security = fields.String(required=True)
    spotPrice = fields.Float(validate=validate_quantity)
    futurePrice = fields.Float(validate=validate_quantity)
    totOiCe = fields.Float(validate=validate_quantity)
    totVolCe = fields.Float(validate=validate_quantity)
    totOiPe = fields.Float(validate=validate_quantity)
    totVolPe = fields.Float(validate=validate_quantity)
    pcrOi = fields.Float(validate=validate_quantity)
    pcrVol = fields.Float(validate=validate_quantity)
    totalOiFut = fields.Integer(validate=validate_quantity)
    totalVolFut = fields.Integer(validate=validate_quantity)
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
    security = fields.String()
    possibleKeys = fields.List(fields.String())
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(CumulativeDerivativesSchema))


class CumulativeRequestSchema(Schema):
    """Cumulative Derivatives Request Schema."""

    security = fields.String()


class DerivativesSchemaCommonFields(Schema):
    """Derivatives Common Fields."""

    id = fields.String(required=False)
    security = fields.String(required=True)
    identifier = fields.String()
    optionType = fields.String()
    lastPrice = fields.Float()
    openInterest = fields.Integer(validate=validate_quantity)
    impliedVolatility = fields.Float()
    changeinOpenInterest = fields.Integer()
    pchangeinOpenInterest = fields.Float()
    change = fields.Float()
    pChange = fields.Float()
    strikePrice = fields.Float()
    instrumentType = fields.String()
    openPrice = fields.Float()
    highPrice = fields.Float()
    lowPrice = fields.Float()
    closePrice = fields.Float()
    prevClose = fields.Float()
    numberOfContractsTraded = fields.Integer()
    totalTurnover = fields.Float()
    tradedVolume = fields.Integer(validate=validate_quantity)
    value = fields.Float(validate=validate_quantity)
    vmap = fields.Float()
    premiumTurnover = fields.Float()
    marketLot = fields.Integer(validate=validate_quantity)
    settlementPrice = fields.Float()
    dailyvolatility = fields.Float()
    annualisedVolatility = fields.Float()
    clientWisePositionLimits = fields.Integer()
    marketWidePositionLimits = fields.Integer()
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
    security = fields.String()
    possibleKeys = fields.List(fields.String())
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

    security = fields.String(required=True)


class EquityRequestSchema(Schema):
    """Equity Derivatives Request Schema."""

    security = fields.String(required=True)


class HistoricalDerivativesSchema(Schema):
    """Historical Derivatives Schema."""

    id = fields.String(required=False)
    security = fields.String(required=True)
    instrument = fields.String()
    marketType = fields.String()
    marketLot = fields.Integer(validate=validate_quantity)
    optionType = fields.String()
    strikePrice = fields.Float()
    openPrice = fields.Float()
    closePrice = fields.Float()
    highPrice = fields.Float()
    lowPrice = fields.Float()
    lastPrice = fields.Float()
    settlePrice = fields.Float()
    prevClosePrice = fields.Float()
    tradedVolume = fields.Integer()
    tradedValue = fields.Integer()
    premiumValue = fields.Float()
    openInterest = fields.Integer()
    changeInOI = fields.Integer()
    onDate = fields.Date(format=TB_DATE_FORMAT)
    expiryDate = fields.Date(format=TB_DATE_FORMAT)
    timestamp = fields.DateTime(format=FULL_TS_FORMAT_TZ)
    positionType = fields.String()

    @pre_load
    def slugify_data(self, in_data: dict, **kwargs) -> dict:
        """Set a new key onDate.

        Args:
            in_data: dict
        """
        marketLot = in_data["marketLot"]
        if marketLot and marketLot != 0:
            in_data["changeInOI"] = int(in_data["changeInOI"] / marketLot)
            in_data["openInterest"] = int(in_data["openInterest"] / marketLot)
        return in_data


class HistoricalDerivativesResponseSchema(Schema):
    """Historical Derivatives Response Schema."""

    derivatives = fields.Boolean(default=True)
    security = fields.String()
    possibleKeys = fields.List(fields.String())
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(HistoricalDerivativesSchema))


class ExpiryDatesResponseSchema(Schema):
    """Expiry Dates Schema."""

    expiryDates = fields.Boolean(default=True)
    security = fields.String()
    totalItems = fields.Integer()
    possibleKeys = fields.List(fields.String())
    items = fields.List(fields.Date(format=TB_DATE_FORMAT))
