"""MaxOI Schema."""
from marshmallow import Schema, fields

from tbutilslib.config.constants import TB_DATE_FORMAT


class MaxOiDatumSchema(Schema):
    """MaxOI Datum Schema."""

    openInterest = fields.Integer()
    strikePrice = fields.Integer()


class MaxOpenInterestSchema(Schema):
    """MaxOI Schema."""

    CE = fields.Nested(MaxOiDatumSchema)
    PE = fields.Nested(MaxOiDatumSchema)


class MaxOpenInterestResponseSchema(Schema):
    """MaxOI Response Schema."""

    maxOpenInterest = fields.Boolean(default=True)
    security = fields.String()
    expiryDate = fields.Date(TB_DATE_FORMAT)
    possibleKeys = fields.List(fields.String())
    items = fields.Nested(MaxOpenInterestSchema)


class MaxOpenInterestRequestSchema(Schema):
    """MaxOI Request Schema."""

    security = fields.String()
