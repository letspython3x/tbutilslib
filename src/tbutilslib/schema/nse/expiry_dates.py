"""Expiry Dates Collection."""

from marshmallow import Schema, fields
from ...utils.enums import DateFormatEnum


class ExpiryDatesSchema(Schema):
    """Expiry Dates Schema."""

    id = fields.String(required=False)
    security_type = fields.String(required=True)
    expiry_dates = fields.List(fields.Date(format=DateFormatEnum.TB_DATE.value))
    timestamp = fields.DateTime(format=DateFormatEnum.FULL_TS.value)


class ExpiryDatesResponseSchema(Schema):
    """Expiry Dates Response Schema."""

    expiry_dates = fields.Boolean(default=True)
    possible_keys = fields.List(fields.String())
    total_items = fields.Integer()
    items = fields.List(fields.Nested(ExpiryDatesSchema))
