from app.models.run import Run


def detect_personal_bests(runs: list[Run]) -> dict[str, int | None]:
    """Return run IDs for best pace and longest distance."""
    if not runs:
        return {'fastest_run_id': None, 'longest_run_id': None}

    fastest = min(runs, key=lambda run: run.avg_pace_seconds)
    longest = max(runs, key=lambda run: run.distance_km)
    return {'fastest_run_id': fastest.id, 'longest_run_id': longest.id}
