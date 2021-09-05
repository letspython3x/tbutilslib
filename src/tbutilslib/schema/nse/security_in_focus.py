"""Security in Focus Schema."""
from marshmallow import Schema, fields, pre_load
from tbutilslib.config.constants import TB_DATE_FORMAT, FULL_TS_FORMAT
from tbutilslib.utils.common import parse_timestamp


class SecurityInFocusSchema(Schema):
    """Security in Focus Schema."""

    security = fields.Str()
    expiryDates = fields.List(fields.Date(TB_DATE_FORMAT), many=True)
    strikePrices = fields.List(fields.Int)
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


class SecurityInFocusResponseSchema(Schema):
    """Security in Focus Response Schema."""

    securityInFocus = fields.Boolean(default=True)
    totalItems = fields.Integer()
    securities = fields.List(fields.Str)
    items = fields.List(fields.Nested(SecurityInFocusSchema))
