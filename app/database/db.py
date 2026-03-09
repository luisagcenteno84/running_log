from collections.abc import Generator
from functools import lru_cache
import os

from google.auth.credentials import AnonymousCredentials
from google.cloud import firestore

from app.config import get_settings


@lru_cache
def get_firestore_client() -> firestore.Client:
    settings = get_settings()
    emulator_host = os.getenv('FIRESTORE_EMULATOR_HOST')

    if emulator_host:
        if not settings.google_cloud_project:
            raise RuntimeError('FIRESTORE_EMULATOR_HOST is set, but GOOGLE_CLOUD_PROJECT is missing.')
        return firestore.Client(
            project=settings.google_cloud_project,
            credentials=AnonymousCredentials(),
        )

    kwargs = {}
    if settings.google_cloud_project:
        kwargs['project'] = settings.google_cloud_project
    return firestore.Client(**kwargs)


def get_db() -> Generator[firestore.Client, None, None]:
    yield get_firestore_client()


def init_db() -> None:
    """Firestore is schemaless, so there is no startup migration step."""
    return None
