"""FII-DII Schema."""
from marshmallow import Schema, fields, pre_load

from ...utils.dtu import change_date_format, str_to_date
from ...utils.enums import DateFormatEnum, FiiDiiCategoryEnum


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

    @pre_load
    def marshal_fields(self, in_data: dict, **kwargs) -> dict:
        """Set new keys on data."""
        on_date = str_to_date(in_data["on_date"], DateFormatEnum.NSE_DATE.value)
        on_date = change_date_format(on_date, DateFormatEnum.TB_DATE.value)
        return {
            "category": FiiDiiCategoryEnum[in_data["category"].upper()].value,
            "fii_purchase": float(in_data["fii_purchase"].replace(",", "")),
            "dii_purchase": float(in_data["dii_purchase"].replace(",", "")),
            "fii_sales": float(in_data["fii_sales"].replace(",", "")),
            "dii_sales": float(in_data["dii_sales"].replace(",", "")),
            "fii_net": float(in_data["fii_net"].replace(",", "")),
            "dii_net": float(in_data["dii_net"].replace(",", "")),
            "on_date": on_date,
        }


class FiiDiiResponseSchema(Schema):
    """FII-DII Response Schema."""

    fii_dii = fields.Boolean(default=True)
    possible_keys = fields.List(fields.String())
    total_items = fields.Integer()
    items = fields.List(fields.Nested(FiiDiiSchema))
