"""Security in Focus Schema."""
from datetime import date, datetime

from marshmallow import Schema, fields, pre_load
from tbutilslib.config.constants import TB_DATE_FORMAT, FULL_TS_FORMAT
from tbutilslib.utils.common import parse_timestamp


class SecurityInFocusSchema(Schema):
    """Security in Focus Schema."""

    id = fields.Str(required=False)
    security = fields.Str(required=True)
    strikePrices = fields.List(fields.Int)
    fno = fields.Bool(default=False)
    onDate = fields.Date(TB_DATE_FORMAT, default=date.today())
    timestamp = fields.DateTime(FULL_TS_FORMAT, default=datetime.now)

    @pre_load
    def slugify_date(self, in_data: dict, **kwargs) -> dict:
        """Set a new key onDate.

        Args:
            in_data: dict
        """
        if "timestamp" in in_data:
            ts = parse_timestamp(in_data["timestamp"])
            in_data["onDate"] = ts.date().strftime(TB_DATE_FORMAT)
        return in_data


class SecurityInFocusResponseSchema(Schema):
    """Security in Focus Response Schema."""

    securityInFocus = fields.Boolean(default=True)
    totalItems = fields.Integer()
    securities = fields.List(fields.Str)
    items = fields.List(fields.Nested(SecurityInFocusSchema))
