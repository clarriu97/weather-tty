import io

import rich.cells as cells
from rich.cells import cell_len
from rich.console import Console

from weather_tty import _richfix
from weather_tty._richfix import VARIATION_SELECTOR_16, apply


# Importing weather_tty.cli applies the fix at import time; call it again to be
# explicit and to prove it is idempotent.
apply()
apply()


def test_variation_selector_emoji_measures_two_cells():
    # These all end with U+FE0F and are rendered as width-2 by modern terminals.
    for emoji in ["☀️", "☁️", "🌧️", "❄️", "⛈️", "🌤️"]:
        assert cell_len(emoji) == 2, f"{emoji!r} should measure 2 cells"


def test_plain_emoji_still_two_cells():
    # ⛅ has no variation selector and was already correct.
    assert cell_len("⛅") == 2


def test_ascii_width_unaffected():
    assert cell_len("Dubai, AE: 40C") == len("Dubai, AE: 40C")


def test_render_with_variation_selector_does_not_crash():
    """Rendering exercises Rich's real width call sites.

    Regression test for the crash on Rich >= 14.3:
        TypeError: get_character_cell_size() takes 1 positional argument but 2
        were given
    """
    console = Console(file=io.StringIO(), width=40)
    console.print("☀️ Dubai, AE: 40C")


def test_noop_when_rich_already_measures_two_cells(monkeypatch):
    """On Rich >= 14.3 the probe emoji already measures 2 cells, so apply() must
    leave Rich's own get_character_cell_size untouched."""
    monkeypatch.setattr(_richfix, "_applied", False)
    original = cells.get_character_cell_size
    monkeypatch.setattr(cells, "cell_len", lambda _text: 2)

    apply()

    assert cells.get_character_cell_size is original


def test_patches_and_forwards_extra_args_on_older_rich(monkeypatch):
    """When Rich under-measures the probe emoji, apply() installs a shim. It must
    forward any extra args (e.g. Rich 14.3's unicode_version) to the original."""
    monkeypatch.setattr(_richfix, "_applied", False)
    calls: list[tuple] = []

    def fake_original(character, *args, **kwargs):
        calls.append((character, args, kwargs))
        return 1

    monkeypatch.setattr(cells, "cell_len", lambda _text: 1)
    monkeypatch.setattr(cells, "get_character_cell_size", fake_original)

    apply()
    shim = cells.get_character_cell_size

    # Bare variation selector is forced to one cell without touching the original.
    assert shim(VARIATION_SELECTOR_16) == 1
    assert shim(VARIATION_SELECTOR_16, "auto") == 1
    assert calls == []

    # Any other character is delegated, extra positional/keyword args and all.
    assert shim("a") == 1
    assert shim("a", "auto") == 1
    assert calls == [("a", (), {}), ("a", ("auto",), {})]
