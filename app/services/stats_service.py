from datetime import date, timedelta

from app.analytics.pace_calculator import format_pace
from app.analytics.personal_records import detect_personal_bests
from app.analytics.training_load import weekly_training_load
from app.repositories.run_repository import RunRepository


class StatsService:
    """Business logic for aggregate training statistics."""

    def __init__(self, db):
        self.run_repo = RunRepository(db)

    def summary(self, user_id: str | None = None, today: date | None = None) -> dict:
        today = today or date.today()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)

        runs = self.run_repo.list(user_id=user_id)
        if not runs:
            return {
                'total_distance_km': 0.0,
                'weekly_mileage_km': 0.0,
                'average_pace': '0:00/km',
                'fastest_run_id': None,
                'longest_run_id': None,
                'training_frequency': 0,
            }

        total_distance = round(sum(run.distance_km for run in runs), 2)
        avg_pace_seconds = sum(run.avg_pace_seconds for run in runs) / len(runs)
        weekly = weekly_training_load(runs, week_start, week_end)
        prs = detect_personal_bests(runs)

        return {
            'total_distance_km': total_distance,
            'weekly_mileage_km': weekly['weekly_distance_km'],
            'average_pace': format_pace(avg_pace_seconds),
            'fastest_run_id': prs['fastest_run_id'],
            'longest_run_id': prs['longest_run_id'],
            'training_frequency': weekly['training_frequency'],
        }
