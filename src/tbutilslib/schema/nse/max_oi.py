from marshmallow import Schema, fields

from app.utils.constants import DATE_FORMAT


class MaxOiDatumSchema(Schema):
    openInterest = fields.Int()
    strikePrice = fields.Int()


class MaxOpenInterestSchema(Schema):
    CE = fields.Nested(MaxOiDatumSchema)
    PE = fields.Nested(MaxOiDatumSchema)


class MaxOpenInterestResponseSchema(Schema):
    maxOpenInterest = fields.Boolean(default=True)
    security = fields.Str()
    expiryDate = fields.Date(DATE_FORMAT)
    possibleKeys = fields.List(fields.Str())
    items = fields.Nested(MaxOpenInterestSchema)


class MaxOpenInterestRequestSchema(Schema):
    security = fields.Str()
