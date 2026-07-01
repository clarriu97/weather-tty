import httpx
import pytest
import respx

from weather_tty.api import (
    FORECAST_URL,
    IP_URL,
    WeatherError,
    daily_forecast,
    get_ip_location,
)


@respx.mock
@pytest.mark.anyio
async def test_get_ip_location_ok():
    respx.get(IP_URL).mock(
        return_value=httpx.Response(
            200,
            json={"status": "success", "lat": 42.81, "lon": -1.64, "city": "Pamplona", "countryCode": "ES"},
        )
    )
    async with httpx.AsyncClient() as c:
        lat, lon, name = await get_ip_location(c)
    assert (lat, lon) == (42.81, -1.64)
    assert name == "Pamplona, ES (auto)"


@respx.mock
@pytest.mark.anyio
async def test_get_ip_location_failure_uses_message():
    respx.get(IP_URL).mock(return_value=httpx.Response(200, json={"status": "fail", "message": "private range"}))
    async with httpx.AsyncClient() as c:
        with pytest.raises(WeatherError, match="private range"):
            await get_ip_location(c)


@respx.mock
@pytest.mark.anyio
async def test_get_ip_location_missing_coords():
    respx.get(IP_URL).mock(return_value=httpx.Response(200, json={"status": "success", "city": "Nowhere"}))
    async with httpx.AsyncClient() as c:
        with pytest.raises(WeatherError, match="coordinates"):
            await get_ip_location(c)


@respx.mock
@pytest.mark.anyio
async def test_get_ip_location_label_fallback():
    respx.get(IP_URL).mock(return_value=httpx.Response(200, json={"status": "success", "lat": 1.0, "lon": 2.0}))
    async with httpx.AsyncClient() as c:
        _, _, name = await get_ip_location(c)
    assert name == "your location (auto)"


@respx.mock
@pytest.mark.anyio
async def test_daily_forecast_builds_imperial_params():
    route = respx.get(FORECAST_URL).mock(return_value=httpx.Response(200, json={"daily": {"time": []}}))
    async with httpx.AsyncClient() as c:
        data = await daily_forecast(c, 40.0, -3.0, units="imperial", forecast_days=5)

    assert data == {"daily": {"time": []}}
    params = route.calls.last.request.url.params
    assert params["temperature_unit"] == "fahrenheit"
    assert params["windspeed_unit"] == "mph"
    assert params["forecast_days"] == "5"
    assert params["timezone"] == "auto"
    assert "temperature_2m_max" in params.get_list("daily")


@respx.mock
@pytest.mark.anyio
async def test_daily_forecast_metric_defaults():
    route = respx.get(FORECAST_URL).mock(return_value=httpx.Response(200, json={"daily": {"time": []}}))
    async with httpx.AsyncClient() as c:
        await daily_forecast(c, 40.0, -3.0, tz="Europe/Madrid")
    params = route.calls.last.request.url.params
    assert params["temperature_unit"] == "celsius"
    assert params["windspeed_unit"] == "kmh"
    assert params["timezone"] == "Europe/Madrid"


@respx.mock
@pytest.mark.anyio
async def test_daily_forecast_raises_on_http_error():
    respx.get(FORECAST_URL).mock(return_value=httpx.Response(500))
    async with httpx.AsyncClient() as c:
        with pytest.raises(httpx.HTTPStatusError):
            await daily_forecast(c, 40.0, -3.0)
