from __future__ import annotations

import asyncio

import httpx
import typer
from rich import print as rprint
from rich.panel import Panel
from rich.table import Table

from .api import WeatherError, daily_forecast, geocode_city, get_ip_location
from .formatting import code_to_emoji, format_line


app = typer.Typer(add_completion=False, no_args_is_help=False, help="Print weather for your terminal.")


@app.command()
def main(
    city: str | None = typer.Option(None, "--city", "-c", help="City name (uses Open-Meteo geocoding)"),
    lat: float | None = typer.Option(None, help="Latitude (overrides --city)"),
    lon: float | None = typer.Option(None, help="Longitude (overrides --city)"),
    tz: str | None = typer.Option(None, "--timezone", help="IANA timezone, default auto"),
    units: str = typer.Option("metric", "--units", "-u", help="metric|imperial"),
    no_emoji: bool = typer.Option(False, "--no-emoji", help="Disable emoji"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show a nice panel instead of plain line"),
    forecast: bool = typer.Option(False, "--forecast", "-f", help="Show 5-day forecast table"),
):
    """
    Print today's weather or a 5-day forecast.
    """
    if units not in {"metric", "imperial"}:
        rprint("[red]invalid --units (use metric|imperial)[/red]")
        raise typer.Exit(2)

    async def _run():
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                if lat is not None and lon is not None:
                    lat_, lon_, display = lat, lon, f"{lat},{lon}"
                elif city:
                    lat_, lon_, display = await geocode_city(client, city)
                else:
                    lat_, lon_, display = await get_ip_location(client)

                data = await daily_forecast(client, lat_, lon_, tz=tz, units=units)
                d = data.get("daily") or {}

                if not forecast:
                    # Single line today
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
                else:
                    # Forecast table
                    table = Table(title=f"Forecast: {display}")
                    table.add_column("Date", style="cyan")
                    table.add_column("Weather", justify="center")
                    table.add_column("Temp", justify="right")
                    table.add_column("Rain", justify="right")
                    table.add_column("Wind", justify="right")

                    unit_temp = "°C" if units == "metric" else "°F"
                    unit_rain = "mm" if units == "metric" else "in"
                    unit_wind = "km/h" if units == "metric" else "mph"

                    for i in range(5):
                        date = d["time"][i]
                        tmin = float(d["temperature_2m_min"][i])
                        tmax = float(d["temperature_2m_max"][i])
                        precip = float(d["precipitation_sum"][i])
                        wmax = float(d.get("windspeed_10m_max", [0])[i])
                        code = int(d["weathercode"][i])

                        emoji = code_to_emoji(code) if not no_emoji else ""
                        rain_val = precip if units == "metric" else round(precip / 25.4, 2)

                        table.add_row(
                            date, f"{emoji}", f"{round(tmax)}/{round(tmin)}{unit_temp}", f"{rain_val}{unit_rain}", f"{round(wmax)} {unit_wind}"
                        )
                    rprint(table)

            except Exception as e:
                # Catch-all for better user experience but could be more specific
                if isinstance(e, (WeatherError, httpx.HTTPError)):
                    rprint(f"[red]error:[/red] {e}")
                else:
                    rprint(f"[red]error:[/red] {type(e).__name__}: {e}")
                raise typer.Exit(1) from None

    asyncio.run(_run())
