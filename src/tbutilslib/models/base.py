from flask_mongoengine import Document
from flask_restful import abort

from app.config import MongoConfig

from mongoengine.errors import NotUniqueError
from pymongo.errors import DuplicateKeyError

BASE_META = {'strict': False,
             'ordered': True,
             'index_background': True,
             'auto_create_index': False,
             'indexes': []}


class BaseCollection(Document):
    """Base DB collection with a few things added."""

    meta = {"abstract": True, 'allow_inheritance': True}

    def save(self, force_insert=False, validate=True, clean=True,
             write_concern=None, cascade=None, cascade_kwargs=None, _refs=None,
             save_condition=None, signal_kwargs=None, **kwargs):
        """FIX IT."""
        try:
            super().save(force_insert=force_insert, validate=validate,
                         clean=clean, write_concern=write_concern,
                         cascade=cascade, cascade_kwargs=cascade_kwargs,
                         _refs=_refs, save_condition=save_condition,
                         signal_kwargs=signal_kwargs, **kwargs)
        except (NotUniqueError, DuplicateKeyError):
            raise abort(409, message="Record Exists Duplicate Entry.")
