from fastapi import FastAPI

from app.api.routes_runs import router as runs_router
from app.api.routes_stats import router as stats_router
from app.api.routes_users import router as users_router
from app.config import get_settings
from app.database.db import init_db

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version='1.0.0',
        description='Backend API for logging and analyzing running workouts.',
    )

    app.include_router(users_router, prefix=settings.api_v1_prefix)
    app.include_router(runs_router, prefix=settings.api_v1_prefix)
    app.include_router(stats_router, prefix=settings.api_v1_prefix)

    @app.get('/health', tags=['health'])
    def health() -> dict[str, str]:
        return {'status': 'ok'}

    return app


app = create_app()
init_db()
