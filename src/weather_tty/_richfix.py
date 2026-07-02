"""Align Rich's emoji width measurement with modern terminals.

Weather emojis such as ``☀️``, ``☁️`` or ``🌧️`` end with the variation selector
``U+FE0F``, which asks the terminal for the coloured, two-cell emoji presentation.
Terminals like Warp, iTerm2, Kitty or Windows Terminal render such an emoji as
**2** cells. Older Rich releases counted ``U+FE0F`` as zero cells and the
preceding symbol as a single cell, so they measured the whole emoji as **1**
cell -- that one-column disagreement is what makes ``--verbose`` panels and
``--forecast`` tables draw their borders slightly off.

Rich learned to measure the variation selector in context in 14.3, where
``get_character_cell_size`` also grew a second ``unicode_version`` argument. So
this module:

* does nothing when the installed Rich already measures a variation-selector
  emoji as two cells (the common case today); and
* otherwise nudges ``U+FE0F`` to contribute one cell, wrapping the original
  width function while forwarding *any* extra arguments so the shim works across
  Rich signatures.

The patch is applied to the module namespace Rich reads at call time, is
idempotent, and degrades to a no-op if Rich changes its internals.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


VARIATION_SELECTOR_16 = chr(0xFE0F)

# A representative weather emoji: a narrow base symbol followed by U+FE0F. Modern
# terminals (and Rich >= 14.3) render this as two cells.
_PROBE_EMOJI = "☀" + VARIATION_SELECTOR_16  # ☀️

_applied = False


def apply() -> None:
    """Make Rich measure variation-selector emoji as two cells.

    A no-op on Rich versions that already do so. Safe to call multiple times;
    only the first call has an effect.
    """
    global _applied
    if _applied:
        return

    try:
        import rich.cells as cells
    except Exception:  # pragma: no cover - Rich is a hard dependency, defensive only
        return

    # Modern Rich already measures "☀️" as two cells; leave it untouched. This
    # also avoids replacing its get_character_cell_size, whose signature grew a
    # second argument in 14.3 that a naive one-argument shim would break.
    try:
        if cells.cell_len(_PROBE_EMOJI) >= 2:
            _applied = True
            return
    except Exception:  # noqa: S110 # pragma: no cover - defensive against Rich refactors
        pass

    original: Callable[..., int] | None = getattr(cells, "get_character_cell_size", None)
    if not callable(original):  # pragma: no cover - defensive against Rich refactors
        return

    def get_character_cell_size(character: str, *args: Any, **kwargs: Any) -> int:
        if character == VARIATION_SELECTOR_16:
            return 1
        return original(character, *args, **kwargs)

    # cached_cell_len() looks this name up in the module globals at call time, so
    # assigning into the module __dict__ propagates to every Rich width call.
    cells.__dict__["get_character_cell_size"] = get_character_cell_size

    cache_clear = getattr(cells.cached_cell_len, "cache_clear", None)
    if callable(cache_clear):
        cache_clear()

    _applied = True
