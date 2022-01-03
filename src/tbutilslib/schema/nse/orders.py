from marshmallow import Schema, fields
from tbutilslib.config.constants import FULL_TS_FORMAT
from tbutilslib.utils.common import validate_quantity


class OrdersSchema(Schema):
    """Orders Schema."""

    orderId = fields.Integer(required=True)
    security = fields.String(required=True)
    status = fields.String()
    action = fields.String()
    limitPrice = fields.Float()
    auxPrice = fields.Float()
    totalQuantity = fields.Float(validate=validate_quantity)
    filled = fields.Float()
    remaining = fields.Float()
    timestamp = fields.DateTime(FULL_TS_FORMAT)


class OrdersResponseSchema(Schema):
    """Order Dates Response Schema."""

    orders = fields.Boolean(default=True)
    totalItems = fields.Integer()
    possibleKeys = fields.List(fields.String())
    items = fields.List(fields.Nested(OrdersSchema))
