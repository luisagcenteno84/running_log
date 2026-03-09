from __future__ import annotations

from datetime import date, datetime, timezone

from app.models.run import Run


class RunRepository:
    """Persistence operations for runs backed by Firestore."""

    def __init__(self, db):
        self.db = db
        self.collection = db.collection('runs')

    def _to_model(self, document) -> Run | None:
        if not document.exists:
            return None
        payload = document.to_dict() or {}
        return Run(
            id=document.id,
            user_id=payload['user_id'],
            date=date.fromisoformat(payload['date']),
            distance_km=payload['distance_km'],
            duration_seconds=payload['duration_seconds'],
            avg_pace_seconds=payload['avg_pace_seconds'],
            avg_speed_kmh=payload['avg_speed_kmh'],
            avg_heart_rate=payload.get('avg_heart_rate'),
            elevation_gain=payload.get('elevation_gain'),
            route_file=payload.get('route_file'),
            notes=payload.get('notes'),
            created_at=payload.get('created_at'),
        )

    def _serialize(self, run: Run) -> dict:
        return {
            'user_id': run.user_id,
            'date': run.date.isoformat(),
            'distance_km': run.distance_km,
            'duration_seconds': run.duration_seconds,
            'avg_pace_seconds': run.avg_pace_seconds,
            'avg_speed_kmh': run.avg_speed_kmh,
            'avg_heart_rate': run.avg_heart_rate,
            'elevation_gain': run.elevation_gain,
            'route_file': run.route_file,
            'notes': run.notes,
            'created_at': run.created_at or datetime.now(timezone.utc),
        }

    def create(self, run: Run) -> Run:
        doc_ref = self.collection.document()
        run.id = doc_ref.id
        run.created_at = run.created_at or datetime.now(timezone.utc)
        doc_ref.set(self._serialize(run))
        return run

    def list(
        self,
        user_id: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        min_distance_km: float | None = None,
        max_distance_km: float | None = None,
    ) -> list[Run]:
        runs = [self._to_model(doc) for doc in self.collection.stream()]
        materialized = [run for run in runs if run is not None]

        if user_id is not None:
            materialized = [run for run in materialized if run.user_id == user_id]
        if start_date is not None:
            materialized = [run for run in materialized if run.date >= start_date]
        if end_date is not None:
            materialized = [run for run in materialized if run.date <= end_date]
        if min_distance_km is not None:
            materialized = [run for run in materialized if run.distance_km >= min_distance_km]
        if max_distance_km is not None:
            materialized = [run for run in materialized if run.distance_km <= max_distance_km]

        return sorted(
            materialized,
            key=lambda run: (run.date, run.created_at or datetime.min.replace(tzinfo=timezone.utc)),
            reverse=True,
        )

    def get_by_id(self, run_id: str) -> Run | None:
        return self._to_model(self.collection.document(run_id).get())
