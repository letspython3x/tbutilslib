import functools
import json
import os
import time
from datetime import datetime
from logging import getLogger
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from requests.exceptions import ReadTimeout, HTTPError, RequestException
from urllib3.exceptions import ReadTimeoutError

from .. import errors
from ..config.apiconfig import TbApiPathConfig
from ..schema import OrdersSchema, PositionsSchema
from ..utils.dtu import TODAY, parse_timestamp, parse_timestamp_to_str
from ..utils.enums import SecurityTypeEnum

name = os.path.basename(__file__)
logger = getLogger("tbutilslib." + __name__)


def request_decorator(func, *args, **kwargs):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        resp = None
        try:
            resp = func(*args, **kwargs)
            resp.raise_for_status()
        except HTTPError as ex:
            logger.exception("HTTP error", exc_info=True)
        except (ReadTimeout, ReadTimeoutError) as ex:
            logger.exception("Timeout error", exc_info=True)
        except ConnectionError as ex:
            logger.exception("Connection error", exc_info=True)
        except RequestException as ex:
            logger.exception("Request error", exc_info=True)
            raise SystemExit(ex)
        except Exception as ex:
            logger.exception("Unknown Api error", exc_info=True)
            raise

        return resp.json() if resp else {}

    return wrapper


class TbApi:
    def __init__(self):
        self.bse_url: str = TbApiPathConfig.BASE_URI
        self.verify_ssl: Optional[bool] = None  # TODO: CA Bundle
        self.x_force_delete: bool = False
        self.header: dict = {}
        self._make_tb_api_headers()

    def _make_tb_api_headers(self):
        """Make trading bot api headers."""
        self.header = TbApiPathConfig.headers
        if self.x_force_delete:
            self.header.update({"X-Force-Delete": "true"})

    @request_decorator
    def _api_request(
        self,
        method: str = "get",
        endpoint: str = "/",
        params: Optional[dict] = None,
        data: Optional[list] = None,
        retry_codes: Optional[int] = None,
        max_retries: int = 3,
        retry_wait: int = 2,
    ):
        """Trading Bot api request."""

        valid: bool = False
        attempt: int = 0
        method: str = method.lower()
        params: dict = params or {}
        url: str = urljoin(self.bse_url, endpoint)
        data: dict = data or {}

        while True:
            attempt += 1
            if method in ["post", "put"]:
                response = getattr(requests, method)(
                    url, json=data, headers=self.header, verify=self.verify_ssl
                )
            elif method == "get" and params:
                response = getattr(requests, method)(
                    url, headers=self.header, params=params, verify=self.verify_ssl
                )
            elif method in ["get", "delete"]:
                response = getattr(requests, method)(
                    url, headers=self.header, verify=self.verify_ssl
                )
            else:
                logger.info("Requested method %s not supported.", method)
                raise ValueError("Requested method %s not supported." % method)
            if response.status_code not in (retry_codes or [429, 502, 503, 504]):
                valid = True
                if str(response.status_code)[0] in ("4", "5"):
                    logger.info(
                        "TradingBotAPI ERROR: {} - {} : {}".format(
                            response.status_code, url, response.text
                        )
                    )
                else:
                    logger.info(
                        "TradingBotAPI response: {} - {}".format(
                            response.status_code, url
                        )
                    )
                break
            if attempt > max_retries:
                break
            time.sleep(retry_wait)
        if valid:
            return response

        raise errors.TradingBotAPIException("Unable to get response from TBAPI")

    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[list | dict] = None,
        params: Optional[dict] = None,
    ):
        """Trading Bot api request."""
        try:
            response = self._api_request(
                method=method, endpoint=endpoint, data=data, params=params
            )
        except errors.TradingBotAPIException as e:
            logger.info("TradingBotAPIException: %s", e.message, exc_info=True)
            raise errors.TradingBotAPIException(e.message)

        except ValueError as e:
            logger.info("ValueError: ", exc_info=True)
            raise errors.TradingBotAPIException(str(e))

        return response

    def get(self, endpoint: str, query: Optional[dict] = None) -> Optional[dict]:
        """Get Request."""
        resp = self.request("get", endpoint, params=query)
        return resp

    def post(self, endpoint: str, data: list | dict):
        """Post Request."""
        self.request("post", endpoint, data=data)

    def put(self, endpoint, data: list | dict):
        """Put Request."""
        if isinstance(data, dict):
            self.request("put", endpoint, data=data)
        elif isinstance(data, list):
            for datum in data:
                self.request("put", endpoint, data=datum)

    def delete(self, endpoint: str):
        """Delete Request."""
        self.x_force_delete = True
        self._make_tb_api_headers()
        self.request("delete", endpoint)

    def get_security_in_focus(self, on_date: str = TODAY):
        """Fetch cache security in focus from TbApi."""
        endpoint = f"{TbApiPathConfig.SECURITY_IN_FOCUS}/{on_date}"
        return self.get(endpoint)

    def get_historical_derivatives(self, security: str = None, query: Dict = None):
        """Get Cache Historical Derivatives."""
        endpoint = (
            f"{TbApiPathConfig.HISTORICAL_DERIVATIVES}/{security}"
            if security
            else TbApiPathConfig.HISTORICAL_DERIVATIVES
        )
        return self.get(endpoint, query=query)

    def get_investment(self):
        """Fetch cache Fii-Dii Investment from TbApi."""
        endpoint = TbApiPathConfig.FII_DII
        return self.get(endpoint)

    def get_past_trading_dates(self, count: int):
        """Fetch past trading dates from TbApi."""

        fii_dii = self.get_investment()
        dates = list({item["on_date"] for item in fii_dii})
        return dates[:count]

    def get_trading_dates(self):
        """Fetch cache Trading Dates from TbApi."""
        endpoint = TbApiPathConfig.TRADING_DATES
        return self.get(endpoint)

    def get_orders(self, on_date: str = TODAY):
        """Fetch cache Orders from TbApi."""
        endpoint = f"{TbApiPathConfig.ORDERS}/{on_date}"
        return self.get(endpoint)

    def get_positions(self, on_date: str = TODAY):
        """Fetch cache Orders from TbApi."""
        endpoint = f"{TbApiPathConfig.POSITIONS}/{on_date}"
        return self.get(endpoint)

    def get_expiry_dates(self, security_type: str = SecurityTypeEnum.EQUITY.value):
        """Fetch cache Orders from TbApi."""

        endpoint = f"{TbApiPathConfig.EXPIRY_DATES}/{security_type.lower()}"
        return self.get(endpoint)

    def get_events(
        self, query: Optional[dict] = None, securities: Optional[list] = None
    ):
        """Fetch cache events from TbApi."""

        endpoint = TbApiPathConfig.EVENTS_PATH
        query = query or {}
        if securities:
            logger.info("Events Count of securities: %d ", len(securities))
            if len(securities) < 80:
                query.update({"security__in": json.dumps(securities)})
            else:
                logger.info("Count of securities is greater than permissible limit.")
        return self.get(endpoint, query=query)

    def get_most_traded_securities(
        self, key: str = "totalTradedValue", count: int = 3, on_date: str = TODAY
    ):
        """Fetch most Traded securities from NSE."""

        endpoint = f"{TbApiPathConfig.EQUITY}/{on_date}"
        items = self.get(endpoint)
        items = [item for item in items if item["security"] != "NIFTY"]
        latest_ts = max([parse_timestamp(item["timestamp"]) for item in items])
        latest_ts = parse_timestamp_to_str(latest_ts)
        latest_ts_payload = [item for item in items if item["timestamp"] == latest_ts]
        latest_ts_payload.sort(key=lambda x: x[key], reverse=True)
        return latest_ts_payload[:count]

    def save_orders(self, orders: list[dict]):
        """Save orders to TbApi."""

        endpoint = f"{TbApiPathConfig.ORDERS}/{TODAY}"
        cache_orders = self.get_orders()
        cache_order_ids = {od["orderId"] for od in cache_orders}
        post_orders = [
            {
                **order,
                "security": order["symbol"],
                "limit_price": order["lmtPrice"],
                "on_date": datetime.today(),
                "timestamp": datetime.now(),
            }
            for order in orders
            if order["orderId"] not in cache_order_ids
        ]
        post_orders = OrdersSchema().dump(post_orders, many=True)
        self.post(endpoint, data=post_orders)

    def save_positions(self, positions: List[Dict]):
        """Save positions to TbApi."""

        endpoint = f"{TbApiPathConfig.POSITIONS}/{TODAY}"
        cache_positions = self.get_positions()
        cache_securities = {pos["security"] for pos in cache_positions}
        positions = [
            {
                **position,
                "security": position["symbol"],
                "on_date": datetime.today(),
                "timestamp": datetime.now(),
            }
            for position in positions
            if position["symbol"] not in cache_securities
        ]
        if positions:
            post_positions = PositionsSchema().dump(positions, many=True)
            self.post(endpoint, data=post_positions)

        update_positions = {
            position["symbol"]: {
                **position,
                "security": position["symbol"],
                "on_date": datetime.today(),
                "timestamp": datetime.now(),
            }
            for position in positions
            if position["symbol"] in cache_securities
        }
        if update_positions:
            self.update_positions(update_positions)

    def update_orders(self, orders):
        """Update orders in TbApi."""

        endpoint = f"{TbApiPathConfig.ORDERS}/{TODAY}"
        put_orders = [
            {
                **val,
                "security": val["symbol"],
                "limit_price": val["lmtPrice"],
                "on_date": datetime.today(),
                "timestamp": datetime.now(),
            }
            for oid, val in orders.items()
        ]
        put_orders = OrdersSchema().dump(put_orders, many=True)
        self.put(endpoint, data=put_orders)

    def update_positions(self, positions: Dict):
        """Update positions in TbApi."""

        endpoint = f"{TbApiPathConfig.POSITIONS}/{TODAY}"
        put_positions = [
            {
                **val,
                "security": val["symbol"],
                "on_date": datetime.today(),
                "timestamp": datetime.now(),
            }
            for val in positions.values()
        ]
        put_positions = PositionsSchema().dump(put_positions, many=True)
        self.put(endpoint, data=put_positions)
