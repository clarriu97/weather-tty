<h1 align="center">🌦️ weather-tty</h1>

<p align="center">
  <em>Tiny CLI to print today's weather for your terminal — zero API keys, just vibes.</em>
</p>

<p align="center">
  <a href="https://github.com/clarriu97/weather-tty/actions/workflows/ci.yml">
    <img src="https://github.com/clarriu97/weather-tty/actions/workflows/ci.yml/badge.svg" alt="CI Status">
  </a>
  <a href="https://pypi.org/project/weather-tty/">
    <img src="https://img.shields.io/pypi/v/weather-tty.svg?color=blue&logo=pypi&logoColor=white" alt="PyPI">
  </a>
  <a href="https://pypi.org/project/weather-tty/">
    <img src="https://img.shields.io/pypi/pyversions/weather-tty.svg?logo=python&logoColor=white" alt="Python Versions">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/badge/code%20style-ruff-black?logo=ruff&logoColor=white" alt="Code style: Ruff">
  </a>
  <a href="https://codecov.io/gh/clarriu97/weather-tty">
    <img src="https://img.shields.io/codecov/c/github/clarriu97/weather-tty?logo=codecov&logoColor=white&color=ff69b4" alt="Coverage">
  </a>
</p>

## Features

- Single-line output: `🌤️ Pamplona, ES: 25°C/12°C · rain 0.0mm · wind 18 km/h · sun 08:10–19:14`
- `--city` geocoding (Open-Meteo) or `--lat/--lon`
- Units: `metric` (default) or `imperial`
- `--no-emoji` for boring terminals
- `--verbose` pretty panel for humans

## Install

```bash
pip install weather-tty
```

## Usage

```bash
# by city
weather-tty today --city "Pamplona"

# coordinates (overrides city)
weather-tty today --lat 40.4168 --lon -3.7038

# imperial units
weather-tty today --city "New York" --units imperial

# pretty panel
weather-tty today --city "Pamplona" --verbose
```

## Notes

- Data source: [Open-Meteo](https://open-meteo.com/)
- No API keys required.
- Prints today (index 0 of daily arrays). If you want multi-day, PRs welcome.

## Development

```bash
uv sync
uv sync --group dev
uv run ruff check .
uv run ruff check . --fix
uv run pytest
uv run weather-tty today --city "Pamplona"
```
