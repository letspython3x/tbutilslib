from marshmallow import Schema, fields

from app.utils.constants import DATE_FORMAT


class ExpiryDatesResponseSchema(Schema):
    expiryDates = fields.Boolean(default=True)
    security = fields.Str()
    totalItems = fields.Integer()
    possibleKeys = fields.List(fields.Str())
    items = fields.List(fields.Date(format=DATE_FORMAT))
