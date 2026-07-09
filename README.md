![GitHub last commit](https://img.shields.io/github/last-commit/Drime-A202/weather-seasonal-particles)
![GitHub repo size](https://img.shields.io/github/repo-size/Drime-A202/weather-seasonal-particles)
![License](https://img.shields.io/github/license/Drime-A202/weather-seasonal-particles)
![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)
# 天象 · 气象幻境

> 基于实时天气数据驱动的节气意象可视化 —— 让城市的气象转译为可感知的传统美学。

👉 **在线体验**：[https://weather-seasonal-particles-4i5wlj4ah2zpsq39wk7xtk.streamlit.app](https://weather-seasonal-particles-4i5wlj4ah2zpsq39wk7xtk.streamlit.app)


## 📖 项目简介

《天象·气象幻境》是一个 **Streamlit** 交互式应用，通过调用 Open-Meteo 实时天气 API，将城市当前气象数据（温度、湿度、风速、天气类型）转译为动态粒子系统，并自动映射为传统二十四节气意象。

**核心转译逻辑**：

| 天气类型 | 节气意象 | 视觉风格 |
| :--- | :--- | :--- |
| 晴 | 立夏流光 | 暖色粒子，缓慢浮动 |
| 雨 | 雨水如墨 | 冷色雨丝，斜向飘落 |
| 雪 | 霜降如雪 | 白色大粒子，轻盈飘落 |
| 雷暴 | 惊蛰如雷 | 闪烁粒子 + 闪电特效 |
| 雾 / 阴 | 清明如烟 | 大粒子弥散，朦胧流动 |

每个城市、每种天气，都会生成独一无二的“节气表情”。用户可以通过侧边栏切换城市，或开启历史回放，查看过去某一天的天气对应的节气意象。


## ✨ 核心功能

### 实时天气驱动
- 🌡️ **温度** → 粒子大小
- 💧 **湿度** → 粒子密度
- 💨 **风速** → 粒子运动速度与方向
- ⛅ **天气代码** → 节气意象（晴/雨/雪/雷暴/雾）

### 交互与体验
- 🖱️ **四种鼠标交互模式**：排斥 / 吸引 / 漩涡 / 爆炸
- 🌀 **点击涟漪**：点击画布产生扩散光波
- ⏳ **历史回放**：选择过去任意日期，逐日播放天气演变
- 🔍 **城市搜索**：侧边栏快速定位 40+ 城市

### 视觉风格
- 🎨 **独立配色**：每种节气拥有专属色彩体系
- 🌄 **动态背景**：渐变 + 山影叠加，层次丰富
- ⚡ **天气特效**：雷暴闪电、雨丝拖尾、雪花飘落


## 🛠️ 技术栈

| 类别 | 技术 |
| :--- | :--- |
| **框架** | Streamlit |
| **数据源** | Open-Meteo API（无需 API Key） |
| **前端渲染** | HTML5 Canvas（粒子系统） |
| **数据处理** | Python 3.9+ / Requests |
| **历史数据** | Open-Meteo Archive API |


## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/Drime-A202/weather-seasonal-particles.git
cd weather-seasonal-particles
```

### 2. 创建虚拟环境（推荐）

```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 启动应用

```bash
streamlit run app.py
```

### 5. 访问

浏览器打开 `http://localhost:8501`

## 🌐 部署说明

本项目采用 **双入口部署策略**：主应用部署在 Streamlit Cloud，同时使用 GitHub Pages 作为项目入口页。

---

### 1️⃣ Streamlit Cloud（主应用）

Streamlit Cloud 负责运行完整的 Python 后端 + 粒子画布，是项目的核心访问入口。

**部署步骤：**

1. 将项目推送到 GitHub 仓库（确保包含 `app.py` 和 `requirements.txt`）。
2. 登录 [Streamlit Cloud](https://streamlit.io/cloud)，点击 **New app**。
3. 选择仓库 `Drime-A202/weather-seasonal-particles`，分支 `main`，主文件 `app.py`。
4. 点击 **Deploy**，等待 1-2 分钟即可获得公网链接。

> ✅ **当前在线地址**：[https://weather-seasonal-particles-4i5wlj4ah2zpsq39wk7xtk.streamlit.app](https://weather-seasonal-particles-4i5wlj4ah2zpsq39wk7xtk.streamlit.app)

---

### 2️⃣ GitHub Pages（项目入口页）

GitHub Pages 托管了静态跳转页 `index.html`，访问该地址会自动重定向到 Streamlit 主应用。作用是为项目提供一个更短、更易记的入口，并承载项目展示的社交卡片（Open Graph）。

**部署步骤：**

1. 在仓库根目录创建 `index.html` 文件（包含自动跳转逻辑和项目简介）。
2. 进入仓库 **Settings → Pages**。
3. 在 **Build and deployment** 部分：
   - **Source** 选择 `Deploy from a branch`。
   - **Branch** 选择 `main`，文件夹选择 `/ (root)`。
4. 点击 **Save**，等待约 1 分钟，页面即部署完成。

> ✅ **当前入口地址**：[https://Drime-A202.github.io/weather-seasonal-particles](https://Drime-A202.github.io/weather-seasonal-particles)

---

### 3️⃣ 自定义域名（可选）

如需绑定自定义域名：

- **Streamlit Cloud**：在应用 Settings → Custom Domain 中配置，并将域名 CNAME 记录指向 Streamlit 提供的目标地址。
- **GitHub Pages**：在仓库 Settings → Pages → Custom domain 中填写域名，并在 DNS 服务商处将 CNAME 记录指向 `Drime-A202.github.io`。

---


## 🎮 使用指南

### 切换城市
- 在左侧边栏下拉菜单中选择城市
- 或使用搜索框快速定位
- 切换后粒子动画自动更新

### 交互模式
| 模式 | 效果 |
| :--- | :--- |
| **排斥** | 鼠标经过，粒子向外推开 |
| **吸引** | 粒子被鼠标吸引聚集 |
| **漩涡** | 粒子围绕鼠标旋转 |
| **爆炸** | 点击画布，粒子向外飞散 |

### 历史回放
1. 侧边栏开启“历史回放”
2. 选择过去任意日期
3. 点击“播放”，画面逐日变化
4. 速度控制可调节播放节奏


## 📊 数据与城市

- **数据来源**：Open-Meteo 实时天气 API（免费，无需 Key）
- **刷新策略**：切换城市时自动获取最新数据
- **历史数据**：Open-Meteo Archive API（支持 1940 年至今）

### 当前支持城市（40+）

| 地区 | 城市 |
| :--- | :--- |
| 直辖市 | 北京、上海、天津、重庆 |
| 东北 | 哈尔滨、长春、沈阳、大连 |
| 华北 | 呼和浩特、太原、石家庄、济南、青岛 |
| 西北 | 乌鲁木齐、拉萨、西宁、兰州、银川、敦煌 |
| 华东 | 南京、杭州、合肥、南昌、福州、台北、厦门、宁波、温州、苏州、无锡 |
| 华中 | 郑州、武汉、长沙 |
| 华南 | 广州、深圳、南宁、海口、三亚、香港、澳门、佛山、东莞、珠海、桂林 |
| 西南 | 成都、贵阳、昆明、大理、丽江 |
| 特色 | 张家界、黄山 |


## 📁 项目结构

```
weather-seasonal-particles/
├── app.py                  # Streamlit 主程序
├── requirements.txt        # Python 依赖
├── LICENSE                 # MIT 许可证
├── README.md               # 项目说明
├── .gitignore              # Git 忽略文件
├── .env.example            # 环境变量示例
├── CNAME                   # 自定义域名
├── .github/
│   └── workflows/
│       └── test.yml        # CI 测试
├── docs/                   # 文档目录
│   ├── AI_COLLABORATION.md # AI 辅助开发说明
│   ├── DEVELOPMENT_LOG.md  # 开发过程记录
│   └── FUTURE_POTENTIAL.md # 未来投稿潜力说明
└── screenshots/            # 截图目录
    ├── beijing-sunny.png
    ├── guangzhou-thunder.png
    └── haerbin-snow.png
```


## 📸 效果展示

|  晴（立夏流光） | 雷雨（惊蛰如雷） | 多云（清明如烟） |
| :---: | :---: | :---: |
| ![晴](screenshots/sunny.jpg) | ![雷雨](screenshots/thunder.jpg) | ![多云](screenshots/smog.jpg) |

> 注：请将实际截图放入 `screenshots/` 目录，并命名为对应文件名。


## 🤖 AI 辅助开发

本项目在开发过程中借助了 AI 工具进行辅助编程与调试，详见 [AI 协作说明](docs/AI_COLLABORATION.md)。


## 📝 开发过程

项目从概念到完成的全过程记录，详见 [开发日志](docs/DEVELOPMENT_LOG.md)。


## 🔮 未来展望

关于项目继续发展的可能性分析，详见 [未来投稿潜力说明](docs/FUTURE_POTENTIAL.md)。


## 📄 许可

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。


## 🙏 致谢

- [Open-Meteo](https://open-meteo.com/) 提供免费天气 API
- [Streamlit](https://streamlit.io/) 提供应用框架与云部署


⭐ 如果这个项目对你有帮助，欢迎 Star 支持！

