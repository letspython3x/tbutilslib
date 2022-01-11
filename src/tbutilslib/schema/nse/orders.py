from marshmallow import Schema, fields
from tbutilslib.config.constants import TB_DATE_FORMAT, FULL_TS_FORMAT
from tbutilslib.utils.common import validate_quantity
from datetime import datetime


class OrdersSchema(Schema):
    """Orders Schema."""

    orderId = fields.Integer(required=True)
    security = fields.String(required=True)
    secType = fields.String(required=True)
    orderType = fields.String(required=True)
    status = fields.String()
    action = fields.String()
    limitPrice = fields.Float()
    auxPrice = fields.Float()
    totalQuantity = fields.Float(validate=validate_quantity)
    filled = fields.Float()
    remaining = fields.Float()
    avgFillPrice = fields.Float()
    onDate = fields.Date(TB_DATE_FORMAT)
    timestamp = fields.DateTime(FULL_TS_FORMAT, default=datetime.now)


class OrdersResponseSchema(Schema):
    """Order Dates Response Schema."""

    orders = fields.Boolean(default=True)
    totalItems = fields.Integer()
    possibleKeys = fields.List(fields.String())
    items = fields.List(fields.Nested(OrdersSchema))
