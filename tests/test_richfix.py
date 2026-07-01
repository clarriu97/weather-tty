from rich.cells import cell_len

from weather_tty._richfix import apply


# Importing weather_tty.cli applies the fix at import time; call it again to be
# explicit and to prove it is idempotent.
apply()
apply()


def test_variation_selector_emoji_measures_two_cells():
    # These all end with U+FE0F and are rendered as width-2 by modern terminals.
    for emoji in ["☀️", "☁️", "🌧️", "❄️", "⛈️", "🌤️"]:
        assert cell_len(emoji) == 2, f"{emoji!r} should measure 2 cells after the fix"


def test_plain_emoji_still_two_cells():
    # ⛅ has no variation selector and was already correct.
    assert cell_len("⛅") == 2


def test_ascii_width_unaffected():
    assert cell_len("Dubai, AE: 40C") == len("Dubai, AE: 40C")


def test_bare_variation_selector_counts_one():
    assert cell_len(chr(0xFE0F)) == 1
