import pytest
from weather_particles.core.term_mapping import season_image

def test_clear_weather():
    result = season_image("晴")
    assert result["mode"] == "clear"
    assert result["solar_term"] == "立夏"

def test_rain_weather():
    result = season_image("大雨")
    assert result["mode"] == "rain"
    assert result["solar_term"] == "雨水"

def test_thunder_weather():
    # 雷雨必须优先判断
    result = season_image("雷雨")
    assert result["mode"] == "thunder"
    assert result["solar_term"] == "惊蛰"