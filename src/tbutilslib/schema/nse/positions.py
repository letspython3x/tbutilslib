from marshmallow import Schema, fields, pre_load
from tbutilslib.config.constants import TB_DATE_FORMAT, FULL_TS_FORMAT
from tbutilslib.utils.common import parse_timestamp, validate_quantity


class PositionsSchema(Schema):
    """Positions Schema."""

    account = fields.Integer(required=True)
    security = fields.String(required=True)
    secType = fields.String()
    currency = fields.String()
    position = fields.Float()
    avgCost = fields.Float(validate=validate_quantity)
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


class PositionsResponseSchema(Schema):
    """Order Dates Response Schema."""

    positions = fields.Boolean(default=True)
    totalItems = fields.Integer()
    possibleKeys = fields.List(fields.String())
    items = fields.List(fields.Nested(PositionsSchema))
