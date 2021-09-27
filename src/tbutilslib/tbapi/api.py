import functools

import requests
from requests.exceptions import ReadTimeout, HTTPError, RequestException
from tbutilslib.config.apiconfig import TbApiPathConfig
from urllib3.exceptions import ReadTimeoutError


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
    def __init__(self, url=None):
        self._session = None
        self._cookies = None
        self.uri = TbApiPathConfig.BASE_URI
        self.url = url

    @property
    def session(self):
        if not self._session:
            self._session = requests.Session()
        return self._session

    @request_decorator
    def get(self, url, params=None, headers=None):
        url = url or self.url
        headers = headers or {}
        headers = {**headers, **TbApiPathConfig.headers}
        return self.session.get(url, headers=headers, params=params)

    @request_decorator
    def post(self, url, data, headers=None):
        if not data:
            return
        url = url or self.url
        headers = headers or {}
        headers = {**headers, **TbApiPathConfig.headers}
        return self.session.post(url, json=data, headers=headers)

    @request_decorator
    def put(self, url, data, headers=None):
        url = url or self.url
        headers = headers or {}
        headers = {**headers, **TbApiPathConfig.headers}
        return self.session.put(url, json=data, headers=headers)

    @request_decorator
    def delete(self, url, headers=None):
        headers = headers or {}
        headers = {**headers,
                   **TbApiPathConfig.headers,
                   'X-Force-Delete': 'true'}
        return self.session.delete(url, headers=headers)
