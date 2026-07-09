import json
import math
import random
import requests
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="天象·气象幻境",
    page_icon="☁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 城市列表 ====================
CITY_COORDS = {
    # 直辖市
    "北京": {"lat": 39.9042, "lon": 116.4074},
    "上海": {"lat": 31.2304, "lon": 121.4737},
    "天津": {"lat": 39.3434, "lon": 117.3616},
    "重庆": {"lat": 29.4316, "lon": 106.9123},
    # 东北地区
    "哈尔滨": {"lat": 45.8038, "lon": 126.5349},
    "长春": {"lat": 43.8171, "lon": 125.3235},
    "沈阳": {"lat": 41.8057, "lon": 123.4315},
    "大连": {"lat": 38.9140, "lon": 121.6147},
    # 华北地区
    "呼和浩特": {"lat": 40.8426, "lon": 111.7490},
    "太原": {"lat": 37.8706, "lon": 112.5489},
    "石家庄": {"lat": 38.0428, "lon": 114.5149},
    "济南": {"lat": 36.6512, "lon": 117.1201},
    "青岛": {"lat": 36.0671, "lon": 120.3826},
    # 西北地区
    "乌鲁木齐": {"lat": 43.8256, "lon": 87.6168},
    "拉萨": {"lat": 29.6520, "lon": 91.1721},
    "西宁": {"lat": 36.6171, "lon": 101.7778},
    "兰州": {"lat": 36.0611, "lon": 103.8343},
    "银川": {"lat": 38.4872, "lon": 106.2309},
    # 华东地区
    "南京": {"lat": 32.0603, "lon": 118.7969},
    "杭州": {"lat": 30.2741, "lon": 120.1551},
    "合肥": {"lat": 31.8206, "lon": 117.2272},
    "南昌": {"lat": 28.6820, "lon": 115.8579},
    "福州": {"lat": 26.0745, "lon": 119.2965},
    "台北": {"lat": 25.0330, "lon": 121.5654},
    "厦门": {"lat": 24.4798, "lon": 118.0894},
    "宁波": {"lat": 29.8683, "lon": 121.5440},
    "温州": {"lat": 27.9938, "lon": 120.6994},
    # 华中地区
    "郑州": {"lat": 34.7466, "lon": 113.6254},
    "武汉": {"lat": 30.5928, "lon": 114.3055},
    "长沙": {"lat": 28.2282, "lon": 112.9388},
    # 华南地区
    "广州": {"lat": 23.1291, "lon": 113.2644},
    "深圳": {"lat": 22.5431, "lon": 114.0579},
    "南宁": {"lat": 22.8170, "lon": 108.3665},
    "海口": {"lat": 20.0444, "lon": 110.1993},
    "三亚": {"lat": 18.2528, "lon": 109.5119},
    "香港": {"lat": 22.3193, "lon": 114.1694},
    "澳门": {"lat": 22.1987, "lon": 113.5439},
    # 西南地区
    "成都": {"lat": 30.5728, "lon": 104.0668},
    "贵阳": {"lat": 26.6470, "lon": 106.6302},
    "昆明": {"lat": 25.0389, "lon": 102.7183},
    # 特色城市
    "敦煌": {"lat": 40.1421, "lon": 94.6620},
    "大理": {"lat": 25.6065, "lon": 100.2676},
    "丽江": {"lat": 26.8721, "lon": 100.2330},
    "张家界": {"lat": 29.3998, "lon": 110.4784},
    "苏州": {"lat": 31.2989, "lon": 120.5853},
    "无锡": {"lat": 31.4912, "lon": 120.3119},
    "佛山": {"lat": 23.0215, "lon": 113.1214},
    "东莞": {"lat": 23.0207, "lon": 113.7518},
    "珠海": {"lat": 22.2707, "lon": 113.5767},
    "桂林": {"lat": 25.2736, "lon": 110.2903},
    "黄山": {"lat": 29.7147, "lon": 118.3155},
}

WEATHER_MAP = {
    0: "晴",
    1: "少云",
    2: "多云",
    3: "阴",
    45: "雾",
    48: "雾",
    51: "小雨",
    53: "中雨",
    55: "大雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    95: "雷雨",
    96: "雷雨",
    99: "雷雨",
}

# ==================== 天气获取 ====================
def fetch_weather(city):
    coord = CITY_COORDS[city]
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={coord['lat']}&longitude={coord['lon']}"
        "&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
    )
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()["current"]
    return {
        "city": city,
        "temperature": data["temperature_2m"],
        "humidity": data["relative_humidity_2m"],
        "wind_speed": data["wind_speed_10m"],
        "weather_code": data["weather_code"],
        "weather": WEATHER_MAP.get(data["weather_code"], "未知"),
        "is_history": False,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }

def fetch_historical_weather(city, date):
    """获取某城市某一天的历史天气数据"""
    coord = CITY_COORDS[city]
    date_str = date.strftime("%Y-%m-%d")
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={coord['lat']}&longitude={coord['lon']}"
        f"&start_date={date_str}&end_date={date_str}"
        "&daily=temperature_2m_mean,relative_humidity_2m_mean,weather_code,wind_speed_10m_max"
        "&timezone=auto"
    )
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()["daily"]
    return {
        "city": city,
        "date": date_str,
        "temperature": data["temperature_2m_mean"][0],
        "humidity": data["relative_humidity_2m_mean"][0],
        "wind_speed": data["wind_speed_10m_max"][0],
        "weather_code": data["weather_code"][0],
        "weather": WEATHER_MAP.get(data["weather_code"][0], "未知"),
        "is_history": True,
    }

# ==================== 节气映射 ====================
def season_image(weather):
    # 优先判断“雷”（雷雨同时包含雷和雨，必须放前面）
    if "雷" in weather:
        return {
            "name": "惊蛰如雷",
            "solar_term": "惊蛰",
            "mode": "thunder",
            "poem": "雷声惊醒地下的生机，光在云层中裂开。",
            "colors": ["#101018", "#312e81", "#facc15", "#f8fafc"],
        }
    if "雨" in weather:
        return {
            "name": "雨水如墨",
            "solar_term": "雨水",
            "mode": "rain",
            "poem": "雨落为墨，城市在水痕中晕开。",
            "colors": ["#0e1116", "#1f2937", "#64748b", "#dbeafe"],
        }
    if "雪" in weather:
        return {
            "name": "霜降如雪",
            "solar_term": "霜降",
            "mode": "snow",
            "poem": "寒意凝结成白，城市被轻轻覆盖。",
            "colors": ["#0f172a", "#334155", "#e2e8f0", "#ffffff"],
        }
    if "雾" in weather or "阴" in weather or "云" in weather:
        return {
            "name": "清明如烟",
            "solar_term": "清明",
            "mode": "mist",
            "poem": "雾气如烟，边界被风慢慢抹去。",
            "colors": ["#111827", "#475569", "#94a3b8", "#e5e7eb"],
        }
    return {
        "name": "立夏流光",
        "solar_term": "立夏",
        "mode": "clear",
        "poem": "晴光流动，热度在空气中慢慢生长。",
        "colors": ["#08111f", "#0f766e", "#f59e0b", "#fef3c7"],
    }

# ==================== Canvas 构建 ====================
def build_canvas(weather_data, image_data, interaction_mode="排斥"):
    is_history = weather_data.get("is_history", False)
    date_label = weather_data.get("date", "")
    mode_label = "⏳ HISTORICAL" if is_history else "🌐 LIVE"

    payload = {
        "city": weather_data["city"],
        "temperature": weather_data["temperature"],
        "humidity": weather_data["humidity"],
        "wind": weather_data["wind_speed"],
        "weather": weather_data["weather"],
        "mode": image_data["mode"],
        "colors": image_data["colors"],
        "is_history": is_history,
        "date": date_label,
        "mode_label": mode_label,
        "interaction_mode": interaction_mode,
    }

    return f"""
    <div class="stage">
      <canvas id="sky"></canvas>
      <div class="overlay">
        <div class="label">{mode_label} {date_label}</div>
        <h1>{weather_data["city"]}</h1>
        <h2>{image_data["name"]}</h2>
        <p>{image_data["poem"]}</p>
        <div class="metrics">
          <span>温度 {weather_data["temperature"]}°C</span>
          <span>湿度 {weather_data["humidity"]}%</span>
          <span>风速 {weather_data["wind_speed"]} km/h</span>
          <span>{weather_data["weather"]}</span>
        </div>
      </div>
    </div>

    <style>
      .stage {{
        position: relative;
        width: 100%;
        height: 680px;
        overflow: hidden;
        border-radius: 8px;
        background: #080b10;
        cursor: crosshair;
      }}
      #sky {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
      }}
      .overlay {{
        position: absolute;
        left: 42px;
        bottom: 38px;
        max-width: 720px;
        color: white;
        font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
      }}
      .label {{
        margin-bottom: 14px;
        color: rgba(255,255,255,.58);
        font-size: 12px;
        letter-spacing: .16em;
        font-weight: 700;
      }}
      .overlay h1 {{
        margin: 0;
        font-size: 86px;
        line-height: .9;
        font-weight: 900;
      }}
      .overlay h2 {{
        margin: 16px 0 10px;
        font-size: 34px;
        font-weight: 700;
      }}
      .overlay p {{
        margin: 0 0 24px;
        color: rgba(255,255,255,.72);
        font-size: 20px;
      }}
      .metrics {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }}
      .metrics span {{
        padding: 8px 12px;
        border: 1px solid rgba(255,255,255,.22);
        border-radius: 999px;
        background: rgba(255,255,255,.08);
        color: rgba(255,255,255,.82);
        font-size: 13px;
      }}
    </style>

    <script>
      const data = {json.dumps(payload, ensure_ascii=False)};
      const canvas = document.getElementById("sky");
      const ctx = canvas.getContext("2d");

      let width = 0;
      let height = 0;
      let particles = [];

      // ========== 鼠标交互变量 ==========
      let mouseX = -9999;
      let mouseY = -9999;
      let mouseActive = false;
      let ripples = [];
      let explosionActive = false;
      let explosionTime = 0;

      canvas.addEventListener('mousemove', function(e) {{
        const rect = canvas.getBoundingClientRect();
        mouseX = (e.clientX - rect.left) * (canvas.width / rect.width);
        mouseY = (e.clientY - rect.top) * (canvas.height / rect.height);
        mouseActive = true;
      }});

      canvas.addEventListener('mouseleave', function() {{
        mouseActive = false;
        mouseX = -9999;
        mouseY = -9999;
      }});

      canvas.addEventListener('click', function(e) {{
        const rect = canvas.getBoundingClientRect();
        const cx = (e.clientX - rect.left) * (canvas.width / rect.width);
        const cy = (e.clientY - rect.top) * (canvas.height / rect.height);

        // 涟漪（保留）
        for (let i = 0; i < 5; i++) {{
          ripples.push({{
            x: cx,
            y: cy,
            radius: 10 + i * 8,
            maxRadius: Math.max(width, height) * 0.5,
            alpha: 0.9 - i * 0.12,
            speed: 4 + i * 1.5,
            life: 0
          }});
        }}

        // 爆炸模式：对附近粒子施加向外速度
        if (data.interaction_mode === "爆炸") {{
          const explodeRadius = 150 * window.devicePixelRatio;
          for (const p of particles) {{
            const dx = p.x - cx;
            const dy = p.y - cy;
            const dist = Math.sqrt(dx*dx + dy*dy);
            if (dist < explodeRadius && dist > 1) {{
              const force = (1 - dist / explodeRadius) * 12;
              p.vx += (dx / dist) * force;
              p.vy += (dy / dist) * force;
            }}
          }}
          explosionActive = true;
          explosionTime = Date.now();
        }}
      }});

      function resize() {{
        const rect = canvas.getBoundingClientRect();
        width = rect.width * window.devicePixelRatio;
        height = rect.height * window.devicePixelRatio;
        canvas.width = width;
        canvas.height = height;
      }}

      function rand(min, max) {{
        return Math.random() * (max - min) + min;
      }}

      function createParticle() {{
        const tempFactor = Math.max(0.4, Math.min(2.2, data.temperature / 18));
        const humidFactor = Math.max(0.4, data.humidity / 55);
        const windFactor = Math.max(0.5, data.wind / 10);

        let p = {{
          x: rand(0, width),
          y: rand(0, height),
          vx: rand(-0.4, 0.4) * windFactor,
          vy: rand(0.4, 1.4) * humidFactor,
          r: rand(1, 3) * tempFactor,
          life: rand(80, 220),
          color: data.colors[Math.floor(rand(0, data.colors.length))],
          alpha: rand(0.18, 0.88)
        }};

        if (data.mode === "rain") {{
          p.vx = rand(-0.5, 0.5) + windFactor * 0.4;
          p.vy = rand(5, 10) * humidFactor;
          p.r = rand(0.8, 1.8);
        }}

        if (data.mode === "snow") {{
          p.vx = rand(-0.7, 0.7) * windFactor;
          p.vy = rand(0.5, 1.8);
          p.r = rand(1.5, 4.2);
        }}

        if (data.mode === "mist") {{
          p.vx = rand(-0.5, 0.5) * windFactor;
          p.vy = rand(-0.25, 0.25);
          p.r = rand(18, 56) * humidFactor;
          p.alpha = rand(0.03, 0.11);
        }}

        if (data.mode === "thunder") {{
          p.vx = rand(-1.8, 1.8);
          p.vy = rand(-1.8, 1.8);
          p.r = rand(1, 4);
          p.alpha = rand(0.35, 1);
        }}

        return p;
      }}

      function init() {{
        resize();
        const count = Math.floor(220 + data.humidity * 3 + data.wind * 8);
        particles = Array.from({{ length: count }}, createParticle);
      }}

      function drawBackground() {{
        const gradient = ctx.createLinearGradient(0, 0, width, height);
        gradient.addColorStop(0, data.colors[0]);
        gradient.addColorStop(0.55, data.colors[1]);
        gradient.addColorStop(1, "#05070b");
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);
      }}

      function drawThunder() {{
        if (data.mode !== "thunder") return;
        if (Math.random() < 0.035) {{
          ctx.save();
          ctx.strokeStyle = "rgba(255,245,170,.9)";
          ctx.lineWidth = 3 * window.devicePixelRatio;
          ctx.beginPath();
          let x = rand(width * 0.25, width * 0.8);
          let y = 0;
          ctx.moveTo(x, y);
          for (let i = 0; i < 10; i++) {{
            x += rand(-60, 60) * window.devicePixelRatio;
            y += rand(35, 80) * window.devicePixelRatio;
            ctx.lineTo(x, y);
          }}
          ctx.stroke();
          ctx.restore();
          ctx.fillStyle = "rgba(255,255,255,.12)";
          ctx.fillRect(0, 0, width, height);
        }}
      }}

      function drawRipples() {{
        for (let i = ripples.length - 1; i >= 0; i--) {{
          const r = ripples[i];
          r.radius += r.speed;
          r.alpha *= 0.98;
          r.life++;
          if (r.alpha < 0.01 || r.radius > r.maxRadius) {{
            ripples.splice(i, 1);
            continue;
          }}
          ctx.save();
          ctx.globalAlpha = r.alpha * 0.4;
          ctx.strokeStyle = "#ffffff";
          ctx.lineWidth = 2 * (1 - r.radius / r.maxRadius);
          ctx.shadowColor = "rgba(255,255,255,0.5)";
          ctx.shadowBlur = 20;
          ctx.beginPath();
          ctx.arc(r.x, r.y, r.radius, 0, Math.PI * 2);
          ctx.stroke();
          ctx.restore();
        }}
      }}

      function drawParticle(p) {{
        ctx.save();
        ctx.globalAlpha = p.alpha;
        ctx.fillStyle = p.color;
        ctx.strokeStyle = p.color;

        if (data.mode === "rain") {{
          ctx.lineWidth = p.r * window.devicePixelRatio;
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p.x + p.vx * 6, p.y + p.vy * 3);
          ctx.stroke();
        }} else {{
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.r * window.devicePixelRatio, 0, Math.PI * 2);
          ctx.fill();
        }}

        ctx.restore();
      }}

      function updateParticle(p) {{
        const mode = data.interaction_mode || "排斥";
        // ---------- 鼠标交互 ----------
        if (mouseActive) {{
          const dx = p.x - mouseX;
          const dy = p.y - mouseY;
          const dist2 = dx * dx + dy * dy;
          const maxDist = 80 * window.devicePixelRatio;
          if (dist2 < maxDist * maxDist && dist2 > 0.1) {{
            const dist = Math.sqrt(dist2);
            const force = (1 - dist / maxDist) * 2.5;

            if (mode === "排斥") {{
              p.vx += (dx / dist) * force;
              p.vy += (dy / dist) * force;
            }} else if (mode === "吸引") {{
              p.vx -= (dx / dist) * force * 0.7;
              p.vy -= (dy / dist) * force * 0.7;
            }} else if (mode === "漩涡") {{
              const angle = Math.atan2(dy, dx);
              const perpX = -Math.sin(angle);
              const perpY = Math.cos(angle);
              const swirlForce = force * 0.9;
              p.vx += perpX * swirlForce;
              p.vy += perpY * swirlForce;
              p.vx -= (dx / dist) * force * 0.15;
              p.vy -= (dy / dist) * force * 0.15;
            }}
          }}
        }}

        if (data.mode === "snow") {{
          p.x += p.vx + Math.sin(Date.now() * 0.001 + p.y * 0.01) * 0.35;
          p.y += p.vy;
        }} else {{
          p.x += p.vx;
          p.y += p.vy;
        }}

        p.vx *= 0.98;
        p.vy *= 0.98;

        p.life -= 1;

        if (
          p.x < -100 || p.x > width + 100 ||
          p.y < -100 || p.y > height + 100 ||
          p.life <= 0
        ) {{
          Object.assign(p, createParticle());
          p.y = data.mode === "rain" || data.mode === "snow" ? -20 : rand(0, height);
        }}
      }}

      function animate() {{
        drawBackground();
        ctx.globalCompositeOperation = data.mode === "mist" ? "screen" : "source-over";
        for (const p of particles) {{
          updateParticle(p);
          drawParticle(p);
        }}
        ctx.globalCompositeOperation = "source-over";
        drawRipples();
        drawThunder();
        if (explosionActive && Date.now() - explosionTime > 2000) {{
          explosionActive = false;
        }}
        requestAnimationFrame(animate);
      }}

      window.addEventListener("resize", init);
      init();
      animate();
    </script>
    """
# ==================== 界面 ====================
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

    # 搜索框
    search_term = st.text_input("🔍 搜索城市", placeholder="输入城市名...", key="city_search")
    if search_term:
        filtered_cities = [city for city in CITY_COORDS.keys() if search_term.lower() in city.lower()]
    else:
        filtered_cities = list(CITY_COORDS.keys())
    if not filtered_cities:
        st.warning("未找到匹配的城市，显示全部")
        filtered_cities = list(CITY_COORDS.keys())

    city = st.selectbox("选择城市", filtered_cities, key="city_select")

    # ========== 交互模式 ==========
    st.divider()
    st.subheader("🖱️ 鼠标交互")
    interaction_mode = st.selectbox(
        "选择交互模式",
        options=["排斥", "吸引", "漩涡", "爆炸"],
        index=0,
        key="interaction_mode"
    )

    # ========== 历史回放 ==========
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

# ==================== 主内容 ====================
try:
    # 判断使用实时还是历史数据
    if history_mode and st.session_state.get("play_history", False):
        city = st.session_state["history_city"]
        date = st.session_state["history_date"]
        weather_data = fetch_historical_weather(city, date)
        # 自动推进日期（播放效果）
        st.session_state["history_date"] += timedelta(days=1)
        # 控制播放速度：通过定时器控制刷新频率，但 Streamlit 无法精确控制间隔，用 sleep 模拟
        # 这里用 st.rerun() 实现连续刷新
    else:
        weather_data = fetch_weather(city)

    image_data = season_image(weather_data["weather"])

    st.components.v1.html(
        build_canvas(weather_data, image_data, interaction_mode),
        height=700,
        scrolling=False
    )

    # 显示指标
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("城市", weather_data["city"])
    col2.metric("温度", f"{weather_data['temperature']}°C")
    col3.metric("湿度", f"{weather_data['humidity']}%")
    col4.metric("风速", f"{weather_data['wind_speed']} km/h")

    # 备注信息
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

    # 如果处于播放模式，自动刷新
    if history_mode and st.session_state.get("play_history", False):
        import time
        speed = st.session_state.get("history_speed", 1)
        # 速度越快，刷新间隔越短
        delay = max(0.5, 3.0 / speed)
        time.sleep(delay)
        st.rerun()

except Exception as e:
    st.error("天气数据获取失败，请稍后重试。")
    st.code(str(e))