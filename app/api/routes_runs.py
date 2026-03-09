from datetime import date

from fastapi import APIRouter, Depends, Query

from app.database.db import get_db
from app.schemas.run_schema import RunCreate, RunRead, RunResponse
from app.services.run_service import RunService

router = APIRouter(prefix='/runs', tags=['runs'])


@router.post('', response_model=RunResponse, status_code=201)
def create_run(payload: RunCreate, db = Depends(get_db)) -> RunResponse:
    run = RunService(db).create_run(payload)
    run_read = RunRead.model_validate(run)
    return RunResponse.from_run(run_read)


@router.get('', response_model=list[RunResponse])
def list_runs(
    user_id: str | None = Query(default=None),
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    min_distance_km: float | None = Query(default=None, ge=0),
    max_distance_km: float | None = Query(default=None, ge=0),
    db = Depends(get_db),
) -> list[RunResponse]:
    runs = RunService(db).list_runs(user_id, start_date, end_date, min_distance_km, max_distance_km)
    return [RunResponse.from_run(RunRead.model_validate(run)) for run in runs]


@router.get('/{run_id}', response_model=RunResponse)
def get_run(run_id: str, db = Depends(get_db)) -> RunResponse:
    run = RunService(db).get_run_or_404(run_id)
    return RunResponse.from_run(RunRead.model_validate(run))
