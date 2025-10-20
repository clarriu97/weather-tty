from __future__ import annotations
import httpx
from typing import Optional

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

class WeatherError(RuntimeError):
    pass

async def geocode_city(client: httpx.AsyncClient, query: str) -> tuple[float, float, str]:
    params = {"name": query, "count": 1, "language": "en", "format": "json"}
    r = await client.get(GEO_URL, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()
    results = (data or {}).get("results") or []
    if not results:
        raise WeatherError(f"city not found: {query}")
    hit = results[0]
    name = ", ".join(filter(None, [hit.get("name"), hit.get("country_code")]))
    return float(hit["latitude"]), float(hit["longitude"]), name

async def daily_forecast(
    client: httpx.AsyncClient,
    lat: float,
    lon: float,
    tz: Optional[str] = None,
    units: str = "metric",
) -> dict:
    temp_unit = "celsius" if units == "metric" else "fahrenheit"
    wind_unit = "kmh" if units == "metric" else "mph"

    params = {
        "latitude": lat,
        "longitude": lon,
        "timezone": tz or "auto",
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "weathercode",
            "sunrise",
            "sunset",
            "windspeed_10m_max",
        ],
        "temperature_unit": temp_unit,
        "windspeed_unit": wind_unit,
    }
    r = await client.get(FORECAST_URL, params=params, timeout=10)
    r.raise_for_status()
    return r.json()
