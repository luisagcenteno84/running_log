from app.analytics.pace_calculator import calculate_pace_seconds, calculate_speed_kmh, format_pace


def test_calculate_pace_and_formatting() -> None:
    pace_seconds = calculate_pace_seconds(duration_seconds=1500, distance_km=5.0)
    assert pace_seconds == 300
    assert format_pace(pace_seconds) == '5:00/km'


def test_calculate_speed() -> None:
    speed = calculate_speed_kmh(duration_seconds=1800, distance_km=5.0)
    assert speed == 10.0


def test_invalid_pace_inputs_raise() -> None:
    try:
        calculate_pace_seconds(duration_seconds=1000, distance_km=0)
        assert False, 'Expected ValueError for zero distance'
    except ValueError:
        assert True
