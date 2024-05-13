"""MaxOI Schema."""
from marshmallow import Schema, fields

from ...utils.enums import DateFormatEnum


class MaxOiDatumSchema(Schema):
    """MaxOI Datum Schema."""

    open_interest = fields.Integer()
    strike_price = fields.Integer()


class MaxOpenInterestSchema(Schema):
    """MaxOI Schema."""

    CE = fields.Nested(MaxOiDatumSchema)
    PE = fields.Nested(MaxOiDatumSchema)


class MaxOpenInterestResponseSchema(Schema):
    """MaxOI Response Schema."""

    max_open_interest = fields.Boolean(default=True)
    security = fields.String()
    expiry_date = fields.Date(DateFormatEnum.TB_DATE.value)
    possible_keys = fields.List(fields.String())
    items = fields.Nested(MaxOpenInterestSchema)


class MaxOpenInterestRequestSchema(Schema):
    """MaxOI Request Schema."""

    security = fields.String()
