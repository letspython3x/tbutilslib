class TradingBotAPIException(Exception):
    """General TradingBot API exception."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InvalidSecurityError(Exception):
    """InValid Security"""
