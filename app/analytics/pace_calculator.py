def calculate_pace_seconds(duration_seconds: int, distance_km: float) -> float:
    """Return pace in seconds per kilometer."""
    if distance_km <= 0:
        raise ValueError('distance_km must be greater than zero')
    if duration_seconds <= 0:
        raise ValueError('duration_seconds must be greater than zero')
    return duration_seconds / distance_km


def calculate_speed_kmh(duration_seconds: int, distance_km: float) -> float:
    """Return average speed in km/h."""
    hours = duration_seconds / 3600
    if hours <= 0:
        raise ValueError('duration_seconds must be greater than zero')
    return distance_km / hours


def format_pace(pace_seconds: float) -> str:
    """Format pace (sec/km) as M:SS/km."""
    minutes = int(pace_seconds // 60)
    seconds = int(round(pace_seconds % 60))
    if seconds == 60:
        minutes += 1
        seconds = 0
    return f'{minutes}:{seconds:02d}/km'
