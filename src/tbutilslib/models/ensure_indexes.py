"""Ensure Indexes."""
from tbutilslib.models import (AdvanceDeclineCollection,
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
                               PositionsCollection)

COLL_INDEXES = [
    {'collection': AdvanceDeclineCollection,
     'index': ['timestamp']},
    {'collection': CumulativeDerivativesCollection,
     'index': ['security', 'expiryDate', '-timestamp']},
    {'collection': EquityDerivatesCollection,
     'index': ['identifier', 'expiryDate', '-timestamp']},
    {'collection': ExpiryDatesCollection,
     'index': ['securityType', '-timestamp']},
    {'collection': EventsCollection,
     'index': ['security', 'purpose', '-eventDate']},
    {'collection': FiiDiiCollection,
     'index': ['category', '-onDate']},
    {'collection': HistoricalDerivatesCollection,
     'index': ['security', '-onDate', '+expiryDate']},
    {'collection': IndexDerivativesCollection,
     'index': ['identifier', 'expiryDate', '-timestamp']},
    {'collection': NiftyEquityCollection,
     'index': ['identifier', '-lastUpdateTime']},
    {'collection': SecurityInFocusCollection,
     'index': ['+security', '-onDate']},
    {'collection': OrdersCollection,
     'index': ['+security', '-timestamp']},
    {'collection': PositionsCollection,
     'index': ['+security', '-onDate', '-timestamp']},
]


def ensure_index():
    """Set indexes for collections."""
    for item in COLL_INDEXES:
        collection = item['collection']
        index = item['index']
        collection.create_index(index, unique=True)
