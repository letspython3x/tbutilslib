"""Base Collection."""
from logging import getLogger

from flask_restful import abort
from mongoengine import Document
from mongoengine.errors import NotUniqueError
from pymongo.errors import DuplicateKeyError

logger = getLogger("tbutilslib." + __name__)

BASE_META = {
    "strict": False,
    "ordered": True,
    "index_background": True,
    "auto_create_index": False,  # To avoid index creation on every insert
    "indexes": [],
}


class BaseCollection(Document):
    """Base DB collection with a few things added."""

    meta = {"abstract": True, "allow_inheritance": True}

    def save(
        self,
        force_insert=False,
        validate=True,
        clean=True,
        write_concern=None,
        cascade=None,
        cascade_kwargs=None,
        _refs=None,
        save_condition=None,
        signal_kwargs=None,
        **kwargs
    ):
        """FIX IT."""
        try:
            super().save(
                force_insert=force_insert,
                validate=validate,
                clean=clean,
                write_concern=write_concern,
                cascade=cascade,
                cascade_kwargs=cascade_kwargs,
                _refs=_refs,
                save_condition=save_condition,
                signal_kwargs=signal_kwargs,
                **kwargs
            )
        except (NotUniqueError, DuplicateKeyError):
            logger.info("Error: Duplicate, record already exists")
            raise abort(409, message="Record Exists Duplicate Entry.")
