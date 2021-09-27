"""Derivatives Related Collection."""
from copy import deepcopy

from mongoengine import fields as mongoFields
from tbutilslib.config.constants import (FULL_TS_FORMAT,
                                         TB_DATE_FORMAT,
                                         FULL_TS_FORMAT_TZ)
from tbutilslib.config.database import MongoConfig
from tbutilslib.models.base import BaseCollection, BASE_META


class CumulativeDerivativesCollection(BaseCollection):
    """CUMULATIVE_DERIVATIVES collection."""

    security = mongoFields.StringField(required=True)
    spotPrice = mongoFields.FloatField()
    futurePrice = mongoFields.FloatField(default=0)
    totOiCe = mongoFields.FloatField()
    totVolCe = mongoFields.FloatField()
    totOiPe = mongoFields.FloatField()
    totVolPe = mongoFields.FloatField()
    pcrOi = mongoFields.FloatField()
    pcrVol = mongoFields.FloatField()
    totalOiFut = mongoFields.IntField()
    totalVolFut = mongoFields.IntField()
    timestamp = mongoFields.DateTimeField(format=FULL_TS_FORMAT)
    onDate = mongoFields.DateField(format=TB_DATE_FORMAT)
    expiryDate = mongoFields.DateField(format=TB_DATE_FORMAT)
    meta = deepcopy(BASE_META)
    meta['ordering'] = ["-timestamp"]
    meta['collection'] = MongoConfig.CUMULATIVE_DERIVATIVES


class DerivativesCommonFields:
    """Derivatives Common Fields for collection."""

    security = mongoFields.StringField(required=True)
    identifier = mongoFields.StringField(required=True)
    optionType = mongoFields.StringField()
    lastPrice = mongoFields.FloatField()
    openInterest = mongoFields.IntField()
    impliedVolatility = mongoFields.FloatField()
    changeinOpenInterest = mongoFields.IntField()
    pchangeinOpenInterest = mongoFields.FloatField()
    change = mongoFields.FloatField()
    pChange = mongoFields.FloatField()
    strikePrice = mongoFields.FloatField()
    instrumentType = mongoFields.StringField()
    openPrice = mongoFields.FloatField()
    highPrice = mongoFields.FloatField()
    lowPrice = mongoFields.FloatField()
    closePrice = mongoFields.FloatField()
    prevClose = mongoFields.FloatField()
    numberOfContractsTraded = mongoFields.IntField()
    totalTurnover = mongoFields.FloatField()
    tradedVolume = mongoFields.IntField()
    value = mongoFields.FloatField()
    vmap = mongoFields.FloatField()
    premiumTurnover = mongoFields.FloatField()
    marketLot = mongoFields.IntField()
    settlementPrice = mongoFields.FloatField()
    dailyvolatility = mongoFields.FloatField()
    annualisedVolatility = mongoFields.FloatField()
    clientWisePositionLimits = mongoFields.IntField()
    marketWidePositionLimits = mongoFields.IntField()
    spotPrice = mongoFields.FloatField()
    expiryDate = mongoFields.DateField(format=TB_DATE_FORMAT)
    onDate = mongoFields.DateField(format=TB_DATE_FORMAT)
    timestamp = mongoFields.DateTimeField(format=FULL_TS_FORMAT)


class IndexDerivativesCollection(BaseCollection, DerivativesCommonFields):
    """INDEX_DERIVATIVES collection."""

    meta = deepcopy(BASE_META)
    meta['ordering'] = ["-timestamp"]
    meta['collection'] = MongoConfig.INDEX_DERIVATIVES


class EquityDerivatesCollection(BaseCollection, DerivativesCommonFields):
    """EQUITY_DERIVATIVES collection."""

    meta = deepcopy(BASE_META)
    meta['ordering'] = ["-timestamp"]
    meta['collection'] = MongoConfig.EQUITY_DERIVATIVES


class HistoricalDerivatesCollection(BaseCollection):
    """HISTORICAL_DERIVATIVES collection."""

    security = mongoFields.StringField(required=True)
    instrument = mongoFields.StringField()
    marketType = mongoFields.StringField()
    marketLot = mongoFields.IntField()
    optionType = mongoFields.StringField()
    strikePrice = mongoFields.FloatField()
    openPrice = mongoFields.FloatField()
    closePrice = mongoFields.FloatField()
    highPrice = mongoFields.FloatField()
    lowPrice = mongoFields.FloatField()
    lastPrice = mongoFields.FloatField()
    settlePrice = mongoFields.FloatField()
    prevClosePrice = mongoFields.FloatField()
    tradedVolume = mongoFields.IntField()
    tradedValue = mongoFields.IntField()
    premiumValue = mongoFields.FloatField()
    openInterest = mongoFields.IntField()
    changeInOI = mongoFields.IntField()
    onDate = mongoFields.DateField(format=TB_DATE_FORMAT)
    expiryDate = mongoFields.DateField(format=TB_DATE_FORMAT)
    timestamp = mongoFields.DateTimeField(format=FULL_TS_FORMAT_TZ)
    positionType = mongoFields.StringField()
    meta = deepcopy(BASE_META)
    meta['ordering'] = ["-timestamp"]
    meta['collection'] = MongoConfig.HISTORICAL_DERIVATIVES
