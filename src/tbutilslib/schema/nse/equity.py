"""Equity Related Schema."""
from marshmallow import Schema, fields, pre_load

from ...utils.common import validate_quantity
from ...utils.dtu import parse_timestamp, str_to_date, change_date_format
from ...utils.enums import DateFormatEnum


class EquitySchema(Schema):
    """Equity Schema."""

    id = fields.String(required=False)
    security = fields.String()
    identifier = fields.String()
    series = fields.String()
    open = fields.Float()
    day_high = fields.Float()
    day_low = fields.Float()
    last_price = fields.Float()
    previous_close = fields.Float()
    change = fields.Float()
    p_change = fields.Float()
    total_traded_volume = fields.Integer(validate=validate_quantity, default=0)
    total_traded_value = fields.Float()
    year_high = fields.Float()
    year_low = fields.Float()
    ffmc = fields.Float()
    near_weak_high = fields.Float()
    near_weak_low = fields.Float()
    per_change_30d = fields.Float()
    per_change_365d = fields.Float()
    chart_30d_path = fields.String()
    chart_today_path = fields.String()
    chart_365d_path = fields.String()
    date_30d_ago = fields.Date(format=DateFormatEnum.TB_DATE.value)
    date_365d_ago = fields.Date(format=DateFormatEnum.TB_DATE.value)
    timestamp = fields.DateTime(DateFormatEnum.FULL_TS.value)
    on_date = fields.Date(format=DateFormatEnum.TB_DATE.value)
    last_update_time = fields.DateTime(DateFormatEnum.FULL_TS.value)
    # Fields coming from `meta`
    company_name = fields.String()
    industry = fields.String()
    active_series = fields.List(fields.String(), default=[])
    debt_series = fields.List(fields.String(), default=[])
    temp_suspended_series = fields.List(fields.String(), default=[])
    is_fno_sec = fields.Bool()
    is_ca_sec = fields.Bool()
    is_slb_sec = fields.Bool()
    is_debt_sec = fields.Bool()
    is_suspended = fields.Bool()
    is_etf_Sec = fields.Bool()
    is_delisted = fields.Bool()
    isin = fields.String()
    is_municipal_bond = fields.Bool()

    @pre_load
    def slugify_date(self, in_data: dict, **kwargs) -> dict:
        """Set a new key on_date and update date format for date30dAgo.

        Args:
            in_data: dict
        """
        is_nse = in_data.get("is_nse", False)
        if is_nse:
            ts = parse_timestamp(in_data["timestamp"])
            on_date = ts.date().strftime(DateFormatEnum.TB_DATE.value)

            date_30d_ago = str_to_date(
                in_data["date30dAgo"], DateFormatEnum.NSE_DATE.value
            )
            date_30d_ago = date_30d_ago.strftime(DateFormatEnum.TB_DATE.value)

            date_365d_ago = str_to_date(
                in_data["date365dAgo"], DateFormatEnum.NSE_DATE.value
            )
            date_365d_ago = date_365d_ago.strftime(DateFormatEnum.TB_DATE.value)

            return {
                "security": in_data["symbol"],
                "identifier": in_data["identifier"],
                "series": in_data["series"],
                "open": in_data["open"],
                "day_high": in_data["dayHigh"],
                "day_low": in_data["dayLow"],
                "last_price": in_data["lastPrice"],
                "previous_close": in_data["previousClose"],
                "change": in_data["change"],
                "p_change": in_data["pChange"],
                "total_traded_volume": in_data["totalTradedVolume"],
                "total_traded_value": in_data["totalTradedValue"],
                "year_high": in_data["yearHigh"],
                "year_low": in_data["yearLow"],
                "ffmc": in_data["ffmc"],
                "near_weak_high": in_data["nearWKH"],
                "near_weak_low": in_data["nearWKL"],
                "per_change_30d": in_data["perChange30d"],
                "per_change_365d": in_data["perChange365d"],
                "chart_30d_path": in_data["chart30dPath"],
                "chart_today_path": in_data["chartTodayPath"],
                "chart_365d_path": in_data["chart365dPath"],
                "on_date": on_date,
                "date_30d_ago": date_30d_ago,
                "date_365d_ago": date_365d_ago,
                "timestamp": change_date_format(
                    in_data["timestamp"], DateFormatEnum.FULL_TS.value
                ),
                "last_update_time": change_date_format(
                    in_data["lastUpdateTime"], DateFormatEnum.FULL_TS.value
                ),
                "company_name": in_data["companyName"],
                "industry": in_data.get("industry") or "",
                "active_series": in_data["activeSeries"],
                "debt_series": in_data["debtSeries"],
                "temp_suspended_series": in_data["tempSuspendedSeries"],
                "is_fno_sec": in_data["isFNOSec"],
                "is_ca_sec": in_data["isCASec"],
                "is_slb_sec": in_data["isSLBSec"],
                "is_debt_sec": in_data["isDebtSec"],
                "is_suspended": in_data["isSuspended"],
                "is_etf_Sec": in_data["isETFSec"],
                "is_delisted": in_data["isDelisted"],
                "isin": in_data["isin"],
                "is_municipal_bond": in_data["isMunicipalBond"],
            }

        return in_data


class EquityResponseSchema(Schema):
    """Equity Response Schema."""

    equity = fields.Boolean(default=True)
    possible_keys = fields.List(fields.String())
    total_items = fields.Integer()
    items = fields.List(fields.Nested(EquitySchema))


class EquityRequestSchema(Schema):
    """Equity Request Schema."""

    security = fields.String()


class AdvanceDeclineSchema(Schema):
    """Advance Decline Schema."""

    id = fields.String(required=False)
    advances = fields.Integer()
    declines = fields.Integer()
    unchanged = fields.Integer()
    timestamp = fields.DateTime(DateFormatEnum.FULL_TS.value)
    on_date = fields.Date(DateFormatEnum.TB_DATE.value)

    @pre_load
    def slugify_date(self, in_data: dict, **kwargs) -> dict:
        """Set a new key on_date.

        Args:
            in_data: dict
        """
        ts = parse_timestamp(in_data["timestamp"])
        in_data["on_date"] = ts.date().strftime(DateFormatEnum.TB_DATE.value)
        return in_data


class AdvanceDeclineResponseSchema(Schema):
    """Advance Decline Response Schema."""

    advance_decline = fields.Boolean(default=True)
    total_items = fields.Integer()
    items = fields.List(fields.Nested(AdvanceDeclineSchema))


class EquityMetaSchema(Schema):
    """Static Equity Schema."""

    id = fields.String(required=False)
    security = fields.String()
    company = fields.String()
    industry = fields.String()
    isin = fields.String()
    series = fields.String()
    is_fno = fields.Boolean(default=False)
    is_nifty_50 = fields.Boolean(default=False)
    is_nifty_100 = fields.Boolean(default=False)
    is_nifty_500 = fields.Boolean(default=False)


class EquityMetaResponseSchema(Schema):
    """Equity Meta Response Schema."""

    equity_meta = fields.Boolean(default=True)
    total_items = fields.Integer()
    items = fields.List(fields.Nested(EquityMetaSchema))
