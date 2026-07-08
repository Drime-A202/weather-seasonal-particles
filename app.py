import json
import math
import random
import requests
import streamlit as st

st.set_page_config(
    page_title="天象·气象幻境",
    page_icon="☁",
    layout="wide",
    initial_sidebar_state="expanded"
)

CITY_COORDS = {
    "北京": {"lat": 39.9042, "lon": 116.4074},
    "上海": {"lat": 31.2304, "lon": 121.4737},
    "广州": {"lat": 23.1291, "lon": 113.2644},
    "杭州": {"lat": 30.2741, "lon": 120.1551},
    "成都": {"lat": 30.5728, "lon": 104.0668},
    "西安": {"lat": 34.3416, "lon": 108.9398},
    "哈尔滨": {"lat": 45.8038, "lon": 126.5349},
    "昆明": {"lat": 25.0389, "lon": 102.7183},
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
    }

def season_image(weather):
    if "雨" in weather:
        return {
            "name": "雨水如墨",
            "solar_term": "雨水",
            "mode": "rain",
            "poem": "雨落为墨，城市在水痕中晕开。",
            "colors": ["#0e1116", "#1f2937", "#64748b", "#dbeafe"],
        }

    if "雷" in weather:
        return {
            "name": "惊蛰如雷",
            "solar_term": "惊蛰",
            "mode": "thunder",
            "poem": "雷声惊醒地下的生机，光在云层中裂开。",
            "colors": ["#101018", "#312e81", "#facc15", "#f8fafc"],
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

def build_canvas(weather_data, image_data):
    payload = {
        "city": weather_data["city"],
        "temperature": weather_data["temperature"],
        "humidity": weather_data["humidity"],
        "wind": weather_data["wind_speed"],
        "weather": weather_data["weather"],
        "mode": image_data["mode"],
        "colors": image_data["colors"],
    }

    return f"""
    <div class="stage">
      <canvas id="sky"></canvas>
      <!-- 水墨晕染层 -->
      <canvas id="ink-layer"></canvas>
      <!-- 印章装饰 -->
      <div class="seal seal-left">气象</div>
      <div class="seal seal-right">天象</div>
      <!-- 古典边框 -->
      <div class="corner corner-tl"></div>
      <div class="corner corner-tr"></div>
      <div class="corner corner-bl"></div>
      <div class="corner corner-br"></div>
      <!-- 墨渍装饰 -->
      <div class="ink-spot ink-spot-1"></div>
      <div class="ink-spot ink-spot-2"></div>
      <div class="ink-spot ink-spot-3"></div>
      <div class="overlay">
        <div class="label">实时气象 · 节气物候</div>
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
      @import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;600&display=swap');

      .stage {{
        position: relative;
        width: 100%;
        height: 680px;
        overflow: hidden;
        border-radius: 8px;
        background: #0d0f12;
        border: 1px solid rgba(255, 255, 255, 0.06);
      }}

      #sky {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
      }}

      #ink-layer {{
        position: absolute;
        inset: 0;
        width: 100%;
        height: 100%;
        opacity: 0.35;
        mix-blend-mode: screen;
      }}

      /* 印章风格 - 朱砂红色 */
      .seal {{
        position: absolute;
        width: 56px;
        height: 56px;
        border: 2px solid rgba(180, 60, 50, 0.7);
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Ma Shan Zheng', cursive;
        font-size: 18px;
        color: rgba(180, 60, 50, 0.75);
        opacity: 0.55;
        background: radial-gradient(circle, rgba(180, 60, 50, 0.08) 0%, transparent 70%);
        z-index: 5;
      }}

      .seal-left {{
        left: 24px;
        top: 24px;
        transform: rotate(-5deg);
      }}

      .seal-right {{
        right: 24px;
        top: 24px;
        transform: rotate(8deg);
      }}

      /* 古典边角装饰 - 水墨线条 */
      .corner {{
        position: absolute;
        width: 40px;
        height: 40px;
        z-index: 4;
      }}

      .corner-tl {{
        top: 12px;
        left: 12px;
        border-left: 1px solid rgba(150, 150, 150, 0.25);
        border-top: 1px solid rgba(150, 150, 150, 0.25);
      }}

      .corner-tr {{
        top: 12px;
        right: 12px;
        border-right: 1px solid rgba(150, 150, 150, 0.25);
        border-top: 1px solid rgba(150, 150, 150, 0.25);
      }}

      .corner-bl {{
        bottom: 12px;
        left: 12px;
        border-left: 1px solid rgba(150, 150, 150, 0.25);
        border-bottom: 1px solid rgba(150, 150, 150, 0.25);
      }}

      .corner-br {{
        bottom: 12px;
        right: 12px;
        border-right: 1px solid rgba(150, 150, 150, 0.25);
        border-bottom: 1px solid rgba(150, 150, 150, 0.25);
      }}

      /* 墨渍晕染效果 */
      .ink-spot {{
        position: absolute;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(100, 100, 110, 0.12) 0%, transparent 60%);
        filter: blur(20px);
        z-index: 3;
        animation: ink-flow 15s ease-in-out infinite alternate;
      }}

      .ink-spot-1 {{
        width: 280px;
        height: 280px;
        top: 15%;
        left: 60%;
        animation-delay: 0s;
      }}

      .ink-spot-2 {{
        width: 200px;
        height: 200px;
        top: 55%;
        left: 25%;
        animation-delay: 3s;
      }}

      .ink-spot-3 {{
        width: 320px;
        height: 320px;
        top: 40%;
        left: 70%;
        animation-delay: 6s;
      }}

      @keyframes ink-flow {{
        0% {{ transform: scale(1) rotate(0deg); opacity: 0.15; }}
        50% {{ transform: scale(1.15) rotate(3deg); opacity: 0.22; }}
        100% {{ transform: scale(1) rotate(-2deg); opacity: 0.18; }}
      }}

      .overlay {{
        position: absolute;
        left: 48px;
        bottom: 42px;
        max-width: 720px;
        color: white;
        font-family: 'Noto Serif SC', serif;
        z-index: 10;
      }}

      .label {{
        margin-bottom: 16px;
        color: rgba(200,200,200,.5);
        font-size: 11px;
        letter-spacing: .2em;
        font-weight: 400;
      }}

      .overlay h1 {{
        margin: 0;
        font-size: 96px;
        line-height: .85;
        font-weight: 400;
        font-family: 'Ma Shan Zheng', cursive;
        letter-spacing: 8px;
        text-shadow: 0 4px 30px rgba(0, 0, 0, 0.5), 0 0 60px rgba(100, 100, 120, 0.2);
      }}

      .overlay h2 {{
        margin: 20px 0 12px;
        font-size: 36px;
        font-weight: 400;
        font-family: 'Ma Shan Zheng', cursive;
        letter-spacing: 3px;
      }}

      .overlay p {{
        margin: 0 0 28px;
        color: rgba(220,220,220,.75);
        font-size: 18px;
        line-height: 1.6;
        font-family: 'Noto Serif SC', serif;
        letter-spacing: 1px;
        border-left: 2px solid rgba(150, 150, 150, 0.2);
        padding-left: 14px;
      }}

      .metrics {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
      }}

      .metrics span {{
        padding: 10px 16px;
        border: 1px solid rgba(150,150,150,.15);
        border-radius: 4px;
        background: rgba(255,255,255,.04);
        color: rgba(255,255,255,.85);
        font-size: 14px;
        font-family: 'Noto Serif SC', serif;
        letter-spacing: 0.5px;
        backdrop-filter: blur(8px);
      }}
    </style>

    <script>
      const data = {json.dumps(payload, ensure_ascii=False)};
      const canvas = document.getElementById("sky");
      const ctx = canvas.getContext("2d");
      const inkCanvas = document.getElementById("ink-layer");
      const inkCtx = inkCanvas.getContext("2d");

      let width = 0;
      let height = 0;
      let particles = [];
      let inkBlots = [];

      function resize() {{
        const rect = canvas.getBoundingClientRect();
        width = rect.width * window.devicePixelRatio;
        height = rect.height * window.devicePixelRatio;
        canvas.width = width;
        canvas.height = height;
        inkCanvas.width = width;
        inkCanvas.height = height;
      }}

      // 水墨晕染层
      function createInkBlot() {{
        return {{
          x: rand(0, width),
          y: rand(0, height),
          r: rand(80, 180) * window.devicePixelRatio,
          alpha: rand(0.05, 0.15),
          drift: rand(-0.3, 0.3)
        }};
      }}

      function initInk() {{
        inkBlots = Array.from({{ length: 5 }}, createInkBlot);
      }}

      function drawInkLayer() {{
        inkCtx.clearRect(0, 0, width, height);
        for (const blot of inkBlots) {{
          blot.x += blot.drift;
          blot.alpha += rand(-0.005, 0.005);
          blot.alpha = Math.max(0.03, Math.min(0.18, blot.alpha));

          const gradient = inkCtx.createRadialGradient(
            blot.x, blot.y, 0,
            blot.x, blot.y, blot.r
          );
          gradient.addColorStop(0, `rgba(120, 125, 130, ${blot.alpha})`);
          gradient.addColorStop(0.5, `rgba(100, 105, 110, ${blot.alpha * 0.5})`);
          gradient.addColorStop(1, 'transparent');

          inkCtx.fillStyle = gradient;
          inkCtx.beginPath();
          inkCtx.arc(blot.x, blot.y, blot.r, 0, Math.PI * 2);
          inkCtx.fill();

          // 边界检测
          if (blot.x < -blot.r || blot.x > width + blot.r) {{
            blot.x = rand(0, width);
          }}
        }}
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
        initInk();
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
        if (data.mode === "snow") {{
          p.x += p.vx + Math.sin(Date.now() * 0.001 + p.y * 0.01) * 0.35;
          p.y += p.vy;
        }} else {{
          p.x += p.vx;
          p.y += p.vy;
        }}

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
        drawThunder();

        requestAnimationFrame(animate);
      }}

      window.addEventListener("resize", init);
      init();
      animate();
    </script>
    """

st.markdown(
    """
    <style>
      .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
      }

      [data-testid="stSidebar"] {
        background: #101318;
      }

      [data-testid="stSidebar"] * {
        color: white;
      }

      .intro {
        margin-bottom: 1.4rem;
      }

      .intro h1 {
        margin-bottom: .4rem;
        font-size: 42px;
        line-height: 1.08;
      }

      .intro p {
        color: #5b6472;
        font-size: 17px;
      }

      .note {
        padding: 16px 18px;
        border-left: 4px solid #111827;
        background: #f3f4f6;
        color: #374151;
        font-size: 15px;
      }
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

with st.sidebar:
    st.title("城市气象")
    city = st.selectbox("选择城市", list(CITY_COORDS.keys()))
    st.caption("数据来源：Open-Meteo 实时天气接口")

try:
    weather_data = fetch_weather(city)
    image_data = season_image(weather_data["weather"])

    st.components.v1.html(
        build_canvas(weather_data, image_data),
        height=700,
        scrolling=False
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("城市", weather_data["city"])
    col2.metric("温度", f"{weather_data['temperature']}°C")
    col3.metric("湿度", f"{weather_data['humidity']}%")
    col4.metric("风速", f"{weather_data['wind_speed']} km/h")

    st.markdown(
        f"""
        <div class="note">
        当前天气为 <b>{weather_data["weather"]}</b>，系统将其映射为
        <b>{image_data["solar_term"]}</b> 意象：<b>{image_data["name"]}</b>。
        温度影响粒子尺度，湿度影响粒子密度，风速影响运动方向与速度，天气类型决定整体视觉语法。
        </div>
        """,
        unsafe_allow_html=True
    )

except Exception as e:
    st.error("天气数据获取失败，请稍后重试。")
    st.code(str(e))