"""FII-DII Schema."""
from marshmallow import Schema, fields

from ...utils.enums import DateFormatEnum


class FiiDiiSchema(Schema):
    """FII-DII Schema."""

    id = fields.String(required=False)
    category = fields.String(required=True)
    fii_purchase = fields.Float()
    dii_purchase = fields.Float()
    fii_sales = fields.Float()
    dii_sales = fields.Float()
    fii_net = fields.Float()
    dii_net = fields.Float()
    on_date = fields.Date(DateFormatEnum.TB_DATE.value)


class FiiDiiResponseSchema(Schema):
    """FII-DII Response Schema."""

    fii_dii = fields.Boolean(default=True)
    possible_keys = fields.List(fields.String())
    total_items = fields.Integer()
    items = fields.List(fields.Nested(FiiDiiSchema))
