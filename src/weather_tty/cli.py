from __future__ import annotations

import asyncio

import httpx
import typer
from rich import print as rprint
from rich.panel import Panel

from . import __version__
from ._richfix import apply as _apply_richfix
from .api import WeatherError, daily_forecast, geocode_city, get_ip_location
from .formatting import build_forecast_table, code_to_emoji, format_line


# Make Rich measure emoji the way modern terminals render them, so --verbose
# panels and --forecast tables keep their borders aligned.
_apply_richfix()

app = typer.Typer(add_completion=False, no_args_is_help=False, help="Print weather for your terminal.")

FORECAST_DAYS = 5


def _version_callback(value: bool) -> None:
    if value:
        rprint(f"weather-tty {__version__}")
        raise typer.Exit()


@app.command()
def main(
    city: str | None = typer.Option(None, "--city", "-c", help="City name (uses Open-Meteo geocoding)"),
    lat: float | None = typer.Option(None, help="Latitude (overrides --city)"),
    lon: float | None = typer.Option(None, help="Longitude (overrides --city)"),
    tz: str | None = typer.Option(None, "--timezone", help="IANA timezone, default auto"),
    units: str = typer.Option("metric", "--units", "-u", help="metric|imperial"),
    no_emoji: bool = typer.Option(False, "--no-emoji", help="Disable emoji"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show a nice panel instead of plain line"),
    forecast: bool = typer.Option(False, "--forecast", "-f", help="Show a 5-day forecast table"),
    _version: bool = typer.Option(
        False, "--version", callback=_version_callback, is_eager=True, help="Show version and exit"
    ),
) -> None:
    """
    Print today's weather or a 5-day forecast.
    """
    if units not in {"metric", "imperial"}:
        rprint("[red]invalid --units (use metric|imperial)[/red]")
        raise typer.Exit(2)

    async def _run() -> None:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                if lat is not None and lon is not None:
                    lat_, lon_, display = lat, lon, f"{lat},{lon}"
                elif city:
                    lat_, lon_, display = await geocode_city(client, city)
                else:
                    lat_, lon_, display = await get_ip_location(client)

                days = FORECAST_DAYS if forecast else 1
                data = await daily_forecast(client, lat_, lon_, tz=tz, units=units, forecast_days=days)
                d = data.get("daily") or {}
                if not d.get("time"):
                    raise WeatherError("no forecast data available")

                if forecast:
                    table = build_forecast_table(display, d, units=units, use_emoji=not no_emoji, max_days=FORECAST_DAYS)
                    rprint(table)
                    return

                line = format_line(
                    display,
                    float(d["temperature_2m_min"][0]),
                    float(d["temperature_2m_max"][0]),
                    float(d["precipitation_sum"][0]),
                    float((d.get("windspeed_10m_max") or [0])[0]),
                    d["sunrise"][0],
                    d["sunset"][0],
                    int(d["weathercode"][0]),
                    units,
                    use_emoji=not no_emoji,
                )

                if verbose:
                    emoji = code_to_emoji(int(d["weathercode"][0])) if not no_emoji else ""
                    rprint(Panel.fit(line, title=f"weather-tty {emoji}"))
                else:
                    print(line)

            except (WeatherError, httpx.HTTPError) as e:
                rprint(f"[red]error:[/red] {e}")
                raise typer.Exit(1) from None
            except Exception as e:  # last-resort guard so the CLI never dumps a traceback
                rprint(f"[red]error:[/red] {type(e).__name__}: {e}")
                raise typer.Exit(1) from None

    asyncio.run(_run())
