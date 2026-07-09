"""canvas_builder.py - 粒子画布构建模块
封装 build_canvas 函数，返回嵌入 Canvas+CSS+JS 的 HTML 字符串。
不依赖 Streamlit（仅依赖标准库 json）。
"""

import json


def build_canvas(weather_data, image_data, interaction_mode="排斥"):
    """构建节气粒子可视化画布

    参数：
      weather_data     - 天气数据字典（由 weather_api 返回）
      image_data       - 节气视觉数据字典（由 term_mapping 返回）
      interaction_mode - 鼠标交互模式：排斥 / 吸引 / 漩涡 / 爆炸

    返回：HTML 字符串（可直接注入 Streamlit 的 st.components.v1.html）
    """
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
        "rain_intensity": weather_data.get("rain_intensity", 0),
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
        const rainIntensity = data.rain_intensity || 0;

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
          const speedFactor = 0.8 + 0.4 * rainIntensity;
          const sizeFactor = 0.7 + 0.3 * rainIntensity;
          const baseVy = rand(6, 14) * humidFactor * speedFactor;
          p.vx = rand(-0.8, 0.8) + windFactor * 0.5;
          p.vy = baseVy;
          p.r = rand(0.8, 1.8) * sizeFactor;
          p._initVy = baseVy;
          p._initVx = p.vx;
          p.life = 999999;
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
        let baseCount = 220;
        if (data.mode === "rain") {{
          const rainIntensity = data.rain_intensity || 0;
          baseCount = 250 + rainIntensity * 70;
        }}
        const count = Math.floor(baseCount + data.humidity * 3 + data.wind * 8);
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
        }} else if (data.mode === "rain") {{
          if (p._initVy) {{
            p.vy += (p._initVy - p.vy) * 0.05;
          }}
          if (p._initVx) {{
            p.vx += (p._initVx - p.vx) * 0.02;
          }}
          p.x += p.vx;
          p.y += p.vy;
        }} else {{
          p.x += p.vx;
          p.y += p.vy;
        }}

        if (data.mode === "rain") {{
          p.vx *= 0.995;
        }} else {{
          p.vx *= 0.98;
          p.vy *= 0.98;
        }}

        if (data.mode !== "rain") {{
          p.life -= 1;
        }}

        const outOfBounds = p.x < -100 || p.x > width + 100 || p.y < -100 || p.y > height + 100;
        const lifeEnd = (data.mode !== "rain" && p.life <= 0);

        if (outOfBounds || lifeEnd) {{
          if (data.mode === "rain") {{
            p.x = rand(0, width);
            p.y = -rand(5, 30);
            p.vy = p._initVy || rand(6, 14) * 0.7;
            p.vx = (p._initVx || 0) + rand(-0.3, 0.3);
          }} else {{
            Object.assign(p, createParticle());
            p.y = rand(0, height);
          }}
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
