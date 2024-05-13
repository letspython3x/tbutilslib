"""FII-DII Schema."""
from marshmallow import Schema, fields

from ...utils.enums import DateFormatEnum


class FiiDiiSchema(Schema):
    """FII-DII Schema."""

    id = fields.String(required=False)
    category = fields.String(required=True)
    on_date = fields.Date(DateFormatEnum.TB_DATE.value)
    buy_value = fields.Float()
    sell_value = fields.Float()
    net_value = fields.Float()


class FiiDiiResponseSchema(Schema):
    """FII-DII Response Schema."""

    fii_dii = fields.Boolean(default=True)
    possible_keys = fields.List(fields.String())
    total_items = fields.Integer()
    items = fields.List(fields.Nested(FiiDiiSchema))
