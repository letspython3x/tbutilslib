import requests
from pymongo import MongoClient
from config.config import DbConfig
from cacheData import NiftyOptionData as cache
import time

URL = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json; charset=utf-8",
    "Accept-Language": "en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-GB;q=0.6,en-US;q=0.5",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36",
    # 'Cookie': 'DFE623D3EEC65BAFA58B221214B59409~PaGg27TsDYO6vn05CwgbAVCiiYVY99be6NEU6fDqKcFjY6+R7ss51qg0Fbt3yFnyOXZ78nQrjnM8hipmFqAKF6BhNbnpShiBjjX3slNZRQUiIViUrSjOiUPCGcbI+iFmdnayL9D9cyR9sGVBF3T5nAHipK8FNkwxXIwkAWEedQ0='
}

from json import loads

stars = "*" * 100


def get_data():
    res = requests.get(URL, headers=HEADERS)
    print(f"STATUS CODE: {res.status_code}")
    if res.status_code == 200:
        return loads(res.text)
    # else:
    #     print("using cache data")
    #     return loads(cache.options)


def massage_option_data(data):
    records = data.get("records")
    expiryDates = records.get("expiryDates")
    underlyingValue = records.get("underlyingValue")
    timestamp = records.get("timestamp")
    strikePrices = records.get("strikePrices")
    recordsData = records.get("data")

    filtered = data.get("filtered")
    totOICE = filtered.get("CE").get("totOI")
    totVolCE = filtered.get("CE").get("totVol")
    totOIPE = filtered.get("PE").get("totOI")
    totVolPE = filtered.get("PE").get("totVol")
    filteredData = filtered.get("data")

    print(f"{stars} \n\tRECORDS at {timestamp} ")
    msg = (
        f"\nexpiryDates: {expiryDates}"
        f"\nunderlyingValue: {underlyingValue}"
        f"\nstrikePrices: {strikePrices}"
        f"\nrecordsData: {len(recordsData)}"
    )
    print(f"{msg}\n{stars}")

    print(f"{stars} \n\tfiltered DATA at {timestamp} ")
    msg = (
        f"\ntotOICE: {totOICE}"
        f"\ntotVolCE: {totVolCE}"
        f"\ntotOIPE: {totOIPE}"
        f"\ntotVolPE: {totVolPE}"
        f"\nfilteredData: {len(filteredData)}"
    )
    print(f"{msg}\n{stars}")


def save_filtered_data(data):
    records = data.get("records")
    timestamp = records.get("timestamp")
    underlyingValue = records.get("underlyingValue")
    minStrikePrice, maxStrikePrice = underlyingValue - 500, underlyingValue + 500
    filtered = data.get("filtered")
    totOICE = filtered.get("CE").get("totOI")
    totVolCE = filtered.get("CE").get("totVol")
    totOIPE = filtered.get("PE").get("totOI")
    totVolPE = filtered.get("PE").get("totVol")
    filteredData = filtered.get("data")

    print(f"Data TimeStamp at : {timestamp}")
    # for datum in filteredData:
    docs = [
        {**value, "timestamp": timestamp, "type": key}
        for datum in filteredData
        for key, value in datum.items()
        if key in ("PE", "CE")
        and (minStrikePrice < value.get("strikePrice") < maxStrikePrice)
    ]

    if docs:
        print(f"SAVING LENGTH: {len(docs)}")
        save(data=docs)

        # for key, value in datum.items():
        #     print(value)
        #     if key in ("PE", "CE") and (minunderlyingValue < value.get(
        #             "strikePrice") < maxunderlyingValue):
        #         doc = {**value, 'timestamp': timestamp, 'type': key}
        #         print(doc)
        #         # save(data=doc)

        # save(data=docs)


def save(collectionName="nifty50_options", data: any = None):
    with MongoClient(DbConfig.HOST, DbConfig.PORT) as client:
        db = client[DbConfig.DB]
        item = db[collectionName]
        # data_id = item.insert_one(data).inserted_id
        if isinstance(data, list):
            item.insert_many(data)
        else:
            item.insert_one(data)


def main():
    while True:
        currTime = time.strftime("%d:%m:%Y %H:%M:%S", time.localtime())
        print(f"{stars}\nRunning at {currTime}")
        data = get_data()
        if data:
            # massage_option_data(data)
            save_filtered_data(data)
        time.sleep(60)


if __name__ == "__main__":
    main()
