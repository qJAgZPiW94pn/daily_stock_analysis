<div align="center">

# 📈 股票智能分析系統

[![GitHub stars](https://img.shields.io/github/stars/ZhuLinsen/daily_stock_analysis?style=social)](https://github.com/ZhuLinsen/daily_stock_analysis/stargazers)
[![CI](https://github.com/ZhuLinsen/daily_stock_analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/ZhuLinsen/daily_stock_analysis/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Ready-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/r/zhulinsen/daily_stock_analysis)

<p align="center">
  <a href="https://trendshift.io/repositories/18527" target="_blank"><img src="https://trendshift.io/api/badge/repositories/18527" alt="ZhuLinsen%2Fdaily_stock_analysis | Trendshift" width="230" /></a>&nbsp;<a href="https://hellogithub.com/repository/ZhuLinsen/daily_stock_analysis" target="_blank"><img src="https://api.hellogithub.com/v1/widgets/recommend.svg?rid=6daa16e405ce46ed97b4a57706aeb29f&claim_uid=pfiJMqhR9uvDGlT&theme=neutral" alt="Featured｜HelloGitHub" width="230" /></a>
</p>

> 🤖 基于 AI 大模型的 A股/港股/美股自选股智能分析系統，每日自动分析并推送「决策仪表盘」到企业微信/飞书/Telegram/Discord/Slack/邮箱

[**产品预览**](#-产品预览) · [**功能特性**](#-功能特性) · [**快速开始**](#-快速开始) · [**推送效果**](#-推送效果) · [**文档中心**](docs/INDEX.md) · [**完整指南**](docs/full-guide.md)

简体中文 | [English](docs/README_EN.md) | [繁體中文](docs/README_CHT.md)

</div>

## 💖 赞助商 (Sponsors)
<div align="center">
  <p align="center">
    <a href="https://open.anspire.cn/?share_code=QFBC0FYC" target="_blank"><img src="./docs/assets/anspire.png" alt="Anspire Open 一站式模型和搜尋服務" width="300" height="141" style="width: 300px; height: 141px; object-fit: contain;"></a>
    <a href="https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis" target="_blank"><img src="./docs/assets/serpapi_banner_zh.png" alt="轻松抓取搜尋引擎上的实时金融新闻數據 - SerpApi" width="300" height="141" style="width: 300px; height: 141px; object-fit: contain;"></a>
  </p>
</div>


## 🖥️ 产品预览

<p align="center">
  <img src="docs/assets/readme_workspace_tour_20260510.gif" alt="DSA Web 工作台演示" width="720">
</p>

## ✨ 功能特性

| 能力 | 覆盖内容 |
|------|------|
| AI 决策报告 | 核心结论、評分、趨勢、买卖点位、風險警报、催化因素、操作檢查清单 |
| 多市场數據聚合 | A股、港股、美股、ETF；行情、K 线、技术指標、資金流、筹码、新闻、公告和基本面 |
| Web / 桌面工作台 | 手动分析、工作进度、历史报告、完整 Markdown、回测、持倉、配置管理、浅色 / 深色主题 |
| Agent 策略问股 | 多轮追问，支援均线、缠论、波浪、趨勢、热点、事件、成长、预期等 15 种内置策略，覆盖 Web/Bot/API |
| 智能匯入与补全 | 图片、CSV/Excel、剪贴板匯入；股票代碼/名称/拼音/别名补全 |
| 自動化与推送 | GitHub Actions、Docker、本機定时工作、FastAPI 服務和企业微信/飞书/Telegram/Discord/Slack/電郵推送 |

> 功能细节、欄位契约、基本面 P0 逾時语义、交易纪律、數據源優先级、Web/API 行为请看 [完整配置与部署指南](docs/full-guide.md)。

### 技术栈与數據来源

| 类型 | 支援 |
|------|------|
| AI 模型 | [Anspire](https://open.anspire.cn/?share_code=QFBC0FYC)、[AIHubMix](https://aihubmix.com/?aff=CfMq)、Gemini、OpenAI 相容、DeepSeek、通义千问、Claude、Ollama 本機模型等 |
| 行情數據 | [TickFlow](https://tickflow.org/auth/register?ref=WDSGSPS5XC)、AkShare、Tushare、Pytdx、Baostock、YFinance、Longbridge |
| 新闻搜尋 | [Anspire](https://open.anspire.cn/?share_code=QFBC0FYC)、[SerpAPI](https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis)、[Tavily](https://tavily.com/)、[Bocha](https://open.bocha.cn/)、[Brave](https://brave.com/search/api/)、[MiniMax](https://platform.minimaxi.com/)、SearXNG |
| 社交舆情 | [Stock Sentiment API](https://api.adanos.org/docs)（Reddit / X / Polymarket，仅美股，可選） |

> 完整規則见 [數據源配置](docs/full-guide.md#數據源配置)。

## 🚀 快速开始

### 方式一：GitHub Actions（推荐）

> 5 分钟完成部署，零成本，無需服務器。


#### 1. Fork 本倉庫

点击右上角 `Fork` 按钮（顺便点个 Star⭐ 支援一下）

#### 2. 配置 Secrets

`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

**AI 模型配置（至少配置一个）**

預設先选一个模型服務商并填写 API Key；需要多模型、图片识别、本機模型或進階路由时，再參考 [LLM 配置指南](docs/LLM_CONFIG_GUIDE.md)。

| Secret 名称 | 说明 | 必填 |
|------------|------|:----:|
| `ANSPIRE_API_KEYS` | [Anspire](https://open.anspire.cn/?share_code=QFBC0FYC) API Key，一Key同时启用全球热门大模型和联网搜尋，無需科学上网，含免费額度 | **推荐** |
| `AIHUBMIX_KEY` | [AIHubMix](https://aihubmix.com/?aff=CfMq) API Key，一Key切換使用全系模型，無需科学上网，本项目可享 10% 优惠 | **推荐** |
| `GEMINI_API_KEY` | Google Gemini API Key | 可選 |
| `ANTHROPIC_API_KEY` | Anthropic Claude API Key | 可選 |
| `OPENAI_API_KEY` | OpenAI 相容 API Key（支援 DeepSeek、通义千问等） | 可選 |
| `OPENAI_BASE_URL` / `OPENAI_MODEL` | 使用 OpenAI 相容服務时填写 | 可選 |

> Ollama 更适合本機 / Docker 部署，GitHub Actions 推荐使用云端 API。

**通知渠道配置（至少配置一个）**

| Secret 名称 | 说明 |
|------------|------|
| `WECHAT_WEBHOOK_URL` | 企业微信机器人 |
| `FEISHU_WEBHOOK_URL` | 飞书机器人 |
| `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` | Telegram |
| `DISCORD_WEBHOOK_URL` | Discord Webhook |
| `SLACK_BOT_TOKEN` + `SLACK_CHANNEL_ID` | Slack Bot |
| `EMAIL_SENDER` + `EMAIL_PASSWORD` | 電郵推送 |

更多渠道、簽名校验、分組電郵、Markdown 转图片等配置见 [通知渠道詳細配置](docs/full-guide.md#通知渠道詳細配置)。

**自选股配置（必填）**

| Secret 名称 | 说明 | 必填 |
|------------|------|:----:|
| `STOCK_LIST` | 自选股代碼，如 `600519,hk00700,AAPL,TSLA` | ✅ |

**新闻源配置（推荐）**

新闻源会显著影响舆情、公告、事件和催化因素质量，建议至少配置一个搜尋服務。

| Secret 名称 | 说明 | 必填 |
|------------|------|:----:|
| `ANSPIRE_API_KEYS` | [Anspire AI Search](https://aisearch.anspire.cn/)：中文内容特别最佳化，适合 A 股新闻和舆情检索；同一 Key 可复用为 Anspire 大模型 | **推荐** |
| `SERPAPI_API_KEYS` | [SerpAPI](https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis)：搜尋引擎结果补强，适合实时金融新闻 | **推荐** |
| `TAVILY_API_KEYS` | [Tavily](https://tavily.com/)：通用新闻搜尋 API | 可選 |
| `BOCHA_API_KEYS` | [博查搜尋](https://open.bocha.cn/)：中文搜尋最佳化，支援 AI 摘要 | 可選 |
| `BRAVE_API_KEYS` | [Brave Search](https://brave.com/search/api/)：隐私優先，美股资讯补强 | 可選 |
| `MINIMAX_API_KEYS` | [MiniMax](https://platform.minimaxi.com/)：结构化搜尋结果 | 可選 |
| `SEARXNG_BASE_URLS` | SearXNG 自建实例：无配額兜底，适合私有部署 | 可選 |

更多搜尋源、社交舆情和降級規則见 [搜尋服務配置](docs/full-guide.md#搜尋服務配置)。

#### 3. 启用 Actions

`Actions` 標籤 → `I understand my workflows, go ahead and enable them`

#### 4. 手动測試

`Actions` → `每日股票分析` → `Run workflow` → `Run workflow`

#### 完成

預設每个**工作日 18:00（北京时间）**自动執行，也可手动触发。預設非交易日（含 A/H/US 節假日）不執行；強制執行、交易日檢查、断点续传等規則见 [完整指南](docs/full-guide.md#定时工作配置)。

### 方式二：本機執行 / Docker 部署

```bash
# 克隆项目
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git && cd daily_stock_analysis

# 安裝依賴
pip install -r requirements.txt

# 配置環境變數
cp .env.example .env && vim .env

# 執行分析
python main.py
```

常用命令：

```bash
python main.py --debug
python main.py --dry-run
python main.py --stocks 600519,hk00700,AAPL
python main.py --market-review
python main.py --schedule
python main.py --serve-only
```

> Docker 部署、定时工作、云服務器訪問請參考 [完整指南](docs/full-guide.md)；桌面客户端打包請參考 [桌面端打包说明](docs/desktop-package.md)。

## 📱 推送效果

### 决策仪表盘
```
🎯 2026-02-08 决策仪表盘
共分析3只股票 | 🟢買入:0 🟡观望:2 🔴賣出:1

📊 分析结果摘要
⚪ 中钨高新(000657): 观望 | 評分 65 | 看多
⚪ 永鼎股份(600105): 观望 | 評分 48 | 震荡
🟡 新莱应材(300260): 賣出 | 評分 35 | 看空

⚪ 中钨高新 (000657)
📰 重要資訊速览
💭 舆情情绪: 市场关注其AI属性与业绩高增长，情绪偏积极，但需消化短期获利盘和主力流出压力。
📊 业绩预期: 基于舆情資訊，公司2025年前三季度业绩同比大幅增长，基本面强劲，为股價提供支撑。

🚨 風險警报:

風險点1：2月5日主力資金大幅净賣出3.63亿元，需警惕短期抛压。
風險点2：筹码集中度高达35.15%，表明筹码分散，拉升阻力可能较大。
風險点3：舆情中提及公司历史违规记录及重组相關風險提示，需保持关注。
✨ 利好催化:

利好1：公司被市场定位为AI服務器HDI核心供应商，受益于AI产业发展。
利好2：2025年前三季度扣非净利潤同比暴涨407.52%，业绩表现强劲。
📢 最新动态: 【最新訊息】舆情顯示公司是AI PCB微钻领域龙头，深度綁定全球头部PCB/载板厂。2月5日主力資金净賣出3.63亿元，需关注后续資金流向。

---
生成时间: 18:00
```

### 大盤复盘
```
🎯 2026-01-10 大盤复盘

📊 主要指數
- 上证指數: 3250.12 (🟢+0.85%)
- 深证成指: 10521.36 (🟢+1.02%)
- 创业板指: 2156.78 (🟢+1.35%)

📈 市场概况
上涨: 3920 | 下跌: 1349 | 漲停: 155 | 跌停: 3

🔥 板塊表现
领涨: 互联网服務、文化传媒、小金属
领跌: 保险、航空机场、光伏设备
```

## ⚙️ 配置说明

完整環境變數、模型渠道、通知渠道、數據源優先级、交易纪律、基本面 P0 语义和部署说明請參考 [完整配置指南](docs/full-guide.md)。

## 🖥️ Web 界面

Web 工作台提供配置管理、工作監控、手动分析、历史报告、完整 Markdown 报告、Agent 问股、回测、持倉管理、智能匯入和浅色 / 深色主题。啟動方式：

```bash
python main.py --webui
python main.py --webui-only
```

訪問 `http://127.0.0.1:8000` 即可使用。認證、智能匯入、搜尋补全、历史报告复制、云服務器訪問等细节见 [本機 WebUI 管理界面](docs/full-guide.md#本機-webui-管理界面)。

## 🤖 Agent 策略问股

配置任意可用 AI API Key 后，Web `/chat` 页面即可使用策略问股；如需显式關閉可设置 `AGENT_MODE=false`。

- 支援均线金叉、缠论、波浪理論、多头趨勢、热点题材、事件驱动、成长质量、预期重估等内置策略
- 支援实时行情、K 线、技术指標、新闻和風險資訊呼叫
- 支援多轮追问、會話匯出、发送到通知渠道和后台執行
- 支援自定义策略文件与多 Agent 编排（实验性）

> Agent 具体參數、`skill` 命名相容、多 Agent 模式和预算护栏见 [完整指南](docs/full-guide.md#本機-webui-管理界面) 与 [LLM 配置指南](docs/LLM_CONFIG_GUIDE.md)。

## 🧩 相關项目 (Related Projects)

> DSA 聚焦日常分析报告；下面两个同系列项目分别覆盖选股、策略驗證与策略进化，适合按需延伸使用。它们当前独立维护，后续会優先探索与 DSA 的候选股匯入、回测驗證和报告联动。

| 项目 | 定位 |
|------|------|
| [AlphaSift](https://github.com/ZhuLinsen/alphasift) | 多因子选股与全市场扫描，用于从股票池中提取候选标的 |
| [AlphaEvo](https://github.com/ZhuLinsen/alphaevo) | 策略回测与自我进化，用于驗證策略規則，并通过反覆探索策略參數与组合 |

## 📬 联系与合作

<table>
  <tr>
    <td width="92" valign="top"><strong>合作邮箱</strong></td>
    <td valign="top">
      <a href="mailto:zhuls345@gmail.com">zhuls345@gmail.com</a><br>
      项目咨询、部署支援与功能扩展
    </td>
    <td align="center" rowspan="3" valign="middle" width="148">
      <a href="http://xhslink.com/m/tU520DWCKT" target="_blank"><img src="./docs/assets/xiaohongshu_tick.jpg" width="112" alt="小红书二维码"></a><br>
      <sub>扫码关注小红书</sub>
    </td>
  </tr>
  <tr>
    <td width="92" valign="top"><strong>小红书</strong></td>
    <td valign="top"><a href="http://xhslink.com/m/tU520DWCKT">欢迎关注小红书</a></td>
  </tr>
  <tr>
    <td width="92" valign="top"><strong>議題反馈</strong></td>
    <td valign="top"><a href="https://github.com/ZhuLinsen/daily_stock_analysis/issues">提交 Issue</a></td>
  </tr>
</table>

## 📄 License

[MIT License](LICENSE) © 2026 ZhuLinsen

欢迎在二次开发或引用时注明本倉庫来源，感谢支援项目持续维护。

## ⚠️ 免责声明

本项目仅供學習和研究使用，不构成任何投资建议。股市有風險，投资需谨慎。作者不对使用本项目产生的任何损失负责。

---
