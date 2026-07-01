"""Regenerate the demo screenshots in ``docs/`` (no network required).

Usage::

    uv run python scripts/gen_demo.py

The sample data is fixed so the screenshots are reproducible, and it deliberately
includes ``U+FE0F`` weather emojis (☁️ 🌧️ ⛈️) to show the panel/table borders
staying aligned after the emoji-width fix.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel

from weather_tty._richfix import apply as apply_richfix
from weather_tty.formatting import build_forecast_table, code_to_emoji, format_line


apply_richfix()

DOCS = Path(__file__).resolve().parent.parent / "docs"
DOCS.mkdir(exist_ok=True)

DISPLAY = "Dubai, AE"
DAILY: dict[str, Any] = {
    "time": ["2026-07-01", "2026-07-02", "2026-07-03", "2026-07-04", "2026-07-05"],
    "temperature_2m_max": [40, 41, 39, 37, 42],
    "temperature_2m_min": [28, 29, 27, 26, 30],
    "precipitation_sum": [0.0, 0.0, 1.2, 4.5, 0.0],
    "weathercode": [3, 2, 61, 95, 0],
    "sunrise": ["2026-07-01T05:32"] * 5,
    "sunset": ["2026-07-01T19:12"] * 5,
    "windspeed_10m_max": [21, 18, 24, 30, 15],
}


def _line() -> str:
    return format_line(
        DISPLAY,
        DAILY["temperature_2m_min"][0],
        DAILY["temperature_2m_max"][0],
        DAILY["precipitation_sum"][0],
        DAILY["windspeed_10m_max"][0],
        DAILY["sunrise"][0],
        DAILY["sunset"][0],
        DAILY["weathercode"][0],
    )


def main() -> None:
    console = Console(record=True, width=78)
    line = _line()

    console.print("[bold green]$ weather-tty --city Dubai[/bold green]")
    console.print(line)
    console.print()

    console.print("[bold green]$ weather-tty --city Dubai --verbose[/bold green]")
    console.print(Panel.fit(line, title=f"weather-tty {code_to_emoji(DAILY['weathercode'][0])}"))
    console.print()

    console.print("[bold green]$ weather-tty --city Dubai --forecast[/bold green]")
    console.print(build_forecast_table(DISPLAY, DAILY))

    out = DOCS / "demo.svg"
    console.save_svg(str(out), title="weather-tty")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
