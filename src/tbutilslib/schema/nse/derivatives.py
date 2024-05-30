"""Derivatives Related Schema."""

from datetime import date, datetime
from marshmallow import Schema, fields, pre_load

from ...utils.common import validate_quantity
from ...utils.dtu import (
    parse_timestamp,
    str_to_date,
    change_date_format,
    parse_timestamp_to_str,
)
from ...utils.enums import DateFormatEnum


class CumulativeDerivativesSchema(Schema):
    """Cumulative Derivatives Schema."""

    id = fields.String(required=False)
    security = fields.String(required=True)
    spot_price = fields.Float(validate=validate_quantity)
    future_price = fields.Float(validate=validate_quantity)
    total_open_interest_ce = fields.Float(validate=validate_quantity)
    total_volume_ce = fields.Float(validate=validate_quantity)
    total_open_interest_pe = fields.Float(validate=validate_quantity)
    total_volume_pe = fields.Float(validate=validate_quantity)
    pcr_open_interest = fields.Float(validate=validate_quantity)
    pcr_volume = fields.Float(validate=validate_quantity)
    total_open_interest_fut = fields.Integer(validate=validate_quantity)
    total_volume_fut = fields.Integer(validate=validate_quantity)
    expiry_date = fields.Date(DateFormatEnum.TB_DATE.value)
    on_date = fields.Date(DateFormatEnum.TB_DATE.value)
    timestamp = fields.DateTime(DateFormatEnum.FULL_TS.value)

    @pre_load
    def marshal_fields(self, in_data: dict, **kwargs) -> dict:
        """Marshal the data fields if it comes from nse."""

        is_nse = in_data.get("is_nse")
        if is_nse:
            # if "timestamp" in in_data:
            timestamp: datetime = parse_timestamp(in_data["timestamp"])
            if "expiry_date" in in_data:
                expiry_date: date = str_to_date(
                    in_data["expiry_date"], DateFormatEnum.NSE_DATE.value
                )
                expiry_date: str = change_date_format(
                    expiry_date, DateFormatEnum.TB_DATE.value
                )

            return {
                "security": in_data["security"],
                "spot_price": in_data["spot_price"],
                "future_price": in_data["future_price"],
                "total_open_interest_ce": in_data["total_open_interest_ce"],
                "total_volume_ce": in_data["total_volume_ce"],
                "total_open_interest_pe": in_data["total_open_interest_pe"],
                "total_volume_pe": in_data["total_volume_pe"],
                "pcr_open_interest": in_data["pcr_open_interest"],
                "pcr_volume": in_data["pcr_volume"],
                "total_open_interest_fut": in_data["total_open_interest_fut"],
                "total_volume_fut": in_data["total_volume_fut"],
                "expiry_date": expiry_date,
                "on_date": change_date_format(
                    timestamp.date(), DateFormatEnum.TB_DATE.value
                ),
                "timestamp": parse_timestamp_to_str(
                    timestamp, DateFormatEnum.FULL_TS.value
                ),
            }

        return in_data


class CumulativeDerivativesResponseSchema(Schema):
    """Cumulative Derivatives Response Schema."""

    cumulative = fields.Boolean(default=True)
    security = fields.String()
    total_items = fields.Integer()
    possible_keys = fields.List(fields.String())
    items = fields.List(fields.Nested(CumulativeDerivativesSchema))


class CumulativeRequestSchema(Schema):
    """Cumulative Derivatives Request Schema."""

    security = fields.String()


class DerivativesSchemaCommonFields(Schema):
    """Derivatives Common Fields."""

    id = fields.String(required=False)
    security = fields.String(required=True)
    identifier = fields.String()
    option_type = fields.String()
    last_price = fields.Float()
    open_interest = fields.Integer(validate=validate_quantity)
    implied_volatility = fields.Float()
    change_in_open_interest = fields.Integer()
    p_change_in_open_interest = fields.Float()
    change = fields.Float()
    p_change = fields.Float()
    strike_price = fields.Float()
    traded_volume = fields.Integer(validate=validate_quantity)
    spot_price = fields.Float()
    expiry_date = fields.Date(DateFormatEnum.TB_DATE.value)
    on_date = fields.Date(DateFormatEnum.TB_DATE.value)
    timestamp = fields.DateTime(DateFormatEnum.FULL_TS.value)

    @pre_load
    def marshal_fields(self, in_data: dict, **kwargs) -> dict:
        """Marshal the fields."""

        is_nse = in_data.get("is_nse")
        if is_nse:
            timestamp: datetime = parse_timestamp(in_data["timestamp"])
            on_date: str = change_date_format(
                timestamp.date(), DateFormatEnum.TB_DATE.value
            )
            expiry_date: date = str_to_date(
                in_data["expiryDate"], DateFormatEnum.NSE_DATE.value
            )
            expiry_date: str = change_date_format(
                expiry_date, DateFormatEnum.TB_DATE.value
            )
            traded_volume: int = (
                in_data.get("tradedVolume") or in_data.get("totalTradedVolume") or 0
            )
            spot_price: float = in_data.get("spotPrice") or in_data.get(
                "underlyingValue"
            )

            return {
                "security": in_data["security"],
                "identifier": in_data["identifier"],
                "option_type": in_data["optionType"],
                "last_price": in_data["lastPrice"],
                "open_interest": in_data["openInterest"],
                "implied_volatility": in_data["impliedVolatility"],
                "change_in_open_interest": in_data["changeinOpenInterest"],
                "p_change_in_open_interest": in_data["pchangeinOpenInterest"],
                "change": in_data["change"],
                "p_change": in_data["pChange"],
                "strike_price": in_data["strikePrice"],
                "traded_volume": traded_volume,
                "spot_price": spot_price,
                "expiry_date": expiry_date,
                "on_date": on_date,
                "timestamp": parse_timestamp_to_str(
                    timestamp, DateFormatEnum.FULL_TS.value
                ),
            }

        return in_data


class DerivativesSchemaResponseCommonFields(Schema):
    """Derivatives Response Schema."""

    derivatives = fields.Boolean(default=True)
    security = fields.String()
    total_items = fields.Integer()
    possible_keys = fields.List(fields.String())


class IndexDerivativesSchema(DerivativesSchemaCommonFields):
    """Index Derivatives Schema."""

    instrument_type = fields.String()
    open_price = fields.Float()
    high_price = fields.Float()
    low_price = fields.Float()
    close_price = fields.Float()
    prev_close = fields.Float()
    number_of_contracts_traded = fields.Integer()
    total_turnover = fields.Float()
    value = fields.Float()
    vmap = fields.Float()
    premium_turnover = fields.Float()
    market_lot = fields.Integer(validate=validate_quantity)
    settlement_price = fields.Float()
    daily_volatility = fields.Float()
    annualised_volatility = fields.Float()
    client_wise_position_limits = fields.Integer()
    market_wide_position_limits = fields.Integer()

    @pre_load
    def marshal_fields(self, in_data: dict, **kwargs) -> dict:
        """Set a new key for fields."""

        is_nse = in_data.get("is_nse")
        if is_nse:
            super_data = super().marshal_fields(in_data, **kwargs)
            return {
                **super_data,
                "instrument_type": in_data["instrumentType"],
                "open_price": in_data["openPrice"],
                "high_price": in_data["highPrice"],
                "low_price": in_data["lowPrice"],
                "close_price": in_data["closePrice"],
                "prev_close": in_data["prevClose"],
                "number_of_contracts_traded": in_data["numberOfContractsTraded"],
                "total_turnover": in_data["totalTurnover"],
                "value": in_data["value"],
                "vmap": in_data["vmap"],
                "premium_turnover": in_data["premiumTurnover"],
                "market_lot": in_data["marketLot"],
                "settlement_price": in_data["settlementPrice"],
                "daily_volatility": in_data.get("dailyVolatility")
                or in_data.get("dailyvolatility"),
                "annualised_volatility": in_data["annualisedVolatility"],
                "client_wise_position_limits": in_data["clientWisePositionLimits"],
                "market_wide_position_limits": in_data["marketWidePositionLimits"],
            }

        return in_data


class EquityDerivativesSchema(DerivativesSchemaCommonFields):
    """Equity Derivatives Schema."""

    pass


class IndexDerivativesResponseSchema(DerivativesSchemaResponseCommonFields):
    """Index Derivatives Response Schema."""

    items = fields.List(fields.Nested(IndexDerivativesSchema))


class EquityDerivativesResponseSchema(DerivativesSchemaResponseCommonFields):
    """Equity Derivatives Response Schema."""

    items = fields.List(fields.Nested(EquityDerivativesSchema))


class IndexRequestSchema(Schema):
    """Index Derivatives Request Schema."""

    security = fields.String(required=True)


class EquityRequestSchema(Schema):
    """Equity Derivatives Request Schema."""

    security = fields.String(required=True)


class HistoricalDerivativesSchema(Schema):
    """Historical Derivatives Schema."""

    id = fields.String(required=False)
    security = fields.String(required=True)
    instrument = fields.String()
    market_type = fields.String()
    market_lot = fields.Integer(validate=validate_quantity)
    option_type = fields.String()
    strike_price = fields.Float()
    open_price = fields.Float()
    close_price = fields.Float()
    high_price = fields.Float()
    low_price = fields.Float()
    last_price = fields.Float()
    settle_price = fields.Float()
    prev_close_price = fields.Float()
    traded_volume = fields.Integer()
    traded_value = fields.Integer()
    premium_value = fields.Float()
    open_interest = fields.Integer()
    change_in_open_interest = fields.Integer()
    position_type = fields.String()
    on_date = fields.Date(format=DateFormatEnum.TB_DATE.value)
    expiry_date = fields.Date(format=DateFormatEnum.TB_DATE.value)
    timestamp = fields.DateTime(format=DateFormatEnum.FULL_TS_TZ.value)

    @pre_load
    def marshal_fields(self, in_data: dict, **kwargs) -> dict:
        """Marshal the fields."""

        is_nse = in_data.get("is_nse")
        if is_nse:
            timestamp: datetime = parse_timestamp(in_data["timestamp"])
            on_date: str = change_date_format(
                timestamp.date(), DateFormatEnum.TB_DATE.value
            )
            expiry_date: date = str_to_date(
                in_data["expiryDate"], DateFormatEnum.NSE_DATE.value
            )
            expiry_date: str = change_date_format(
                expiry_date, DateFormatEnum.TB_DATE.value
            )

            in_data = {
                "security": in_data["security"],
                "instrument": in_data["instrument"],
                "market_type": in_data["marketType"],
                "market_lot": in_data["marketLot"],
                "option_type": in_data["optionType"],
                "strike_price": in_data["strikePrice"],
                "open_price": in_data["openPrice"],
                "close_price": in_data["closePrice"],
                "high_price": in_data["highPrice"],
                "low_price": in_data["lowPrice"],
                "last_price": in_data["lastPrice"],
                "settle_price": in_data["settlePrice"],
                "prev_close_price": in_data["prevClosePrice"],
                "traded_volume": in_data["tradedVolume"] or 0,
                "traded_value": in_data["tradedValue"],
                "premium_value": in_data["premiumValue"],
                "open_interest": in_data["openInterest"],
                "change_in_open_interest": in_data["changeInOI"],
                "position_type": in_data["positionType"],
                "on_date": on_date,
                "expiry_date": expiry_date,
                "timestamp": parse_timestamp_to_str(
                    timestamp, DateFormatEnum.FULL_TS.value
                ),
            }

        market_lot = in_data["market_lot"]
        if market_lot and market_lot != 0:
            in_data["change_in_oi"] = int(in_data["change_in_oi"] / market_lot)
            in_data["open_interest"] = int(in_data["open_interest"] / market_lot)

        return in_data


class HistoricalDerivativesResponseSchema(Schema):
    """Historical Derivatives Response Schema."""

    derivatives = fields.Boolean(default=True)
    security = fields.String()
    total_items = fields.Integer()
    possible_keys = fields.List(fields.String())
    items = fields.List(fields.Nested(HistoricalDerivativesSchema))


class ExpiryDatesResponseSchema(Schema):
    """Expiry Dates Response Schema."""

    expiry_dates = fields.Boolean(default=True)
    security = fields.String()
    total_items = fields.Integer()
    possible_keys = fields.List(fields.String())
    items = fields.List(fields.Date(format=DateFormatEnum.TB_DATE.value))


class OptionMetaDataSchema(Schema):
    """Security in Focus Schema."""

    id = fields.String(required=False)
    security = fields.String(required=True)
    strike_prices = fields.List(fields.Int)
    is_fno = fields.Bool(default=False)
    on_date = fields.Date(DateFormatEnum.TB_DATE.value, default=date.today())
    expiry_dates = fields.List(fields.Date(format=DateFormatEnum.TB_DATE.value))
    timestamp = fields.DateTime(DateFormatEnum.FULL_TS.value, default=datetime.now)

    @pre_load
    def marshal_fields(self, in_data: dict, **kwargs) -> dict:
        """Marshal the fields."""

        is_nse = in_data.get("is_nse", False)
        if is_nse:
            timestamp: datetime = parse_timestamp(in_data["timestamp"])
            on_date: str = change_date_format(
                timestamp.date(), DateFormatEnum.TB_DATE.value
            )

            if "expiry_dates" in in_data:
                updated_expiry_dates = []
                for exp in in_data["expiry_dates"]:
                    ed = str_to_date(exp, DateFormatEnum.NSE_DATE.value)
                    ed = change_date_format(ed, DateFormatEnum.TB_DATE.value)
                    updated_expiry_dates.append(ed)

            return {
                "security": in_data["security"],
                "strike_prices": in_data["strike_prices"],
                "expiry_dates": updated_expiry_dates,
                "is_fno": in_data.get("is_fno", False),
                "on_date": on_date,
                "timestamp": in_data["timestamp"],
            }

        return in_data


class OptionMetaDataResponseSchema(Schema):
    """Security in Focus Response Schema."""

    option_meta_data = fields.Boolean(default=True)
    total_items = fields.Integer()
    securities = fields.List(fields.String)
    items = fields.List(fields.Nested(OptionMetaDataSchema))
