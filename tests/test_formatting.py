from weather_tty.formatting import (
    build_forecast_table,
    code_to_emoji,
    format_line,
    rain_in_units,
    unit_labels,
)


def _daily(days: int) -> dict:
    return {
        "time": [f"2026-07-0{i + 1}" for i in range(days)],
        "temperature_2m_max": [25.0 + i for i in range(days)],
        "temperature_2m_min": [15.0 + i for i in range(days)],
        "precipitation_sum": [0.0 for _ in range(days)],
        "weathercode": [2 for _ in range(days)],
        "windspeed_10m_max": [10.0 for _ in range(days)],
    }


def test_code_to_emoji_known():
    assert code_to_emoji(0) == "☀️"


def test_code_to_emoji_unknown_falls_back():
    assert code_to_emoji(1234) == "🌡️"


def test_unit_labels():
    assert unit_labels("metric") == ("°C", "mm", "km/h")
    assert unit_labels("imperial") == ("°F", "in", "mph")


def test_rain_in_units():
    assert rain_in_units(12.7, "metric") == 12.7
    assert rain_in_units(25.4, "imperial") == 1.0


def test_format_line_metric():
    s = format_line("Pamplona, ES", 12.3, 24.9, 1.6, 22.4, "2025-10-20T08:10", "2025-10-20T19:14", 2, "metric")
    assert "Pamplona, ES" in s
    assert "°C" in s
    assert "rain 1.6mm" in s
    assert "08:10" in s and "19:14" in s


def test_format_line_imperial_converts_rain_and_temp_unit():
    s = format_line("NYC, US", 50, 77, 25.4, 10, "2025-10-20T06:10", "2025-10-20T18:12", 61, "imperial")
    assert "rain 1.0in" in s  # 25.4 mm -> 1.0 in
    assert "°F" in s
    assert "77°F/50°F" in s


def test_format_line_no_emoji_starts_with_city():
    s = format_line("Pamplona, ES", 12, 24, 0, 5, "2025-10-20T08:10", "2025-10-20T19:14", 2, use_emoji=False)
    assert s.startswith("Pamplona, ES:")


def test_build_forecast_table_limits_to_available_days():
    table = build_forecast_table("Somewhere", _daily(3), max_days=5)
    assert table.row_count == 3
    assert "Somewhere" in str(table.title)


def test_build_forecast_table_respects_max_days():
    table = build_forecast_table("Somewhere", _daily(7), max_days=5)
    assert table.row_count == 5
