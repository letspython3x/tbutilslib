import json
import os
from typing import Dict, List
from urllib.parse import urljoin

from tbutilslib.config.apiconfig import TbApiPathConfig
from tbutilslib.tbapi.api import TbApi
from tbutilslib.utils.common import TODAY, parse_timestamp

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


def get_most_traded_securities_by_value(count=3):
    api = TbApi()
    url = urljoin(TbApiPathConfig.BASE_URI, TbApiPathConfig.EQUITY)
    url = f"{url}/{TODAY}"
    cache = api.get(url)
    items = cache.get('items')[0] if cache else []
    latestTs = max([parse_timestamp(item["timestamp"]) for item in items])
    latestTsPayload = [item for item in items if item["timestamp"] == latestTs]
    latestTsPayload.sort(key=lambda x: x["totalTradedValue"])
    return latestTsPayload[:count]
