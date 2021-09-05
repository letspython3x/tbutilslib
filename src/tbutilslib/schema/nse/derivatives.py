from marshmallow import Schema, fields, pre_load

from app.utils.common import parse_timestamp
from app.utils.constants import (DATE_FORMAT,
                                 NSE_DATE_FORMAT,
                                 FULL_TS_FORMAT,
                                 FULL_TS_FORMAT_TZ)


class CumulativeDerivativesSchema(Schema):
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
    expiryDate = fields.Date(DATE_FORMAT)
    onDate = fields.Date(DATE_FORMAT)
    timestamp = fields.DateTime(FULL_TS_FORMAT)

    @pre_load
    def slugify_date(self, in_data, **kwargs):
        ts = parse_timestamp(in_data["timestamp"])
        in_data["onDate"] = ts.date().strftime(DATE_FORMAT)
        return in_data


class CumulativeDerivativesResponseSchema(Schema):
    cumulative = fields.Boolean(default=True)
    security = fields.Str()
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(CumulativeDerivativesSchema))


class CumulativeRequestSchema(Schema):
    security = fields.Str()


class DerivativesSchemaCommonFields(Schema):
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
    expiryDate = fields.Date(DATE_FORMAT)
    onDate = fields.Date(DATE_FORMAT)
    timestamp = fields.DateTime(FULL_TS_FORMAT)

    @pre_load
    def slugify_date(self, in_data, **kwargs):
        ts = parse_timestamp(in_data["timestamp"])
        in_data["onDate"] = ts.date().strftime(DATE_FORMAT)
        return in_data


class DerivativesSchemaResponseCommonFields(Schema):
    derivatives = fields.Boolean(default=True)
    security = fields.Str()
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Integer()


class IndexDerivativesSchema(DerivativesSchemaCommonFields):
    pass


class EquityDerivativesSchema(DerivativesSchemaCommonFields):
    pass


class IndexDerivativesResponseSchema(DerivativesSchemaResponseCommonFields):
    items = fields.List(fields.Nested(IndexDerivativesSchema))


class EquityDerivativesResponseSchema(DerivativesSchemaResponseCommonFields):
    items = fields.List(fields.Nested(EquityDerivativesSchema))


class IndexRequestSchema(Schema):
    security = fields.Str(required=True)


class EquityRequestSchema(Schema):
    security = fields.Str(required=True)


class HistoricalDerivativesSchema(Schema):
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
    onDate = fields.Date(format=NSE_DATE_FORMAT)
    expiryDate = fields.Date(format=NSE_DATE_FORMAT)
    timestamp = fields.DateTime(format=FULL_TS_FORMAT_TZ)


class HistoricalDerivativesResponseSchema(Schema):
    derivatives = fields.Boolean(default=True)
    security = fields.Str()
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(HistoricalDerivativesSchema))
