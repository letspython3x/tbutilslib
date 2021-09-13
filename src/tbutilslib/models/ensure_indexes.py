"""Ensure Indexes."""
from tbutilslib.models import (AdvanceDeclineCollection,
                               CumulativeDerivativesCollection,
                               EventsCollection,
                               EquityDerivatesCollection,
                               FiiDiiCollection,
                               HistoricalDerivatesCollection,
                               IndexDerivativesCollection,
                               NiftyEquityCollection,
                               SecurityInFocusCollection)

COLL_INDEXES = [
    {'collection': AdvanceDeclineCollection,
     'index': ['timestamp']},
    {'collection': CumulativeDerivativesCollection,
     'index': ['security', 'expiryDate', '-timestamp']},
    {'collection': EquityDerivatesCollection,
     'index': ['identifier', 'expiryDate', '-timestamp']},
    {'collection': EventsCollection,
     'index': ['security', 'purpose', '+eventDate']},
    {'collection': FiiDiiCollection,
     'index': ['category', '-onDate']},
    {'collection': HistoricalDerivatesCollection,
     'index': ['security', '-onDate', '+expiryDate']},
    {'collection': IndexDerivativesCollection,
     'index': ['identifier', 'expiryDate', '-timestamp']},
    {'collection': NiftyEquityCollection,
     'index': ['identifier', '-lastUpdateTime']},
    {'collection': SecurityInFocusCollection,
     'index': ['security', '-onDate']},
]


def ensure_index():
    """Set indexes for collections."""
    for item in COLL_INDEXES:
        collection = item['collection']
        index = item['index']
        collection.ensure_index(index, unique=True)
