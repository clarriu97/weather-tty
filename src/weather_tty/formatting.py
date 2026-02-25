from __future__ import annotations


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


def code_to_emoji(code: int) -> str:
    return WEATHERCODE_EMOJI.get(int(code), "🌡️")


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
    unit_temp = "°C" if units == "metric" else "°F"
    unit_rain = "mm" if units == "metric" else "in"
    unit_wind = "km/h" if units == "metric" else "mph"

    emoji = code_to_emoji(code) if use_emoji else ""
    rain_val = precip_mm if units == "metric" else round(precip_mm / 25.4, 2)

    return (
        f"{emoji} {city_display}: "
        f"{round(tmax)}{unit_temp}/{round(tmin)}{unit_temp} · "
        f"rain {rain_val}{unit_rain} · wind {round(wind_max)} {unit_wind} · "
        f"sun {sunrise[-5:]}–{sunset[-5:]}"
    ).strip()
