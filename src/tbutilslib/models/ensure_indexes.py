"""Ensure Indexes."""

from tbutilslib.models import (
    AdvanceDeclineCollection,
    CumulativeDerivativesCollection,
    EventsCollection,
    EquityDerivatesCollection,
    ExpiryDatesCollection,
    FiiDiiCollection,
    HistoricalDerivatesCollection,
    IndexDerivativesCollection,
    NiftyEquityCollection,
    SecurityInFocusCollection,
    OrdersCollection,
    PositionsCollection,
)

COLL_INDEXES = [
    {"collection": AdvanceDeclineCollection, "index": ["timestamp"]},
    {
        "collection": CumulativeDerivativesCollection,
        "index": ["security", "expiry_date", "-timestamp"],
    },
    {
        "collection": EquityDerivatesCollection,
        "index": ["identifier", "expiry_date", "-timestamp"],
    },
    {"collection": ExpiryDatesCollection, "index": ["security_type", "-timestamp"]},
    {"collection": EventsCollection, "index": ["security", "purpose", "-event_date"]},
    {"collection": FiiDiiCollection, "index": ["category", "-on_date"]},
    {
        "collection": HistoricalDerivatesCollection,
        "index": ["security", "-on_date", "+expiry_date"],
    },
    {
        "collection": IndexDerivativesCollection,
        "index": ["identifier", "expiry_date", "-timestamp"],
    },
    {"collection": NiftyEquityCollection, "index": ["identifier", "-last_update_time"]},
    {"collection": SecurityInFocusCollection, "index": ["+security", "-on_date"]},
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
