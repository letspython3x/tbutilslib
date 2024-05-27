"""Database."""
import csv
import os
from logging import getLogger

from mongoengine import connect
from mongoengine.connection import ConnectionFailure
from tbutilslib.config.database import MongoConfig

from src.tbutilslib.models import FiiDiiCollection
from src.tbutilslib.models.nse.equities import EquityMetaCollection
from src.tbutilslib.schema import FiiDiiSchema
from src.tbutilslib.schema.nse.equity import EquityMetaSchema

logger = getLogger("app." + __name__)
nifty_500_list = "Nifty500_list.csv"
fii_dii_cash = "fii_dii_cash.csv"


def mongo_connect():
    """Connect to mongo database."""
    try:
        return connect(
            (
                "mongoenginetest"
                if os.getenv("TESTING", "False") == "True"
                else MongoConfig.MONGODB_DB
            ),
            host=(
                "mongomock://localhost"
                if os.getenv("TESTING", "False") == "True"
                else MongoConfig.MONGODB_URI
            ),
        )
    except ConnectionFailure as err:
        logger.info("Database connection error.", exc_info=True)


def load_nifty_500():
    """Load nifty 500 list."""
    schema = EquityMetaSchema()
    model = EquityMetaCollection

    with open(nifty_500_list, "r") as fin:
        reader = csv.DictReader(fin)
        data = list(reader)

    marshal_data = schema.load(data, many=True)
    data = [model(**datum) for datum in marshal_data]
    model.objects.insert(data)


def load_fii_dii():
    """Load FII and DII csv."""

    schema = FiiDiiSchema()
    model = FiiDiiCollection

    with open(fii_dii_cash, "r") as fin:
        reader = csv.DictReader(fin)
        data = list(reader)

    marshal_data = schema.load(data, many=True)
    data = [model(**datum) for datum in marshal_data]
    model.objects.insert(data)


if __name__ == "__main__":
    mongo_connect()
    load_nifty_500()
    load_fii_dii()
