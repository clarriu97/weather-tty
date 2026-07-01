"""Align Rich's emoji width measurement with modern terminals.

Weather emojis such as ``☀️``, ``☁️`` or ``🌧️`` end with the variation selector
``U+FE0F``, which asks the terminal for the coloured, two-cell emoji presentation.
Rich's width table counts ``U+FE0F`` as zero cells and the preceding symbol as a
single cell, so it measures the whole emoji as **1** cell. Terminals like Warp,
iTerm2, Kitty or Windows Terminal render it as **2** cells. That one-column
disagreement is what makes ``--verbose`` panels and ``--forecast`` tables draw
their borders slightly off (see the mismatched box the user reported).

We nudge ``U+FE0F`` to contribute one cell so Rich's measurements line up with
those terminals. The patch is applied to the module namespace Rich reads at call
time, is idempotent, and degrades to a no-op if Rich changes its internals.
"""

from __future__ import annotations


VARIATION_SELECTOR_16 = chr(0xFE0F)

_applied = False


def apply() -> None:
    """Patch Rich so an emoji variation selector counts as one cell.

    Safe to call multiple times; only the first call has an effect.
    """
    global _applied
    if _applied:
        return

    try:
        import rich.cells as cells
    except Exception:  # pragma: no cover - Rich is a hard dependency, defensive only
        return

    original = getattr(cells, "get_character_cell_size", None)
    if not callable(original):  # pragma: no cover - defensive against Rich refactors
        return

    def get_character_cell_size(character: str) -> int:
        if character == VARIATION_SELECTOR_16:
            return 1
        return original(character)

    # cached_cell_len() looks this name up in the module globals at call time, so
    # assigning into the module __dict__ propagates to every Rich width call.
    cells.__dict__["get_character_cell_size"] = get_character_cell_size

    cache_clear = getattr(cells.cached_cell_len, "cache_clear", None)
    if callable(cache_clear):
        cache_clear()

    _applied = True
