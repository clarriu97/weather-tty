import respx
import httpx
import pytest
from weather_tty.api import geocode_city, GEO_URL, WeatherError

@respx.mock
@pytest.mark.anyio
async def test_geocode_city_ok():
    route = respx.get(GEO_URL).mock(
        return_value=httpx.Response(
            200,
            json={"results": [{"name": "Pamplona", "country_code": "ES", "latitude": 42.81, "longitude": -1.64}]},
        )
    )
    async with httpx.AsyncClient() as c:
        lat, lon, name = await geocode_city(c, "Pamplona")
    assert route.called
    assert name.startswith("Pamplona")
    assert lat and lon

@respx.mock
@pytest.mark.anyio
async def test_geocode_city_not_found():
    respx.get(GEO_URL).mock(return_value=httpx.Response(200, json={"results": []}))
    async with httpx.AsyncClient() as c:
        with pytest.raises(WeatherError):
            await geocode_city(c, "Atlantis")
