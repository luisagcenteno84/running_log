from __future__ import annotations

from collections.abc import Generator
from copy import deepcopy
import uuid

import pytest
from fastapi.testclient import TestClient

from app.database.db import get_db
from app.main import app


class FakeDocumentSnapshot:
    def __init__(self, doc_id: str, data: dict | None):
        self.id = doc_id
        self._data = deepcopy(data) if data is not None else None

    @property
    def exists(self) -> bool:
        return self._data is not None

    def to_dict(self) -> dict | None:
        return deepcopy(self._data)


class FakeDocumentReference:
    def __init__(self, collection: 'FakeCollection', doc_id: str):
        self.collection = collection
        self.id = doc_id

    def set(self, data: dict) -> None:
        self.collection.documents[self.id] = deepcopy(data)

    def get(self) -> FakeDocumentSnapshot:
        return FakeDocumentSnapshot(self.id, self.collection.documents.get(self.id))


class FakeCollection:
    def __init__(self):
        self.documents: dict[str, dict] = {}

    def document(self, doc_id: str | None = None) -> FakeDocumentReference:
        return FakeDocumentReference(self, doc_id or uuid.uuid4().hex)

    def stream(self):
        for doc_id, data in list(self.documents.items()):
            yield FakeDocumentSnapshot(doc_id, data)


class FakeFirestoreClient:
    def __init__(self):
        self.collections: dict[str, FakeCollection] = {}

    def collection(self, name: str) -> FakeCollection:
        if name not in self.collections:
            self.collections[name] = FakeCollection()
        return self.collections[name]


@pytest.fixture
def fake_db() -> FakeFirestoreClient:
    return FakeFirestoreClient()


@pytest.fixture(autouse=True)
def override_firestore(fake_db: FakeFirestoreClient) -> Generator[None, None, None]:
    def _override_get_db() -> Generator[FakeFirestoreClient, None, None]:
        yield fake_db

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
