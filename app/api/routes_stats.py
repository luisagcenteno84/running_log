from fastapi import APIRouter, Depends, Query

from app.database.db import get_db
from app.schemas.run_schema import StatsResponse
from app.services.stats_service import StatsService

router = APIRouter(prefix='/stats', tags=['stats'])


@router.get('', response_model=StatsResponse)
def get_stats(user_id: str | None = Query(default=None), db = Depends(get_db)) -> StatsResponse:
    summary = StatsService(db).summary(user_id=user_id)
    return StatsResponse(**summary)
