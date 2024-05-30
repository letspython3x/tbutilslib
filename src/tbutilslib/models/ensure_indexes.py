"""Ensure Indexes."""

from tbutilslib.models import (
    AdvanceDeclineCollection,
    CumulativeDerivativesCollection,
    EventsCollection,
    EquityDerivatesCollection,
    FiiDiiCollection,
    HistoricalDerivatesCollection,
    IndexDerivativesCollection,
    NiftyEquityCollection,
    IndexCollection,
    OrdersCollection,
    PositionsCollection,
    OptionMetaDataCollection,
)

COLL_INDEXES = [
    {"collection": AdvanceDeclineCollection, "index": ["timestamp"]},
    {
        "collection": CumulativeDerivativesCollection,
        "index": ["security", "expiry_date", "-on_date", "-timestamp"],
    },
    {
        "collection": EquityDerivatesCollection,
        "index": [
            "security",
            "strike_price",
            "option_type",
            "expiry_date",
            "-timestamp",
        ],
    },
    {"collection": EventsCollection, "index": ["security", "purpose", "-event_date"]},
    {"collection": FiiDiiCollection, "index": ["category", "-on_date"]},
    {
        "collection": HistoricalDerivatesCollection,
        "index": ["security", "-on_date", "+expiry_date"],
    },
    {
        "collection": IndexDerivativesCollection,
        "index": [
            "security",
            "strike_price",
            "option_type",
            "expiry_date",
            "-timestamp",
        ],
    },
    {"collection": NiftyEquityCollection, "index": ["identifier", "-timestamp"]},
    {"collection": IndexCollection, "index": ["security", "-timestamp"]},
    {"collection": OptionMetaDataCollection, "index": ["+security", "-on_date"]},
    {"collection": OrdersCollection, "index": ["+security", "-timestamp"]},
    {
        "collection": PositionsCollection,
        "index": ["+security", "-on_date", "-timestamp"],
    },
]


def ensure_index():
    """Set indexes for collections."""
    for item in COLL_INDEXES:
        collection = item["collection"]
        index = item["index"]
        collection.create_index(index, unique=True)
