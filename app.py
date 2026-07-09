"""app.py - Streamlit 主入口
职责：UI 布局（页头、侧边栏、主内容） + 业务逻辑编排

依赖模块：
  - config.py       ：CITY_COORDS
  - weather_api.py  ：fetch_weather / fetch_historical_weather
  - term_mapping.py ：season_image
  - canvas_builder.py：build_canvas
"""

import time
import streamlit as st
from datetime import datetime, timedelta

from config import CITY_COORDS
from weather_api import fetch_weather, fetch_historical_weather
from term_mapping import season_image
from canvas_builder import build_canvas


# ==================== 页面基础配置 ====================
st.set_page_config(
    page_title="天象·气象幻境",
    page_icon="☁",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== 全局样式 ====================
st.markdown(
    """
    <style>
      .block-container { padding-top: 2rem; padding-bottom: 2rem; }
      [data-testid="stSidebar"] { background: #101318; }
      [data-testid="stSidebar"] * { color: white; }
      .intro { margin-bottom: 1.4rem; }
      .intro h1 { margin-bottom: .4rem; font-size: 42px; line-height: 1.08; }
      .intro p { color: #5b6472; font-size: 17px; }
      .note { padding: 16px 18px; border-left: 4px solid #111827; background: #f3f4f6; color: #374151; font-size: 15px; }
    </style>
    """,
    unsafe_allow_html=True
)


# ==================== 页头 ====================
st.markdown(
    """
    <div class="intro">
      <h1>天象·气象幻境</h1>
      <p>以实时天气数据驱动粒子系统，将城市气象转译为传统节气物候意象。</p>
    </div>
    """,
    unsafe_allow_html=True
)


# ==================== 侧边栏 ====================
with st.sidebar:
    st.title("城市气象")

    # 城市搜索 + 选择
    search_term = st.text_input("🔍 搜索城市", placeholder="输入城市名...", key="city_search")
    if search_term:
        filtered_cities = [city for city in CITY_COORDS.keys() if search_term.lower() in city.lower()]
    else:
        filtered_cities = list(CITY_COORDS.keys())
    if not filtered_cities:
        st.warning("未找到匹配的城市，显示全部")
        filtered_cities = list(CITY_COORDS.keys())

    city = st.selectbox("选择城市", filtered_cities, key="city_select")

    st.divider()
    st.subheader("🖱️ 鼠标交互")
    interaction_mode = st.selectbox(
        "选择交互模式",
        options=["排斥", "吸引", "漩涡", "爆炸"],
        index=0,
        key="interaction_mode"
    )

    st.divider()
    st.subheader("⏳ 历史回放")

    history_mode = st.toggle("开启历史回放", value=False)

    if history_mode:
        col1, col2 = st.columns(2)
        with col1:
            default_date = datetime.now() - timedelta(days=30)
            selected_date = st.date_input("选择日期", default_date)
        with col2:
            speed = st.select_slider("速度", options=[1, 2, 5, 10], value=1)

        if st.button("▶ 播放", use_container_width=True):
            st.session_state["play_history"] = True
            st.session_state["history_date"] = selected_date
            st.session_state["history_speed"] = speed
            st.session_state["history_city"] = city
        if st.button("⏹ 停止", use_container_width=True):
            st.session_state["play_history"] = False

    st.caption("数据来源：Open-Meteo 实时/历史天气接口")


# ==================== 主内容区 ====================
try:
    # 1) 取天气数据（实时 或 历史回放）
    if history_mode and st.session_state.get("play_history", False):
        city = st.session_state["history_city"]
        date = st.session_state["history_date"]
        weather_data = fetch_historical_weather(city, date)
        st.session_state["history_date"] += timedelta(days=1)
    else:
        weather_data = fetch_weather(city)

    # 2) 映射到节气意象
    image_data = season_image(weather_data["weather"])

    # 3) 渲染粒子画布
    st.components.v1.html(
        build_canvas(weather_data, image_data, interaction_mode),
        height=700,
        scrolling=False
    )

    # 4) 指标卡片
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("城市", weather_data["city"])
    col2.metric("温度", f"{weather_data['temperature']}°C")
    col3.metric("湿度", f"{weather_data['humidity']}%")
    col4.metric("风速", f"{weather_data['wind_speed']} km/h")

    # 5) 说明文本
    history_tag = "（历史数据）" if weather_data.get("is_history", False) else "（实时数据）"
    st.markdown(
        f"""
        <div class="note">
        当前天气为 <b>{weather_data["weather"]}</b> {history_tag}，系统将其映射为
        <b>{image_data["solar_term"]}</b> 意象：<b>{image_data["name"]}</b>。
        温度影响粒子尺度，湿度影响粒子密度，风速影响运动方向与速度，天气类型决定整体视觉语法。
        </div>
        """,
        unsafe_allow_html=True
    )

    # 6) 历史回放的延时 + 重渲染
    if history_mode and st.session_state.get("play_history", False):
        speed = st.session_state.get("history_speed", 1)
        delay = max(0.5, 3.0 / speed)
        time.sleep(delay)
        st.rerun()

except Exception as e:
    st.error("天气数据获取失败，请稍后重试。")
    st.code(str(e))
