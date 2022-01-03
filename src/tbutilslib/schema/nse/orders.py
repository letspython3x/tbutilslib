from marshmallow import Schema, fields, pre_load
from tbutilslib.config.constants import TB_DATE_FORMAT, FULL_TS_FORMAT
from tbutilslib.utils.common import parse_timestamp, validate_quantity


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
    onDate = fields.Date(TB_DATE_FORMAT)
    timestamp = fields.DateTime(FULL_TS_FORMAT)

    @pre_load
    def slugify_date(self, in_data: dict, **kwargs) -> dict:
        """Set a new key onDate.

        Args:
            in_data: dict
        """
        ts = parse_timestamp(in_data["timestamp"])
        in_data["onDate"] = ts.date().strftime(TB_DATE_FORMAT)
        return in_data


class OrdersResponseSchema(Schema):
    """Order Dates Response Schema."""

    orders = fields.Boolean(default=True)
    totalItems = fields.Integer()
    possibleKeys = fields.List(fields.String())
    items = fields.List(fields.Nested(OrdersSchema))
