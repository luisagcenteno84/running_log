from __future__ import annotations

import datetime as dt
from dataclasses import dataclass


@dataclass(slots=True)
class Run:
    id: str | None
    user_id: str
    date: dt.date
    distance_km: float
    duration_seconds: int
    avg_pace_seconds: float
    avg_speed_kmh: float
    avg_heart_rate: int | None = None
    elevation_gain: float | None = None
    route_file: str | None = None
    notes: str | None = None
    created_at: dt.datetime | None = None
