from app.models.nse import (AdvanceDeclineCollection,
                            CumulativeDerivativesCollection,
                            EventsCalendarCollection,
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
     'index': ['security', 'expiryDate', '+timestamp']},
    {'collection': EquityDerivatesCollection,
     'index': ['identifier', 'expiryDate', '+timestamp']},
    {'collection': EventsCalendarCollection,
     'index': ['security', 'purpose', '+eventDate']},
    {'collection': FiiDiiCollection,
     'index': ['category', '+onDate']},
    {'collection': HistoricalDerivatesCollection,
     'index': ['security', '+onDate', '+expiryDate']},
    {'collection': IndexDerivativesCollection,
     'index': ['identifier', 'expiryDate', '+timestamp']},
    {'collection': NiftyEquityCollection,
     'index': ['identifier', '+lastUpdateTime']},
    {'collection': SecurityInFocusCollection,
     'index': ['security', '+timestamp']},
]


def ensure_index():
    for item in COLL_INDEXES:
        collection = item['collection']
        index = item['index']
        collection.ensure_index(index, unique=True)
