from weather_tty.formatting import code_to_emoji, format_line

def test_code_to_emoji_known():
    assert code_to_emoji(0) == "☀️"

def test_format_line_metric():
    s = format_line("Pamplona, ES", 12.3, 24.9, 1.6, 22.4, "2025-10-20T08:10", "2025-10-20T19:14", 2, "metric")
    assert "Pamplona, ES" in s
    assert "°C" in s
    assert "rain 1.6mm" in s
    assert "08:10" in s and "19:14" in s

def test_format_line_imperial_converts_rain():
    s = format_line("NYC, US", 50, 77, 25.4, 10, "2025-10-20T06:10", "2025-10-20T18:12", 61, "imperial")
    assert "rain 1.0in" in s  # 25.4 mm -> 1.0 in
