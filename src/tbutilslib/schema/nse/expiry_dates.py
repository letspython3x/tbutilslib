"""Expiry Dates Collection."""

from marshmallow import Schema, fields
from tbutilslib.config.constants import TB_DATE_FORMAT, FULL_TS_FORMAT


class ExpiryDatesSchema(Schema):
    """Expiry Dates Schema."""

    id = fields.Str(required=False)
    securityType = fields.Str(required=True)
    expiryDates = fields.List(fields.Date(format=TB_DATE_FORMAT))
    timestamp = fields.DateTime(format=FULL_TS_FORMAT, )


class ExpiryDatesResponseSchema(Schema):
    """Expiry Dates Response Schema."""

    expiryDates = fields.Boolean(default=True)
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(ExpiryDatesSchema))
