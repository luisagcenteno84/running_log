from __future__ import annotations

import datetime as dt
from dataclasses import dataclass


@dataclass(slots=True)
class User:
    id: str | None
    name: str
    email: str
    password_hash: str | None = None
    created_at: dt.datetime | None = None
