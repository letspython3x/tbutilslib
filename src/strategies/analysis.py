import time
from datetime import datetime, timedelta

from pymongo import MongoClient

from app.config import MongoConfig, ApiConfig
from app.errors import InvalidSecurityError
from app.utils.common import (
    EnumIndicator,
    TODAY,
    END_TIME,
    START_TIME,
    DATE_FORMAT,
    FULL_TS_FORMAT,
)


# from app.utils.common import is_trading_hours_open
# TODAY = "12-02-2021"


class Db:
    def __init__(self, security="", collectionName=None):
        self.security = security.upper()
        self._collectionName = collectionName
        self.query = {"security": self.security}

    @property
    def collectionName(self):
        """
        set the mongo db collection name as per the security.
        """
        if self._collectionName is None:
            if self.security in ApiConfig.EQUITIES:
                self._collectionName = MongoConfig.EQUITY_DERIVATIVES
            elif self.security in ApiConfig.INDEXES:
                self._collectionName = MongoConfig.INDEX_DERIVATIVES
            else:
                raise InvalidSecurityError(f"Invalid Security: {self.security}")

        return self._collectionName

    def get(
        self, query, key="", sortFlag=False, ascend=True, projection=None, distinct=None
    ):
        """
        Fetches the data from database collection as per the given query.
        """
        projection = projection or {"_id": 0, "_cls": 0}
        with MongoClient(MongoConfig.HOST, MongoConfig.PORT) as client:
            db = client[MongoConfig.MONGODB_DB]
            item = db[self.collectionName]
            # print(query, self.collectionName)
            if sortFlag:
                order = 1 if ascend else -1
                # print(query)
                data = item.find(query, projection).sort(key, order)
            elif distinct:
                data = item.find(query, projection).distinct(key)
            else:
                data = item.find(query, projection)
        # data = [d for d in data]
        # print("HERE : "+ str(data))
        return list(data) if data else None

    @staticmethod
    def append_expiry_date(query, eDate):
        if eDate:
            query.update({"expiryDate": datetime.strptime(eDate, DATE_FORMAT)})

    @staticmethod
    def parse_dates_to_str(data, key, format=DATE_FORMAT):
        return [{**item, key: item.get(key).strftime(format)} for item in data]

    @staticmethod
    def get_day_range():
        gtTime, lsTime = (
            f"{TODAY} {START_TIME}",
            f"{TODAY} {END_TIME}",
        )
        return gtTime, lsTime

    @staticmethod
    def get_timestamps(timeframe):
        format = "%d-%b-%Y %H:%M:%S"
        currTime = time.strftime("%H:%M:%S", time.localtime())
        if currTime > END_TIME:
            dayEnd = f"{TODAY} {END_TIME}"
            lsTime = f"{TODAY} 15:27:00"
            return dayEnd, lsTime

        NOW = datetime.now()
        lsTime = NOW - timedelta(minutes=timeframe)
        return NOW.strftime(format), lsTime.strftime(format)

    def get_derivatives_data(self, strikePrice=None, expiryDate=None):
        """
        Get the derivatives data
        """
        gte = datetime.strptime(TODAY, DATE_FORMAT)
        self.query.update({"timestamp": {"$gte": gte}})
        if strikePrice:
            self.query.update({"strikePrice": int(strikePrice)})
        self.append_expiry_date(self.query, expiryDate)
        print(self.query)
        data = self.get(self.query, key="timestamp", sortFlag=True)
        data = self.parse_dates_to_str(data, key="timestamp", format=FULL_TS_FORMAT)
        data = self.parse_dates_to_str(data, key="expiryDate")
        return data

    def get_cumulative_data(self, expiryDate=None):
        """
        Returns the cumulative data with put-call ratio (pcr)
        """
        self._collectionName = MongoConfig.CUMULATIVE_DERIVATIVES
        self.query.update(
            {"timestamp": {"$gte": datetime.strptime(TODAY, DATE_FORMAT)}}
        )
        self.append_expiry_date(self.query, expiryDate)
        # print(self.query)
        data = self.get(self.query)
        data = self.parse_dates_to_str(data, key="timestamp", format=FULL_TS_FORMAT)
        data = self.parse_dates_to_str(data, key="expiryDate")
        # print(data[0])
        return data

    def get_events(self, from_date=None, to_date=None, **kwargs):
        """
        Returns the events between the mentioned dates or
        Post current date.
        """
        key = "eventDate"
        from_date = from_date or kwargs.get("from_date")
        to_date = to_date or kwargs.get("to_date")
        from_date = datetime.strptime(from_date, "%d-%m-%Y") if from_date else from_date
        to_date = datetime.strptime(to_date, "%d-%m-%Y") if to_date else to_date

        if from_date and to_date:
            query = {key: {"$gte": from_date, "$lte": to_date}}
        elif from_date:
            query = {key: {"$gte": from_date}}
        else:
            query = {key: {"$gte": TODAY}}

        data = self.get(query, key=key, sortFlag=True)
        data = self.parse_dates_to_str(data, key="eventDate")
        return data

    def get_last_value_of_security(self, security, key="timestamp", projection=None):
        """
        Get the last value of the security from database.
        """
        query = {"security": security}
        projection = projection or {"_id": 0}
        data = self.get(
            query=query, key=key, ascend=False, projection=projection, sortFlag=True
        )
        return data[0][key]

    def get_max_oi(self, expiryDate=None, timeframe=3):
        """
        params:
        expiryDate:
        timeframe: Default 3 min

        Returns the strikePrice and value of OpenInterest
        for which we have maximum open interest for both PUT and CALL
        for the equity on mentioned expiryDate.
        """

        if expiryDate and isinstance(expiryDate, str):
            expiryDate = datetime.strptime(expiryDate, DATE_FORMAT)
        else:
            expiryDate = datetime.strptime("25-02-2021", DATE_FORMAT)
        projection = {"_id": 0, "timestamp": 1}
        latestTs = self.get_last_value_of_security(self.security, projection=projection)

        self.query.update(
            {
                "timestamp": {
                    "$gte": latestTs - timedelta(minutes=timeframe),
                    "$lte": latestTs + timedelta(minutes=timeframe),
                },
                "expiryDate": {"$eq": expiryDate},
            }
        )
        projection = {"_id": 0, "strikePrice": 1, "openInterest": 1, "optionType": 1}
        data = self.get(
            query=self.query,
            projection=projection,
            key="openInterest",
            sortFlag=True,
            ascend=False,
        )
        # print(data)
        peData = [datum for datum in data if datum.get("optionType") == "PE"]
        ceData = [datum for datum in data if datum.get("optionType") == "CE"]
        payload = {}
        if peData and ceData:
            payload = {
                "resistance": ceData[0],
                "support": peData[0],
            }
        return payload

    def get_expiry_dates(self):
        """
        Get the next expiry dates for the security.
        """
        key = "expiryDate"
        self.query.update({key: {"$gte": datetime.strptime(TODAY, DATE_FORMAT)}})
        # print(self.query)
        projection = {"_id": 0, key: 1}
        data = self.get(query=self.query, projection=projection, distinct=True, key=key)
        # print(data)
        payload = {}
        for pos, item in enumerate(data):
            if pos == 0:
                payload["current"] = item.strftime("%d-%m-%Y")
            else:
                payload["current+" + str(pos)] = item.strftime("%d-%m-%Y")

        return payload

    def get_equity_data(self, tsDate=None):
        dt = datetime.strptime(tsDate or TODAY, DATE_FORMAT)
        lte = dt + timedelta(days=1)
        self.query.update({"timestamp": {"$gt": dt, "$lt": lte}})
        data = self.get(self.query)
        data = self.parse_dates_to_str(data, key="timestamp")
        return data

    def get_security_names_in_focus(self, tsDate=None):
        """
        Get the names of securities which are in focus today (some other date).
        Fetch distinct securities from MongoConfig.EQUITY_DERIVATIVES
        for today (or date)
        """
        key = "security"
        dt = datetime.strptime(tsDate or TODAY, DATE_FORMAT)
        lt = dt + timedelta(days=1)
        query = {"timestamp": {"$gt": dt, "$lt": lt}}
        projection = {"_id": 0, key: 1}
        # print(query)
        data = self.get(query=query, projection=projection)
        data = sorted(list(set([datum[key] for datum in data])))
        return data

    @staticmethod
    def trendline(index, data, order=1):
        """
        if the slope is a +ve value --> increasing trend
        if the slope is a -ve value --> decreasing trend
        if the slope is a zero value --> No trend
        """

        # coeffs = np.polyfit(index, data, order)
        slope = 0  # coeffs[-2]
        # print(slope)
        return float(slope)

    def check_indicator(self, data):
        timestamp = [datum["timestamp"] for datum in data]
        openInterest = [datum["totOiCe"] for datum in data]
        trendOi = self.trendline(timestamp, openInterest)
        price = [datum["spotPrice"] for datum in data]
        trendPrice = self.trendline(timestamp, price)
        if trendPrice > 0:
            if trendOi > 0:
                indicator = EnumIndicator.LONG
            else:
                indicator = EnumIndicator.SHORT_COVERING
        else:
            if trendOi > 0:
                indicator = EnumIndicator.SHORT
            else:
                indicator = EnumIndicator.LONG_UNWINDING

        return indicator.value
