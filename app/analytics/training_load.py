from datetime import date
from typing import Iterable

from app.analytics.pace_calculator import format_pace
from app.models.run import Run


def weekly_mileage(runs: Iterable[Run], week_start: date, week_end: date) -> float:
    """Return total distance for runs between week_start and week_end inclusive."""
    return round(
        sum(run.distance_km for run in runs if week_start <= run.date <= week_end),
        2,
    )


def weekly_training_load(runs: Iterable[Run], week_start: date, week_end: date) -> dict[str, float | int | str]:
    """Aggregate weekly distance, average pace, and run count."""
    weekly_runs = [run for run in runs if week_start <= run.date <= week_end]
    if not weekly_runs:
        return {'weekly_distance_km': 0.0, 'average_pace': '0:00/km', 'training_frequency': 0}

    total_distance = sum(run.distance_km for run in weekly_runs)
    avg_pace_seconds = sum(run.avg_pace_seconds for run in weekly_runs) / len(weekly_runs)
    return {
        'weekly_distance_km': round(total_distance, 2),
        'average_pace': format_pace(avg_pace_seconds),
        'training_frequency': len(weekly_runs),
    }
