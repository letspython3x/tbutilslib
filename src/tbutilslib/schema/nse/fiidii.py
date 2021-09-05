"""FII-DII Schema."""
from marshmallow import Schema, fields

from tbutilslib.config.constants import TB_DATE_FORMAT


class FiiDiiSchema(Schema):
    """FII-DII Schema."""

    category = fields.Str(required=True)
    onDate = fields.Date(TB_DATE_FORMAT)
    buyValue = fields.Float()
    sellValue = fields.Float()
    netValue = fields.Float()


class FiiDiiResponseSchema(Schema):
    """FII-DII Response Schema."""

    fiidii = fields.Boolean(default=True)
    possibleKeys = fields.List(fields.Str())
    totalItems = fields.Integer()
    items = fields.List(fields.Nested(FiiDiiSchema))
