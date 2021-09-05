from marshmallow import Schema, fields

from app.utils.constants import DATE_FORMAT


class FiiDiiSchema(Schema):
    category = fields.Str(required=True)
    onDate = fields.Date(DATE_FORMAT)
    buyValue = fields.Float()
    sellValue = fields.Float()
    netValue = fields.Float()


class FiiDiiResponseSchema(Schema):
    fiidii = fields.Boolean(default=True)
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(FiiDiiSchema))
