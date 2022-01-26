import functools
import json
import os
import time
from datetime import datetime
from typing import Dict, List
from urllib.parse import urljoin

import requests
from requests.exceptions import ReadTimeout, HTTPError, RequestException
from urllib3.exceptions import ReadTimeoutError

from .. import errors
from ..config.apiconfig import TbApiPathConfig
from ..logger import get_logger
from ..schema import OrdersSchema, PositionsSchema
from ..utils.common import (TODAY,
                            parse_timestamp,
                            parse_timestamp_to_str)

name = os.path.basename(__file__)
logger = get_logger(name)


def request_decorator(func, *args, **kwargs):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        resp = None
        try:
            resp = func(*args, **kwargs)
            resp.raise_for_status()
        except HTTPError as ex:
            print(f'HTTP error occurred: {ex}')
        except (ReadTimeout, ReadTimeoutError) as ex:
            print(f'Timeout error occurred: {ex}')
        except ConnectionError as ex:
            print(f'Connection error occurred: {ex}')
        except RequestException as ex:
            raise SystemExit(ex)
        except Exception as ex:
            print(f">>> TBAPI POST REQUEST FAILURE: {ex}")
            raise
        return resp.json() if resp else {}

    return wrapper


class TbApi:
    def __init__(self):
        self._api = None
        self.baseURL = TbApiPathConfig.BASE_URI
        self.verify_ssl = None  # TODO: CA Bundle
        self.delete = False
        self.header = {}
        self._make_tb_api_headers()

    def _make_tb_api_headers(self):
        """Make trading bot api headers."""
        self.header = TbApiPathConfig.headers
        if self.delete:
            self.header.updte({'X-Force-Delete': 'true'})

    @request_decorator
    def _api_request(self, method="get", endpoint="/", params=None,
                     data=None, retryCodes=None, maxRetries=30, retryWait=2):
        """Trading Bot api request."""
        valid = False
        attempt = 0
        method = method.lower()
        params = params or {}
        url = urljoin(self.baseURL, endpoint)
        data = data or {}

        while True:
            attempt += 1
            if method in ["post", "put"]:
                response = getattr(requests, method)(
                    url, json=data, headers=self.header,
                    verify=self.verify_ssl)
            elif method == "get" and params:
                response = getattr(requests, method)(
                    url, headers=self.header,
                    params=params, verify=self.verify_ssl)
            elif method in ["get", "delete"]:
                response = getattr(requests, method)(
                    url, headers=self.header,
                    verify=self.verify_ssl)
            else:
                logger.debug("method: {}".format(method))
                raise ValueError("Requested method not supported.")
            if response.status_code not in (retryCodes or [429, 502, 503, 504]):
                valid = True
                if str(response.status_code)[0] in ("4", "5"):
                    logger.debug("TradingBotAPI ERROR: {} - {} : {}".format(
                        response.status_code, url, response.text))
                else:
                    logger.debug("TradingBotAPI response: {} - {}".format(
                        response.status_code, url))
                break
            if attempt > maxRetries:
                break
            time.sleep(retryWait)
        if valid:
            return response
        raise errors.TradingBotAPIException("Unable to get response from TBAPI")

    def request(self, method, endpoint, data=None, params=None):
        """Trading Bot api request."""
        try:
            response = self._api_request(
                method=method, endpoint=endpoint, data=data, params=params)
        except errors.TradingBotAPIException as e:
            raise errors.TradingBotAPIException(e)
        except ValueError as e:
            raise errors.TradingBotAPIException(e)
        return response

    def get(self, endpoint, method="get", query=None):
        """Get Request."""
        resp = self.request(method, endpoint, params=query)
        return (resp or []) and resp.get('items', [])

    def post(self, endpoint, method="post", data=None):
        """Post Request."""
        self.request(method, endpoint, data=data)

    def put(self, endpoint, method="put", data=None):
        """Put Request."""
        if isinstance(data, dict):
            self.request(method, endpoint, data=data)
        elif isinstance(data, list):
            for datum in data:
                self.request(method, endpoint, data=datum)

    def delete(self, endpoint, method="delete"):
        """Delete Request."""
        self.delete = True
        self._make_tb_api_headers()
        self.request(method, endpoint)

    def get_security_in_focus(self, onDate=TODAY):
        """Fetch cache security in focus from TbApi."""
        endpoint = f"{TbApiPathConfig.SECURITY_IN_FOCUS}/{onDate}"
        return self.get(endpoint)

    def get_historical_derivatives(self,
                                   security: str = None,
                                   query: Dict = None):
        """Get Cache Historical Derivatives."""
        endpoint = (f"{TbApiPathConfig.HISTORICAL_DERIVATIVES}/{security}" if
                    security else TbApiPathConfig.HISTORICAL_DERIVATIVES)
        return self.get(endpoint, query=query)

    def get_investment(self):
        """Fetch cache Fii-Dii Investment from TbApi."""
        endpoint = TbApiPathConfig.FII_DII
        return self.get(endpoint)

    def get_past_trading_dates(self, count: int):
        """Fetch past trading dates from TbApi."""
        fiiDii = self.get_investment()
        dates = list({item["onDate"] for item in fiiDii})
        return dates[:count]

    def get_trading_dates(self):
        """Fetch cache Trading Dates from TbApi."""
        endpoint = TbApiPathConfig.TRADING_DATES
        return self.get(endpoint)

    def get_orders(self, onDate=TODAY):
        """Fetch cache Orders from TbApi."""
        endpoint = f"{TbApiPathConfig.ORDERS}/{onDate}"
        return self.get(endpoint)

    def get_positions(self, onDate=TODAY):
        """Fetch cache Orders from TbApi."""
        endpoint = f"{TbApiPathConfig.POSITIONS}/{onDate}"
        return self.get(endpoint)

    def get_expiry_dates(self, securityType="equity"):
        """Fetch cache Orders from TbApi."""
        endpoint = f"{TbApiPathConfig.EXPIRY_DATES}/{securityType.lower()}"
        return self.get(endpoint)

    def get_events(self, query: Dict = None, securities: List = None):
        """Fetch cache events from TbApi."""
        endpoint = TbApiPathConfig.EVENTS_PATH
        query = query or {}
        if securities and len(securities) < 80:
            query.update({'security__in': json.dumps(securities)})
        return self.get(endpoint, query=query)

    def get_most_traded_securities(self, key="totalTradedValue",
                                   count=3, onDate=TODAY):
        """Fetch most Traded securities from NSE."""
        endpoint = f"{TbApiPathConfig.EQUITY}/{onDate}"
        items = self.get(endpoint)
        items = [item for item in items if item["security"] != "NIFTY"]
        latestTs = max([parse_timestamp(item["timestamp"]) for item in items])
        latestTs = parse_timestamp_to_str(latestTs)
        latestTsPayload = [item for item in items if
                           item["timestamp"] == latestTs]
        latestTsPayload.sort(key=lambda x: x[key], reverse=True)
        return latestTsPayload[:count]

    def save_orders(self, orders: List[Dict]):
        """Save orders to TbApi."""
        endpoint = f"{TbApiPathConfig.ORDERS}/{TODAY}"
        cacheOrders = self.get_orders()
        cacheOrderIds = {od["orderId"] for od in cacheOrders}
        postOrders = [{**order,
                       "security": order["symbol"],
                       "limitPrice": order["lmtPrice"],
                       "onDate": datetime.today(),
                       "timestamp": datetime.now()}
                      for order in orders
                      if order["orderId"] not in cacheOrderIds]
        postOrders = OrdersSchema().dump(postOrders, many=True)
        self.post(endpoint, data=postOrders)

    def save_positions(self, positions: List[Dict]):
        """Save positions to TbApi."""
        endpoint = f"{TbApiPathConfig.POSITIONS}/{TODAY}"
        cachePositions = self.get_positions()
        cacheSecurities = {pos["security"] for pos in cachePositions}
        positions = [{**position,
                      "security": position["symbol"],
                      "onDate": datetime.today(),
                      "timestamp": datetime.now()}
                     for position in positions
                     if position["symbol"] not in cacheSecurities]
        postPositions = PositionsSchema().dump(positions, many=True)
        self.post(endpoint, data=postPositions)

    def update_orders(self, orders):
        """Update orders in TbApi."""
        endpoint = f"{TbApiPathConfig.ORDERS}/{TODAY}"
        putOrders = [{**val,
                      "security": val["symbol"],
                      "limitPrice": val["lmtPrice"],
                      "onDate": datetime.today(),
                      "timestamp": datetime.now()}
                     for oid, val in orders.items()]
        putOrders = OrdersSchema().dump(putOrders, many=True)
        self.put(endpoint, data=putOrders)

    def update_positions(self, positions):
        """Update positions in TbApi."""
        endpoint = f"{TbApiPathConfig.POSITIONS}/{TODAY}"
        putPositions = [{**val,
                         "security": val["symbol"],
                         "onDate": datetime.today(),
                         "timestamp": datetime.now()}
                        for val in positions.values()]
        putPositions = PositionsSchema().dump(putPositions, many=True)
        self.put(endpoint, data=putPositions)
