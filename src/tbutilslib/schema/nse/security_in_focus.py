from marshmallow import Schema, fields, pre_load

from app.utils.common import parse_timestamp
from app.utils.constants import DATE_FORMAT, FULL_TS_FORMAT


class SecurityInFocusSchema(Schema):
    security = fields.Str()
    expiryDates = fields.List(fields.Date(DATE_FORMAT), many=True)
    strikePrices = fields.List(fields.Int)
    onDate = fields.Date(DATE_FORMAT)
    timestamp = fields.DateTime(FULL_TS_FORMAT)

    @pre_load
    def slugify_date(self, in_data, **kwargs):
        ts = parse_timestamp(in_data["timestamp"])
        in_data["onDate"] = ts.date().strftime(DATE_FORMAT)
        return in_data


class SecurityInFocusResponseSchema(Schema):
    securityInFocus = fields.Boolean(default=True)
    totalItems = fields.Integer()
    securities = fields.List(fields.Str)
    items = fields.List(fields.Nested(SecurityInFocusSchema))
