from datetime import date

from fastapi import HTTPException, status

from app.analytics.pace_calculator import calculate_pace_seconds, calculate_speed_kmh
from app.models.run import Run
from app.repositories.run_repository import RunRepository
from app.repositories.user_repository import UserRepository
from app.schemas.run_schema import RunCreate


class RunService:
    """Business logic for run workflows."""

    def __init__(self, db):
        self.run_repo = RunRepository(db)
        self.user_repo = UserRepository(db)

    def create_run(self, payload: RunCreate) -> Run:
        user = self.user_repo.get_by_id(payload.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

        avg_pace_seconds = calculate_pace_seconds(payload.duration_seconds, payload.distance_km)
        speed_kmh = calculate_speed_kmh(payload.duration_seconds, payload.distance_km)

        run = Run(
            id=None,
            user_id=payload.user_id,
            date=payload.date,
            distance_km=payload.distance_km,
            duration_seconds=payload.duration_seconds,
            avg_pace_seconds=avg_pace_seconds,
            avg_speed_kmh=speed_kmh,
            avg_heart_rate=payload.avg_heart_rate,
            elevation_gain=payload.elevation_gain,
            route_file=payload.route_file,
            notes=payload.notes,
        )
        return self.run_repo.create(run)

    def list_runs(
        self,
        user_id: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        min_distance_km: float | None = None,
        max_distance_km: float | None = None,
    ) -> list[Run]:
        return self.run_repo.list(user_id, start_date, end_date, min_distance_km, max_distance_km)

    def get_run_or_404(self, run_id: str) -> Run:
        run = self.run_repo.get_by_id(run_id)
        if not run:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Run not found')
        return run
