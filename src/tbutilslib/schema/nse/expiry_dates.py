"""Expiry Dates Collection."""

from marshmallow import Schema, fields
from tbutilslib.config.constants import (TB_DATE_FORMAT,
                                         FULL_TS_FORMAT)


class ExpiryDatesSchema(Schema):
    """Expiry Dates Schema."""

    index = fields.Bool(default=False)
    expiryDates = fields.List(fields.Date(format=TB_DATE_FORMAT))
    timestamp = fields.Date(format=FULL_TS_FORMAT)


class ExpiryDatesResponseSchema(Schema):
    """Expiry Dates Response Schema."""

    expiryDates = fields.Boolean(default=True)
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(ExpiryDatesSchema))
