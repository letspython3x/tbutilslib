from marshmallow import Schema, fields, pre_load

from app.utils.common import parse_timestamp, str_to_date
from app.utils.constants import FULL_TS_FORMAT, NSE_DATE_FORMAT, DATE_FORMAT


class EquitySchema(Schema):
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
    date30dAgo = fields.Date(format=DATE_FORMAT)
    perChange30d = fields.Float()
    chart30dPath = fields.Str()
    chartTodayPath = fields.Str()
    timestamp = fields.DateTime(FULL_TS_FORMAT)
    onDate = fields.Date(format=DATE_FORMAT)
    lastUpdateTime = fields.DateTime(FULL_TS_FORMAT)

    @pre_load
    def slugify_date(self, in_data, **kwargs):
        ts = parse_timestamp(in_data["timestamp"])
        in_data["onDate"] = ts.date().strftime(DATE_FORMAT)
        date30dAgo = str_to_date(in_data['date30dAgo'], NSE_DATE_FORMAT)
        in_data["date30dAgo"] = date30dAgo.strftime(DATE_FORMAT)
        return in_data


class EquityResponseSchema(Schema):
    equity = fields.Boolean(default=True)
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(EquitySchema))


class EquityRequestSchema(Schema):
    security = fields.Str()
