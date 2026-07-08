# 天象 · 气象幻境

> 基于实时天气数据驱动的节气意象可视化

## 📖 项目简介

本项目是一个 **Streamlit** 交互式应用，通过调用 Open-Meteo 实时天气 API，将城市当前气象数据（温度、湿度、风速、天气类型）转译为动态粒子系统，并映射为传统二十四节气意象：

- **晴** → 立夏流光
- **雨** → 雨水如墨
- **雪** → 霜降如雪
- **雷暴** → 惊蛰如雷
- **雾/阴** → 清明如烟

每个节气拥有独立的配色方案、粒子形态与运动特征，形成“一城一气象，一时一节气”的视觉体验。

## ✨ 核心功能

- 🌦️ **实时天气驱动**：接入 Open-Meteo API，自动获取选定城市的温度、湿度、风速、天气代码
- 🎨 **动态粒子系统**：温度影响粒子大小，湿度影响密度，风速影响运动方向与速度，天气代码决定整体视觉语法
- 🏮 **节气意象映射**：将现代气象数据转译为传统节气物候（雨水、惊蛰、清明、立夏、霜降）
- 🖱️ **简洁交互**：侧边栏切换城市，粒子动画实时响应

## 🛠️ 技术栈

- **框架**：Streamlit
- **数据源**：Open-Meteo API（无需 API Key）
- **前端**：HTML5 Canvas（粒子渲染）
- **语言**：Python 3.9+

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/Drime-A202/weather-seasonal-particles.git
cd weather-seasonal-particles
```
### 2. 安装依赖

```bash
pip install -r requirements.txt
```
### 3. 运行应用

```bash
streamlit run app.py
```
### 4. 访问应用

打开浏览器，访问 `http://localhost:8501` 即可查看应用。
- 选择城市后，应用会实时更新粒子系统，展示该城市的当前气象数据。
- 可以切换不同的城市，查看不同城市的气象数据。
- 应用会根据当前天气类型，实时切换粒子系统的颜色、大小、密度、运动方向与速度。
## 📁 项目结构
```text
weather-seasonal-particles/
├── app.py                  # Streamlit 主程序
├── requirements.txt        # 依赖列表
├── LICENSE                 # MIT 许可证
├── README.md               # 项目说明
├── .gitignore              # Git 忽略文件
└── docs/
    ├── AI_COLLABORATION.md # AI 辅助开发说明
    ├── DEVELOPMENT_LOG.md  # 开发过程记录
    └── FUTURE_POTENTIAL.md # 未来投稿潜力说明
```
## 🤖 AI 辅助开发
本项目在开发过程中借助了 AI 工具进行辅助，详见 AI 协作说明。
- **OpenAI ChatGPT**：用于生成应用的初始代码、优化代码、处理用户反馈。
- **OpenAI DALL-E**：用于生成应用的配色方案、粒子形态与运动特征。
## 📝 开发过程
项目从概念到完成的全过程记录，详见 开发日志(https://docs/DEVELOPMENT_LOG.md)。
## 🔮 未来展望
关于项目继续发展的可能性分析，详见 未来投稿潜力说明(https://docs/FUTURE_POTENTIAL.md)。
## 📄 许可
本项目采用 MIT 许可证。
[MIT License](https://github.com/Drime-A202/weather-seasonal-particles/blob/main/LICENSE)
