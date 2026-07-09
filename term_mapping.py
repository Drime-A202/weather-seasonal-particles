"""term_mapping.py - 节气意象映射模块
根据天气关键词映射到节气视觉风格（包含配色、粒子模式、文案）
"""


def season_image(weather):
    """将天气映射为节气意象

    返回：
      name:       视觉名称（如「立夏流光」）
      solar_term: 节气名
      mode:       粒子模式（clear / rain / snow / mist / thunder）
      poem:       诗句
      colors:     5 色配色数组（深→浅），供 Canvas 使用
    """
    # 优先判断「雷」：雷雨同时包含「雷」和「雨」，必须放前面
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
