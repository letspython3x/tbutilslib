import json
import os
from typing import Dict, List
from urllib.parse import urljoin
from datetime import datetime

from tbutilslib.config.apiconfig import TbApiPathConfig
from tbutilslib.tbapi.api import TbApi
from tbutilslib.utils.common import (TODAY,
                                     parse_timestamp,
                                     parse_timestamp_to_str)
from tbutilslib.schema import OrdersSchema, PositionsSchema

name = os.path.basename(__file__)


def get_cache_security_in_focus():
    """Fetch cache security in focus from TbApi."""
    api = TbApi()
    url = urljoin(TbApiPathConfig.BASE_URI, TbApiPathConfig.SECURITY_IN_FOCUS)
    url = f"{url}/{TODAY}"
    cache = api.get(url)
    return cache.get('items') if cache else []


def get_cache_historical_derivatives(security):
    """Get Cache Historical Derivatives."""
    api = TbApi()
    url = urljoin(TbApiPathConfig.BASE_URI,
                  f"{TbApiPathConfig.HISTORICAL_DERIVATIVES}/{security}")
    cache = api.get(url)
    return cache.get('items') if cache else []


def get_cache_events(query: Dict = None, securities: List = None):
    """Fetch cache events from TbApi."""
    api = TbApi()
    url = urljoin(TbApiPathConfig.BASE_URI, TbApiPathConfig.EVENTS_PATH)
    query = query or {}
    if securities and len(securities) < 80:
        query.update({'security__in': json.dumps(securities)})
    data = api.get(url, params=query)
    events = data['items'] if data and 'items' in data else []
    return events


def get_cache_trading_dates():
    """Fetch cache Trading Dates from TbApi."""
    api = TbApi()
    url = urljoin(TbApiPathConfig.BASE_URI, TbApiPathConfig.TRADING_DATES)
    cache = api.get(url)
    return cache.get('items') if cache else []


def get_cache_investment():
    """Fetch cache Fii-Dii Investment from TbApi."""
    api = TbApi()
    url = urljoin(TbApiPathConfig.BASE_URI, TbApiPathConfig.FII_DII)
    cache = api.get(url)
    return cache.get('items')[0] if cache else []


def get_most_traded_securities(key="totalTradedValue", count=3):
    """Fetch most Traded securities"""
    api = TbApi()
    url = urljoin(TbApiPathConfig.BASE_URI, TbApiPathConfig.EQUITY)
    url = f"{url}/{TODAY}"
    cache = api.get(url)
    items = cache.get('items') if cache else []
    items = [item for item in items if item["security"] != "NIFTY"]
    latestTs = max([parse_timestamp(item["timestamp"]) for item in items])
    latestTs = parse_timestamp_to_str(latestTs)
    latestTsPayload = [item for item in items if item["timestamp"] == latestTs]
    latestTsPayload.sort(key=lambda x: x[key], reverse=True)
    return latestTsPayload[:count]


def save_orders(orders):
    api = TbApi()
    url = urljoin(TbApiPathConfig.BASE_URI, TbApiPathConfig.ORDERS)
    url = f"{url}/{TODAY}"
    cache = api.get(url)
    items = cache.get('items') if cache else []
    cacheOrderIds = {od["orderId"] for od in items}
    orderKeys = set(orders.keys())
    postOrderIds = orderKeys.difference(cacheOrderIds)
    # putOrderIds = ordersKeys.intersection(cacheOrderIds)

    orders = [{**val,
               "security": val["symbol"],
               "limitPrice": val["lmtPrice"],
               "onDate": datetime.today(),
               "timestamp": datetime.now()}
              for oid, val in orders.items()]
    orders = OrdersSchema().dump(orders, many=True)
    postOrders = [order for order in orders
                  if order["orderId"] in postOrderIds]
    # putOrders = [order for order in orders
    #              if order["orderId"] in putOrderIds]
    if postOrders:
        api.post(url, postOrders)
    # api.put(url, putOrders)


def save_positions(positions):
    api = TbApi()
    url = urljoin(TbApiPathConfig.BASE_URI, TbApiPathConfig.POSITIONS)
    url = f"{url}/{TODAY}"
    cache = api.get(url)
    items = cache.get('items') if cache else []
    cachePositions = {pos["security"] for pos in items}
    positionKeys = set(positions.keys())
    postSecurities = positionKeys.difference(cachePositions)
    # putSecurities = positionKeys.intersection(cachePositions)

    positions = [{**val,
                  "security": val["symbol"],
                  "onDate": datetime.today(),
                  "timestamp": datetime.now()}
                 for val in positions.values()]
    positions = PositionsSchema().dump(positions, many=True)
    postPositions = [val for val in positions
                     if val["security"] in postSecurities]
    if postPositions:
        api.post(url, postPositions)
    # putPositions = [val for val in positions
    #                 if val["security"] in putSecurities]


    # api.put(url, putPositions)
