"""weather_api.py - 天气数据获取模块（实时 + 历史）
依赖：
  - config.py 中的 CITY_COORDS / WEATHER_MAP / RAIN_INTENSITY_MAP
  - requests 库
  - streamlit（用于失败提示 st.warning）
"""

import requests
import streamlit as st
from datetime import datetime

from config import CITY_COORDS, WEATHER_MAP, RAIN_INTENSITY_MAP


def fetch_weather(city):
    """获取实时天气数据（Open-Meteo Forecast API）"""
    coord = CITY_COORDS[city]
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={coord['lat']}&longitude={coord['lon']}"
        "&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()["current"]
        code = data["weather_code"]
        return {
            "city": city,
            "temperature": data["temperature_2m"],
            "humidity": data["relative_humidity_2m"],
            "wind_speed": data["wind_speed_10m"],
            "weather_code": code,
            "weather": WEATHER_MAP.get(code, "未知"),
            "rain_intensity": RAIN_INTENSITY_MAP.get(code, 0),
            "is_history": False,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
    except Exception as e:
        st.warning(f"⚠️ 实时天气获取失败，使用模拟数据。错误：{e}")
        return {
            "city": city,
            "temperature": 22,
            "humidity": 60,
            "wind_speed": 5,
            "weather_code": 1,
            "weather": "晴（模拟）",
            "rain_intensity": 0,
            "is_history": False,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }


def fetch_historical_weather(city, date):
    """获取历史天气数据（Open-Meteo Archive API）"""
    coord = CITY_COORDS[city]
    date_str = date.strftime("%Y-%m-%d")
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={coord['lat']}&longitude={coord['lon']}"
        f"&start_date={date_str}&end_date={date_str}"
        "&daily=temperature_2m_mean,relative_humidity_2m_mean,weather_code,wind_speed_10m_max"
        "&timezone=auto"
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()["daily"]
        code = data["weather_code"][0]
        return {
            "city": city,
            "date": date_str,
            "temperature": data["temperature_2m_mean"][0],
            "humidity": data["relative_humidity_2m_mean"][0],
            "wind_speed": data["wind_speed_10m_max"][0],
            "weather_code": code,
            "weather": WEATHER_MAP.get(code, "未知"),
            "rain_intensity": RAIN_INTENSITY_MAP.get(code, 0),
            "is_history": True,
        }
    except Exception as e:
        st.warning(f"⚠️ 历史天气获取失败，使用模拟数据。错误：{e}")
        return {
            "city": city,
            "date": date_str,
            "temperature": 20,
            "humidity": 55,
            "wind_speed": 4,
            "weather_code": 1,
            "weather": "晴（模拟）",
            "rain_intensity": 0,
            "is_history": True,
        }
