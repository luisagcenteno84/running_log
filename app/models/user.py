from __future__ import annotations

import datetime as dt
from dataclasses import dataclass


@dataclass(slots=True)
class User:
    id: str | None
    name: str
    email: str
    password_hash: str | None = None
    goal_weekly_distance_km: float | None = None
    goal_avg_pace_seconds: float | None = None
    goal_training_frequency: int | None = None
    created_at: dt.datetime | None = None
