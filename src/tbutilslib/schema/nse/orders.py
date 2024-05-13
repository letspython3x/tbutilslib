from marshmallow import Schema, fields

from datetime import datetime

from ...utils.common import validate_quantity
from ...utils.enums import DateFormatEnum


class OrdersSchema(Schema):
    """Orders Schema."""

    id = fields.String(required=False)
    order_id = fields.Integer(required=True)
    security = fields.String(required=True)
    sec_type = fields.String(required=True)
    order_type = fields.String(required=True)
    status = fields.String()
    action = fields.String()
    limit_price = fields.Float()
    aux_price = fields.Float()
    total_quantity = fields.Float(validate=validate_quantity)
    filled = fields.Float()
    remaining = fields.Float()
    avg_fill_price = fields.Float()
    on_date = fields.Date(DateFormatEnum.TB_DATE.value)
    timestamp = fields.DateTime(DateFormatEnum.FULL_TS.value, default=datetime.now)


class OrdersResponseSchema(Schema):
    """Order Dates Response Schema."""

    orders = fields.Boolean(default=True)
    total_items = fields.Integer()
    possible_keys = fields.List(fields.String())
    items = fields.List(fields.Nested(OrdersSchema))
