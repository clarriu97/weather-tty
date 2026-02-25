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
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/badge/code%20style-ruff-black?logo=ruff&logoColor=white" alt="Code style: Ruff">
  </a>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/coverage-¯\_(ツ)_/¯-blueviolet?style=flat-square" alt="Coverage shrug">
  <img src="https://img.shields.io/badge/build-success%20(usually,%20ask%20ChatGPT)-orange?style=flat-square" alt="Build success (usually, ask ChatGPT)">
  <img src="https://img.shields.io/badge/type%20checked-LOL-red?style=flat-square" alt="Type checked LOL">
  <img src="https://img.shields.io/badge/PRs-welcome%20(but%20judged)-yellow?style=flat-square" alt="PRs welcome (but judged)">
  <img src="https://img.shields.io/badge/maintainer-sleep%20deprived-blue?style=flat-square" alt="Maintainer sleep deprived">
  <img src="https://img.shields.io/badge/made%20with-%E2%9D%A4%20and%20Python-ff69b4?logo=python&logoColor=white&style=flat-square" alt="Made with love and Python">
  <img src="https://img.shields.io/badge/runs%20on-UV-6E40C9?logo=astral&style=flat-square" alt="Runs on UV">
  <img src="https://img.shields.io/badge/async-await%20all%20the%20things-007ec6?style=flat-square" alt="Async all the things">
  <img src="https://img.shields.io/badge/emoji%20support-✅-brightgreen?style=flat-square" alt="Emoji support">
  <img src="https://img.shields.io/badge/works%20on-my%20machine-lightgrey?style=flat-square" alt="Works on my machine">
  <img src="https://img.shields.io/badge/built%20with-anger%20and%20coffee-brown?style=flat-square" alt="Built with anger and coffee">
  <img src="https://img.shields.io/badge/weather-🌤️%20probably%20fine-blue?style=flat-square" alt="Weather probably fine">
  <img src="https://img.shields.io/badge/terminal-approved-black?style=flat-square&logo=gnometerminal" alt="Terminal approved">
</p>

## Features

- **Zero-config**: just type `weather-tty` and it will guess your city by IP.
- Single-line summary: `🌤️ Pamplona, ES: 25°C/12°C · rain 0.0mm · wind 18 km/h · sun 08:10–19:14`
- Multi-day forecast: `weather-tty --forecast` for a 5-day table.
- `--city` geocoding (Open-Meteo) or `--lat/--lon`.
- Units: `metric` (default) or `imperial`.
- `--no-emoji` for boring terminals.
- `--verbose` pretty panel for humans.

## Install

> **Requires Python 3.10+**

### Recommended (pipx)

The easiest way to install `weather-tty` as a CLI tool:

```bash
brew install pipx  # if you don't have pipx
pipx install weather-tty
```

This installs `weather-tty` in an isolated environment and makes it available globally.

### Alternative (pip)

```bash
pip install weather-tty
```

> ⚠️ On macOS with Homebrew Python, you may get an `externally-managed-environment` error.
> Use `pipx` instead, or create a virtual environment.

## Usage

```bash
# auto-detect city by IP
weather-tty

# by city
weather-tty --city "Pamplona"

# 5-day forecast table
weather-tty --city "Pamplona" --forecast

# coordinates (overrides city)
weather-tty --lat 40.4168 --lon -3.7038

# imperial units
weather-tty --city "New York" --units imperial

# pretty panel
weather-tty --city "Pamplona" --verbose
```

### Pro Tip: Terminal Greeting

Add `weather-tty` to the end of your `.zshrc`, `.bashrc`, or `.bash_profile` to get a fresh weather report every time you open a new terminal session:

```bash
# Add this to ~/.zshrc or ~/.bashrc
weather-tty
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
uv run weather-tty --city "Pamplona"
```
