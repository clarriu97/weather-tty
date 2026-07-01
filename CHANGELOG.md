# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-07-01

### Added
- `--version` flag: prints the installed version and exits (no network call).
- `py.typed` marker so downstream type checkers use the package's inline type hints.
- Type checking with [ty](https://github.com/astral-sh/ty) (Astral) in CI and locally.
- Full test suite for the IP/forecast API, the CLI end-to-end, and the emoji-width
 fix (100% coverage, enforced at a 90% floor).
- README preview screenshot of the terminal output, with reproducible generation
 scripts (`scripts/gen_demo.py`, `scripts/demo.tape`).

### Fixed
- Panel (`--verbose`) and forecast table borders no longer misalign: Rich measured
 emoji ending in the `U+FE0F` variation selector (☀️ ☁️ 🌧️ …) as 1 cell while
 modern terminals render them as 2. Widths are now aligned with the terminal.
- `--forecast` no longer risks an `IndexError` when the API returns fewer days than
 requested; the number of days is requested explicitly and rows are capped safely.
- IP-based location lookup no longer crashes when the response omits city/country
 fields, and surfaces a clear error when coordinates are missing.

### Changed
- Unit labels and rain conversion are centralized and shared by the single line and
 the forecast table (no more duplicated logic).
- Packaging: deterministic source distribution (only `src`, `tests`, `README`,
 `LICENSE`) so build artifacts and local files never leak into releases.
- CI now runs a Python 3.10–3.13 matrix with ruff, ty and coverage, on refreshed
 actions (`checkout@v5`, `setup-uv@v6`) with caching.

## [0.2.1] - 2026-02-25

### Fixed
- Corrected the package version metadata (it had lagged behind the released tags),
 so the version published to PyPI matches the release.

## [0.2.0] - 2026-02-25

### Added
- **Zero-config**: with no arguments, `weather-tty` guesses your city from your IP.
- Multi-day forecast: `--forecast` prints a 5-day table.

### Changed
- README overhaul documenting the new zero-config and forecast features.

## [0.1.1] - 2025-10-22

### Changed
- Streamlined the PyPI publish workflow (updated actions, `uv build` / `uv publish`).

## [0.1.0] - 2025-10-20

### Added
- Initial release: single-line weather summary for the terminal, powered by
 [Open-Meteo](https://open-meteo.com/) with no API key.
- Location via `--city` (geocoding) or `--lat`/`--lon`.
- Options: `--units` (metric/imperial), `--timezone`, `--no-emoji`, and `--verbose`
 (pretty panel).
- MIT license and CI / publish GitHub Actions workflows.

[0.3.0]: https://github.com/clarriu97/weather-tty/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/clarriu97/weather-tty/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/clarriu97/weather-tty/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/clarriu97/weather-tty/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/clarriu97/weather-tty/releases/tag/v0.1.0
