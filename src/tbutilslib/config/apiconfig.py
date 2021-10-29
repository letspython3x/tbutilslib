"""Config."""
import os


class NseApiConfig:
    """Configuration for NSE."""

    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/80.0.3987.149 Safari/537.36',
               'accept-language': 'en,gu;q=0.9,hi;q=0.8',
               'accept-encoding': 'gzip, deflate, br',
               'Content-Type': 'application/json; charset=utf-8',
               }
    BASE_URL = 'https://www.nseindia.com/'
    BASE_PATH = 'https://www.nseindia.com/api/'
    # EQUITY_OC_PATH = "quote-derivative?symbol={}"
    QUOTE_DERIVATIVES = "quote-derivative?symbol={}"
    HISTORY_DERIVATIVES = "historical/fo/derivatives"
    EQUITY_QUOTE = "quote-equity?symbol={}"
    EQUITY_PATH = "{}"  # TO BE FILLED IN
    EVENT_CALENDAR_PATH = "event-calendar"
    FII_DII = "fiidiiTradeReact"
    # MARKET DATA
    NIFTY_EQUITIES_PATH = "equity-stockIndices?index=NIFTY%2050"
    MARKET_STATUS = "marketStatus"
    INDEXES = ["NIFTY", "BANKNIFTY"]
    # Not using currently
    INDEX_OC_PATH = "option-chain-indices?symbol={}"


class TbApiConfig:
    """Configuration for API."""

    BASE_URL = r"/api/v1"
    MSG_400 = (
        "The request is missing one or more elements, or the values of some ",
        "elements are invalid: {error}")
    MSG_401 = (
        "You are not authorized to complete this operation. This error ",
        "can occur if the request is submitted with an invalid authentication ",
        "token.")
    MSG_403 = (
        "The request was valid, but the server is refusing to respond because ",
        "you do not have permission to access the requested resource. Submit ",
        "a request to your account administrator to determine how to gain ",
        "access.")
    MSG_404 = "Token not valid."
    MSG_409 = "Record Exists Duplicate Entry: {error}."
    MGS_501 = (
        "The request method is not supported by the server and cannot be ",
        "handled")
    MSG_503 = "Unable to delete record: {error}"
    ERRORS = {
        "ClientBadRequest": {"message": MSG_400, "status": 400},
        "ClientNotAuthorized": {"message": MSG_401, "status": 401},
        "ClientNotPermitted": {"message": MSG_403, "status": 403},
        "ResourceAlreadyExists": {"message": MSG_409, "status": 409}
    }
    FINANCIAL_RESULTS = 'financial results'
    INDEXES = ["NIFTY", "BANKNIFTY"]


class TbApiPathConfig:
    """Trading Bot Api Path Config."""

    headers = {'Content-Type': 'application/json; charset=utf-8'}
    BASE_URI = os.getenv('ENVIRONMENT', 'http://0.0.0.0/api/v1/')
    EVENTS_PATH = "events"
    SECURITY_IN_FOCUS = "securityInFocus"
    MAX_OI = "maxOpenInterest"
    EXPIRY_DATES = "expiryDates"
    FII_DII = "fiidii"
    ADV_DECLINE = "advanceDecline"
    INDEX_DERIVATIVES = "index/derivatives"
    EQUITY_DERIVATIVES = "equity/derivatives"
    CUMULATIVE_DERIVATIVES = "cumulative"
    HISTORICAL_DERIVATIVES = "historical/derivatives"
    EQUITY = "equity"


class Config:
    """Configuration for App."""

    DEBUG = os.getenv("DEBUG", True)
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    CORS_HEADERS = 'Content-Type'
