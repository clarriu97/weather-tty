from __future__ import annotations

from typing import Any

from rich.table import Table


WEATHERCODE_EMOJI = {
    0: "☀️",  # Clear
    1: "🌤️",  # Mainly clear
    2: "⛅",  # Partly cloudy
    3: "☁️",  # Overcast
    45: "🌫️",  # Fog
    48: "🌫️",
    51: "🌦️",  # Drizzle light
    53: "🌦️",
    55: "🌧️",
    56: "🌧️",
    57: "🌧️",
    61: "🌧️",  # Rain
    63: "🌧️",
    65: "🌧️",
    66: "🌧️",
    67: "🌧️",
    71: "🌨️",  # Snow
    73: "🌨️",
    75: "❄️",
    77: "❄️",
    80: "🌧️",
    81: "🌧️",
    82: "🌧️",
    85: "🌨️",
    86: "🌨️",
    95: "⛈️",
    96: "⛈️",
    99: "⛈️",
}

MM_PER_INCH = 25.4


def code_to_emoji(code: int) -> str:
    return WEATHERCODE_EMOJI.get(int(code), "🌡️")


def unit_labels(units: str) -> tuple[str, str, str]:
    """Return the (temperature, rain, wind) unit labels for the given system."""
    if units == "metric":
        return "°C", "mm", "km/h"
    return "°F", "in", "mph"


def rain_in_units(precip_mm: float, units: str) -> float:
    """Convert precipitation from mm to the requested unit system."""
    if units == "metric":
        return precip_mm
    return round(precip_mm / MM_PER_INCH, 2)


def format_line(
    city_display: str,
    tmin: float,
    tmax: float,
    precip_mm: float,
    wind_max: float,
    sunrise: str,
    sunset: str,
    code: int,
    units: str = "metric",
    use_emoji: bool = True,
) -> str:
    unit_temp, unit_rain, unit_wind = unit_labels(units)
    emoji = code_to_emoji(code) if use_emoji else ""
    rain_val = rain_in_units(precip_mm, units)

    return (
        f"{emoji} {city_display}: "
        f"{round(tmax)}{unit_temp}/{round(tmin)}{unit_temp} · "
        f"rain {rain_val}{unit_rain} · wind {round(wind_max)} {unit_wind} · "
        f"sun {sunrise[-5:]}–{sunset[-5:]}"
    ).strip()


def build_forecast_table(
    display: str,
    daily: dict[str, Any],
    units: str = "metric",
    use_emoji: bool = True,
    max_days: int = 5,
) -> Table:
    """Build a Rich table with up to ``max_days`` of forecast rows."""
    unit_temp, unit_rain, unit_wind = unit_labels(units)

    table = Table(title=f"Forecast: {display}")
    table.add_column("Date", style="cyan")
    table.add_column("Weather", justify="center")
    table.add_column("Temp", justify="right")
    table.add_column("Rain", justify="right")
    table.add_column("Wind", justify="right")

    times = daily.get("time") or []
    days = min(max_days, len(times))
    for i in range(days):
        date = times[i]
        tmin = float(daily["temperature_2m_min"][i])
        tmax = float(daily["temperature_2m_max"][i])
        precip = float(daily["precipitation_sum"][i])
        wmax = float((daily.get("windspeed_10m_max") or [0])[i])
        code = int(daily["weathercode"][i])

        emoji = code_to_emoji(code) if use_emoji else ""
        rain_val = rain_in_units(precip, units)

        table.add_row(
            date,
            emoji,
            f"{round(tmax)}/{round(tmin)}{unit_temp}",
            f"{rain_val}{unit_rain}",
            f"{round(wmax)} {unit_wind}",
        )
    return table
