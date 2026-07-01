from __future__ import annotations

from typing import Any

import httpx


GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
IP_URL = "http://ip-api.com/json/"  # free tier is HTTP-only

DEFAULT_TIMEOUT = 10.0

DAILY_FIELDS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "weathercode",
    "sunrise",
    "sunset",
    "windspeed_10m_max",
]


class WeatherError(RuntimeError):
    """Raised when weather/location data cannot be retrieved."""


async def get_ip_location(client: httpx.AsyncClient) -> tuple[float, float, str]:
    """Get approximate location from the caller's IP address."""
    r = await client.get(IP_URL, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    data: dict[str, Any] = r.json()
    if data.get("status") != "success":
        raise WeatherError(data.get("message") or "could not determine location from IP")
    try:
        lat, lon = float(data["lat"]), float(data["lon"])
    except (KeyError, TypeError, ValueError) as exc:
        raise WeatherError("IP location response is missing coordinates") from exc
    label = ", ".join(filter(None, [data.get("city"), data.get("countryCode")])) or "your location"
    return lat, lon, f"{label} (auto)"


async def geocode_city(client: httpx.AsyncClient, query: str) -> tuple[float, float, str]:
    """Resolve a city name to coordinates via Open-Meteo geocoding."""
    params: dict[str, Any] = {"name": query, "count": 1, "language": "en", "format": "json"}
    r = await client.get(GEO_URL, params=params, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    data: dict[str, Any] = r.json() or {}
    results = data.get("results") or []
    if not results:
        raise WeatherError(f"city not found: {query}")
    hit = results[0]
    name = ", ".join(filter(None, [hit.get("name"), hit.get("country_code")]))
    return float(hit["latitude"]), float(hit["longitude"]), name


async def daily_forecast(
    client: httpx.AsyncClient,
    lat: float,
    lon: float,
    tz: str | None = None,
    units: str = "metric",
    forecast_days: int = 7,
) -> dict[str, Any]:
    """Fetch the daily forecast for the given coordinates."""
    temp_unit = "celsius" if units == "metric" else "fahrenheit"
    wind_unit = "kmh" if units == "metric" else "mph"

    params: dict[str, Any] = {
        "latitude": lat,
        "longitude": lon,
        "timezone": tz or "auto",
        "daily": DAILY_FIELDS,
        "temperature_unit": temp_unit,
        "windspeed_unit": wind_unit,
        "forecast_days": forecast_days,
    }
    r = await client.get(FORECAST_URL, params=params, timeout=DEFAULT_TIMEOUT)
    r.raise_for_status()
    data: dict[str, Any] = r.json()
    return data
