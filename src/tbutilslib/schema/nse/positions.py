from marshmallow import Schema, fields, pre_load

from ...utils.common import validate_quantity
from ...utils.dtu import parse_timestamp
from ...utils.enums import DateFormatEnum


class PositionsSchema(Schema):
    """Positions Schema."""

    id = fields.String(required=False)
    account = fields.String(required=True)
    security = fields.String(required=True)
    sec_type = fields.String()
    currency = fields.String()
    position = fields.Float()
    avg_cost = fields.Float(validate=validate_quantity)
    on_date = fields.Date(DateFormatEnum.TB_DATE.value)
    timestamp = fields.DateTime(DateFormatEnum.FULL_TS.value)

    @pre_load
    def slugify_date(self, in_data: dict, **kwargs) -> dict:
        """Set a new key on_date.

        Args:
            in_data: dict
        """
        ts = parse_timestamp(in_data["timestamp"])
        in_data["on_date"] = ts.date().strftime(DateFormatEnum.TB_DATE.value)
        return in_data


class PositionsResponseSchema(Schema):
    """Order Dates Response Schema."""

    positions = fields.Boolean(default=True)
    totalItems = fields.Integer()
    possibleKeys = fields.List(fields.String())
    items = fields.List(fields.Nested(PositionsSchema))
