"""weather-tty: tiny CLI to print the weather for your terminal (Open-Meteo, zero API key)."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version


try:
    __version__ = version("weather-tty")
except PackageNotFoundError:  # pragma: no cover - only hit when running from a non-installed tree
    __version__ = "0.0.0"

__all__ = ["__version__"]
