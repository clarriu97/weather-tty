import httpx
import respx
from typer.testing import CliRunner

from weather_tty import __version__
from weather_tty.api import FORECAST_URL, GEO_URL, IP_URL
from weather_tty.cli import app


runner = CliRunner()


def _forecast_json(days: int = 5) -> dict:
    return {
        "daily": {
            "time": [f"2026-07-0{i + 1}" for i in range(days)],
            "temperature_2m_max": [25.0 + i for i in range(days)],
            "temperature_2m_min": [15.0 + i for i in range(days)],
            "precipitation_sum": [0.0 for _ in range(days)],
            "weathercode": [2 for _ in range(days)],
            "sunrise": ["2026-07-01T06:30" for _ in range(days)],
            "sunset": ["2026-07-01T21:45" for _ in range(days)],
            "windspeed_10m_max": [10.0 for _ in range(days)],
        }
    }


def test_version_flag_does_not_hit_network():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_invalid_units_exits_2():
    result = runner.invoke(app, ["--units", "bogus"])
    assert result.exit_code == 2
    assert "invalid --units" in result.stdout


@respx.mock
def test_line_with_coords():
    respx.get(FORECAST_URL).mock(return_value=httpx.Response(200, json=_forecast_json()))
    result = runner.invoke(app, ["--lat", "42.8", "--lon", "-1.6"])
    assert result.exit_code == 0
    assert "42.8,-1.6" in result.stdout
    assert "°C" in result.stdout
    assert "06:30" in result.stdout


@respx.mock
def test_line_no_emoji():
    respx.get(FORECAST_URL).mock(return_value=httpx.Response(200, json=_forecast_json()))
    result = runner.invoke(app, ["--lat", "42.8", "--lon", "-1.6", "--no-emoji"])
    assert result.exit_code == 0
    assert "⛅" not in result.stdout


@respx.mock
def test_forecast_table():
    respx.get(FORECAST_URL).mock(return_value=httpx.Response(200, json=_forecast_json(days=5)))
    result = runner.invoke(app, ["--lat", "42.8", "--lon", "-1.6", "--forecast"])
    assert result.exit_code == 0
    assert "Forecast" in result.stdout
    assert "2026-07-01" in result.stdout
    assert "2026-07-05" in result.stdout


@respx.mock
def test_city_geocode_then_forecast():
    respx.get(GEO_URL).mock(
        return_value=httpx.Response(
            200,
            json={"results": [{"name": "Pamplona", "country_code": "ES", "latitude": 42.81, "longitude": -1.64}]},
        )
    )
    respx.get(FORECAST_URL).mock(return_value=httpx.Response(200, json=_forecast_json()))
    result = runner.invoke(app, ["--city", "Pamplona"])
    assert result.exit_code == 0
    assert "Pamplona" in result.stdout


@respx.mock
def test_verbose_panel():
    respx.get(FORECAST_URL).mock(return_value=httpx.Response(200, json=_forecast_json()))
    result = runner.invoke(app, ["--lat", "42.8", "--lon", "-1.6", "--verbose"])
    assert result.exit_code == 0
    assert "weather-tty" in result.stdout


@respx.mock
def test_ip_auto_path_with_no_args():
    respx.get(IP_URL).mock(
        return_value=httpx.Response(
            200,
            json={"status": "success", "lat": 42.81, "lon": -1.64, "city": "Pamplona", "countryCode": "ES"},
        )
    )
    respx.get(FORECAST_URL).mock(return_value=httpx.Response(200, json=_forecast_json()))
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "(auto)" in result.stdout


@respx.mock
def test_unexpected_error_exits_1():
    # time is present (passes the empty-data guard) but the value arrays are empty,
    # so indexing raises IndexError and hits the last-resort handler.
    broken = {"daily": {"time": ["2026-07-01"]}}
    respx.get(FORECAST_URL).mock(return_value=httpx.Response(200, json=broken))
    result = runner.invoke(app, ["--lat", "42.8", "--lon", "-1.6"])
    assert result.exit_code == 1
    assert "error" in result.stdout


@respx.mock
def test_empty_forecast_data_exits_1():
    respx.get(FORECAST_URL).mock(return_value=httpx.Response(200, json={"daily": {"time": []}}))
    result = runner.invoke(app, ["--lat", "42.8", "--lon", "-1.6"])
    assert result.exit_code == 1
    assert "no forecast data available" in result.stdout


@respx.mock
def test_http_error_exits_1():
    respx.get(FORECAST_URL).mock(return_value=httpx.Response(500))
    result = runner.invoke(app, ["--lat", "42.8", "--lon", "-1.6"])
    assert result.exit_code == 1
    assert "error" in result.stdout


@respx.mock
def test_city_not_found_exits_1():
    respx.get(GEO_URL).mock(return_value=httpx.Response(200, json={"results": []}))
    result = runner.invoke(app, ["--city", "Atlantis"])
    assert result.exit_code == 1
    assert "city not found" in result.stdout
