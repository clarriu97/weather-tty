from __future__ import annotations

import asyncio

import httpx
import typer
from rich import print as rprint
from rich.panel import Panel

from .api import WeatherError, daily_forecast, geocode_city
from .formatting import code_to_emoji, format_line

app = typer.Typer(add_completion=False, no_args_is_help=True, help="Print today's weather for your terminal.")

@app.command()
def today(
    city: str | None = typer.Option(None, "--city", "-c", help="City name (uses Open-Meteo geocoding)"),
    lat: float | None = typer.Option(None, help="Latitude (overrides --city)"),
    lon: float | None = typer.Option(None, help="Longitude (overrides --city)"),
    tz: str | None = typer.Option(None, "--timezone", help="IANA timezone, default auto"),
    units: str = typer.Option("metric", "--units", "-u", help="metric|imperial"),
    no_emoji: bool = typer.Option(False, "--no-emoji", help="Disable emoji"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show a nice panel instead of plain line"),
):
    """
    Print a single line with today's forecast: tmax/tmin, precipitation sum, wind max and sunrise/sunset.
    """
    if units not in {"metric", "imperial"}:
        rprint("[red]invalid --units (use metric|imperial)[/red]")
        raise typer.Exit(2)

    async def _run():
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                if lat is None or lon is None:
                    if not city:
                        rprint("[yellow]Specify --city or --lat/--lon[/yellow]")
                        raise typer.Exit(2)
                    lat_, lon_, display = await geocode_city(client, city)
                else:
                    lat_, lon_, display = lat, lon, city or f"{lat},{lon}"

                data = await daily_forecast(client, lat_, lon_, tz=tz, units=units)
                d = data.get("daily") or {}
                # siempre tomamos el índice 0 (hoy)
                tmin = float(d["temperature_2m_min"][0])
                tmax = float(d["temperature_2m_max"][0])
                precip = float(d["precipitation_sum"][0])
                wmax = float(d.get("windspeed_10m_max", [0])[0])
                code = int(d["weathercode"][0])
                sunrise = d["sunrise"][0]
                sunset = d["sunset"][0]

                line = format_line(display, tmin, tmax, precip, wmax, sunrise, sunset, code, units, use_emoji=not no_emoji)

                if verbose:
                    emoji = code_to_emoji(code) if not no_emoji else ""
                    rprint(Panel.fit(line, title=f"weather-tty {emoji}"))
                else:
                    print(line)

            except WeatherError as e:
                rprint(f"[red]error:[/red] {e}")
                raise typer.Exit(1) from None
            except httpx.HTTPError as e:
                rprint(f"[red]network error:[/red] {e}")
                raise typer.Exit(1) from None

    asyncio.run(_run())
