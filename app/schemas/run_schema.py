from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.analytics.pace_calculator import format_pace


class RunBase(BaseModel):
    date: date
    distance_km: float = Field(gt=0)
    duration_seconds: int = Field(gt=0)
    avg_heart_rate: int | None = Field(default=None, gt=0)
    elevation_gain: float | None = Field(default=None, ge=0)
    route_file: str | None = None
    notes: str | None = None


class RunCreate(RunBase):
    user_id: str


class RunRead(RunBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    avg_pace_seconds: float
    avg_speed_kmh: float
    created_at: datetime

    @field_validator('avg_pace_seconds')
    @classmethod
    def rounded_pace(cls, value: float) -> float:
        return round(value, 2)


class RunResponse(BaseModel):
    run_id: str
    user_id: str
    date: date
    distance_km: float
    duration_seconds: int
    avg_pace: str
    avg_speed_kmh: float
    avg_heart_rate: int | None = None
    elevation_gain: float | None = None
    route_file: str | None = None
    notes: str | None = None
    created_at: datetime

    @classmethod
    def from_run(cls, run: RunRead) -> 'RunResponse':
        return cls(
            run_id=run.id,
            user_id=run.user_id,
            date=run.date,
            distance_km=run.distance_km,
            duration_seconds=run.duration_seconds,
            avg_pace=format_pace(run.avg_pace_seconds),
            avg_speed_kmh=round(run.avg_speed_kmh, 2),
            avg_heart_rate=run.avg_heart_rate,
            elevation_gain=run.elevation_gain,
            route_file=run.route_file,
            notes=run.notes,
            created_at=run.created_at,
        )


class RunFilters(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    min_distance_km: float | None = Field(default=None, ge=0)
    max_distance_km: float | None = Field(default=None, ge=0)


class StatsResponse(BaseModel):
    total_distance_km: float
    weekly_mileage_km: float
    average_pace: str
    fastest_run_id: str | None
    longest_run_id: str | None
    training_frequency: int
