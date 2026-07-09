import pytest
from unittest.mock import patch, MagicMock
from weather_particles.api.weather_api import fetch_weather

@patch("weather_particles.api.weather_api.requests.get")
def test_fetch_weather_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "current": {
            "temperature_2m": 25.0,
            "relative_humidity_2m": 60,
            "weather_code": 0,
            "wind_speed_10m": 5.0
        }
    }
    mock_get.return_value = mock_response
    
    result = fetch_weather("北京")
    assert result["temperature"] == 25.0
    assert result["weather"] == "晴"