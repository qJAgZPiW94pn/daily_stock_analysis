# 📖 完整配置与部署指南

本文档包含 A股智能分析系統的完整配置说明，适合需要進階功能或特殊部署方式的使用者。

> 💡 快速上手請參考 [README.md](../README.md)，本文档为进阶配置。

## 📁 项目结构

```
daily_stock_analysis/
├── main.py              # 主程式入口
├── src/                 # 核心业务邏輯
│   ├── analyzer.py      # AI 分析器
│   ├── config.py        # 配置管理
│   ├── notification.py  # 訊息推送
│   └── ...
├── data_provider/       # 多數據源適配器
├── bot/                 # 机器人交互模組
├── api/                 # FastAPI 后端服務
├── apps/dsa-web/        # React 前端
├── docker/              # Docker 配置
├── docs/                # 项目文档
└── .github/workflows/   # GitHub Actions
```

## 📑 目錄

- [项目结构](#项目结构)
- [GitHub Actions 詳細配置](#github-actions-詳細配置)
- [環境變數完整列表](#環境變數完整列表)
- [Docker 部署](#docker-部署)
- [本機執行詳細配置](#本機執行詳細配置)
- [定时工作配置](#定时工作配置)
- [通知渠道詳細配置](#通知渠道詳細配置)
- [數據源配置](#數據源配置)
- [進階功能](#進階功能)
- [回测功能](#回测功能)
- [本機 WebUI 管理界面](#本機-webui-管理界面)

---

## GitHub Actions 詳細配置

### 1. Fork 本倉庫

点击右上角 `Fork` 按钮

### 2. 配置 Secrets

进入你 Fork 的倉庫 → `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

<div align="center">
  <img src="assets/secret_config.png" alt="GitHub Secrets 配置示意图" width="600">
</div>

#### AI 模型配置（至少配置一个）

| Secret 名称 | 说明 | 必填 |
|------------|------|:----:|
| `ANSPIRE_API_KEYS` | [Anspire](https://open.anspire.cn/?share_code=QFBC0FYC) API Key，一 Key 同时启用大模型和中文最佳化联网搜尋，含本项目免费額度 | 推荐 |
| `AIHUBMIX_KEY` | [AIHubMix](https://aihubmix.com/?aff=CfMq) API Key，一 Key 切換使用全系模型，本项目可享 10% 优惠 | 推荐 |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/) 獲取免费 Key | 可選 |
| `ANTHROPIC_API_KEY` | Anthropic Claude API Key | 可選 |
| `OPENAI_API_KEY` | OpenAI 相容 API Key（支援 DeepSeek、通义千问等） | 可選 |
| `OPENAI_BASE_URL` | OpenAI 相容 API 地址（如 `https://api.deepseek.com`） | 可選 |
| `OPENAI_MODEL` | 模型名称（如 `gemini-3.1-pro-preview`、`deepseek-v4-flash`、`gpt-5.5`） | 可選 |

> *注：以上模型 Key / 渠道至少配置一个；推荐優先从 Anspire 或 AIHubMix 这类一 Key 多模型服務开始。

#### 通知渠道配置（可同时配置多个，全部推送）

> 通知渠道、minimal/advanced key 分層、Actions 映射、`--check-notify` 診斷、Web 一键測試和本機 / Docker / GitHub Actions / Desktop 場景说明详见 [通知专题文档](notifications.md)。

| Secret 名称 | 说明 | 必填 |
|------------|------|:----:|
| `WECHAT_WEBHOOK_URL` | 企业微信 Webhook URL | 可選 |
| `FEISHU_WEBHOOK_URL` | 飞书 Webhook URL | 可選 |
| `FEISHU_WEBHOOK_SECRET` | 飞书 Webhook 簽名密钥（开启“簽名校验”时必填） | 可選 |
| `FEISHU_WEBHOOK_KEYWORD` | 飞书 Webhook 關鍵词（开启“關鍵词”时必填） | 可選 |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token（@BotFather 獲取） | 可選 |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | 可選 |
| `TELEGRAM_MESSAGE_THREAD_ID` | Telegram Topic ID (用于发送到子话题) | 可選 |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL（[建立方法](https://support.discord.com/hc/en-us/articles/228383668)） | 可選 |
| `DISCORD_BOT_TOKEN` | Discord Bot Token（与 Webhook 二选一） | 可選 |
| `DISCORD_MAIN_CHANNEL_ID` | Discord Channel ID（使用 Bot 时需要） | 可選 |
| `DISCORD_INTERACTIONS_PUBLIC_KEY` | Discord Public Key（仅入站 Interaction/Webhook 回调验签时需要） | 可選 |
| `SLACK_BOT_TOKEN` | Slack Bot Token（推荐，支援图片上傳；同时配置时優先于 Webhook） | 可選 |
| `SLACK_CHANNEL_ID` | Slack Channel ID（使用 Bot 时需要） | 可選 |
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL（仅文本，不支援图片） | 可選 |
| `EMAIL_SENDER` | 发件人邮箱（如 `xxx@qq.com`） | 可選 |
| `EMAIL_PASSWORD` | 邮箱授權码（非登录密碼） | 可選 |
| `EMAIL_RECEIVERS` | 收件人邮箱（多个用逗号分隔，留空则发给自己） | 可選 |
| `EMAIL_SENDER_NAME` | 发件人顯示名称（預設：daily_stock_analysis股票分析助手） | 可選 |
| `PUSHPLUS_TOKEN` | PushPlus Token（[獲取地址](https://www.pushplus.plus)，国内推送服務） | 可選 |
| `SERVERCHAN3_SENDKEY` | Server酱³ Sendkey（[獲取地址](https://sc3.ft07.com/)，手机APP推送服務） | 可選 |
| `ASTRBOT_URL` | AstrBot Webhook URL | 可選 |
| `ASTRBOT_TOKEN` | AstrBot Bearer Token（可選） | 可選 |
| `NTFY_URL` | ntfy 完整 topic endpoint，必须包含 topic path，例如 `https://ntfy.sh/my-topic` | 可選 |
| `NTFY_TOKEN` | ntfy Bearer Token（可選） | 可選 |
| `GOTIFY_URL` | Gotify server base URL，不包含 `/message`；系統会自动拼接 `/message` | 可選 |
| `GOTIFY_TOKEN` | Gotify application token，通过 `X-Gotify-Key` Header 发送 | 可選 |
| `CUSTOM_WEBHOOK_URLS` | 自定义 Webhook（支援钉钉等，多个用逗号分隔） | 可選 |
| `CUSTOM_WEBHOOK_BEARER_TOKEN` | 自定义 Webhook 的 Bearer Token（用于需要認證的 Webhook） | 可選 |
| `CUSTOM_WEBHOOK_BODY_TEMPLATE` | 自定义 Webhook JSON body 模板，適配 AstrBot、NapCat、自建服務等特殊 payload | 可選 |
| `WEBHOOK_VERIFY_SSL` | 讀取该配置的 webhook-style HTTPS 通知請求证书校验（預設 true）。设为 false 可支援自簽名证书。警告：關閉有严重安全風險（MITM），仅限可信内网 | 可選 |

> *注：至少配置一个渠道，配置多个则同时推送
>
> 当前預設 `daily_analysis.yml` 只显式映射固定 Secret / Variable 名称，不会自动把 `STOCK_GROUP_1`、`EMAIL_GROUP_1` 这类任意编号變數匯入執行環境。所以分組邮箱功能目前不适用于倉庫自带預設 GitHub Actions workflow；它适用于本機 `.env`、Docker，或你自行显式扩展过 `env:` 映射的執行環境。Actions 已显式映射 `CUSTOM_WEBHOOK_BODY_TEMPLATE`、`WEBHOOK_VERIFY_SSL`、`FEISHU_WEBHOOK_SECRET`、`FEISHU_WEBHOOK_KEYWORD`、`PUSHPLUS_TOPIC`、`NTFY_URL`、`NTFY_TOKEN`、`GOTIFY_URL`、`GOTIFY_TOKEN`、P3 通知路由键以及 P4 通知降噪键；`MARKDOWN_TO_IMAGE_CHANNELS` 和 `MERGE_EMAIL_NOTIFICATION` 仍作为行为开关不在預設 workflow 中自动映射。

#### 推送行为配置

| Secret 名称 | 说明 | 必填 |
|------------|------|:----:|
| `SINGLE_STOCK_NOTIFY` | 单股推送模式：设为 `true` 则每分析完一只股票立即推送 | 可選 |
| `REPORT_TYPE` | 报告类型：`simple`(精简)、`full`(完整)、`brief`(3-5句概括)，Docker環境推荐设为 `full` | 可選 |
| `REPORT_LANGUAGE` | 报告輸出语言：`zh`(預設中文) / `en`(英文)；会同步影响 Prompt、模板、通知 fallback 与 Web 报告页固定文案。倉庫自带 `daily_analysis.yml` 已显式映射该變數，直接在 Actions Secrets/Variables 中配置即可生效 | 可選 |
| `REPORT_SUMMARY_ONLY` | 仅分析结果摘要：设为 `true` 时只推送汇总，不含個股详情；多股时适合快速浏览（預設 false，Issue #262） | 可選 |
| `REPORT_SHOW_LLM_MODEL` | 通知报告底部是否顯示本次分析使用的 LLM 模型名称，預設 `true`；设为 `false` 可隱藏執行时模型資訊。该變數仅調整展示，不影响 provider/model/Base URL、LiteLLM 路由或執行时模型保存/迁移/清理语义。 | 可選 |
| `REPORT_TEMPLATES_DIR` | Jinja2 模板目錄（相對项目根，預設 `templates`） | 可選 |
| `REPORT_RENDERER_ENABLED` | 启用 Jinja2 模板渲染（預設 `false`，保证零迴歸） | 可選 |
| `REPORT_INTEGRITY_ENABLED` | 启用报告完整性校验，缺失必填欄位时重試或占位补全（預設 `true`） | 可選 |
| `REPORT_INTEGRITY_RETRY` | 完整性校验重試次数（預設 `1`，`0` 表示仅占位不重試） | 可選 |
| `REPORT_HISTORY_COMPARE_N` | 历史信号对比条数，`0` 關閉（預設），`>0` 启用 | 可選 |
| `ANALYSIS_DELAY` | 個股分析和大盤分析之间的延遲（秒），避免API限流，如 `10` | 可選 |
| `MERGE_EMAIL_NOTIFICATION` | 個股与大盤复盘合併推送（預設 false），减少電郵数量、降低垃圾電郵風險；与 `SINGLE_STOCK_NOTIFY` 互斥（单股模式下合併不生效） | 可選 |
| `MARKDOWN_TO_IMAGE_CHANNELS` | 将 Markdown 转为图片发送的渠道（用逗号分隔）：telegram,wechat,custom,email,slack；单股推送需同时配置且安裝转图工具 | 可選 |
| `NOTIFICATION_REPORT_CHANNELS` | report 路由渠道（单股推送、聚合日报、大盤复盘、合併推送等）；留空表示所有已配置渠道 | 可選 |
| `NOTIFICATION_ALERT_CHANNELS` | alert 路由渠道（EventMonitor 警報）；留空表示所有已配置渠道 | 可選 |
| `NOTIFICATION_SYSTEM_ERROR_CHANNELS` | system_error 预留路由渠道；当前不新增自动系統錯誤生产者，留空表示所有已配置渠道 | 可選 |
| `NOTIFICATION_DEDUP_TTL_SECONDS` | 通知去重 TTL 秒数，`0` 關閉；同一稳定去重 key 在 TTL 内只发送一次 | 可選 |
| `NOTIFICATION_COOLDOWN_SECONDS` | 通知冷却秒数，`0` 關閉；同一冷却 key 在窗口内限频 | 可選 |
| `NOTIFICATION_QUIET_HOURS` | 通知静默时段，格式 `HH:MM-HH:MM`，支援跨午夜；留空關閉 | 可選 |
| `NOTIFICATION_TIMEZONE` | 静默时段使用的 IANA 时区，如 `Asia/Shanghai`；留空跟随 `TZ` 或系統本機时区 | 可選 |
| `NOTIFICATION_MIN_SEVERITY` | 最低通知級別：`info`、`warning`、`error`、`critical`；留空保持现状 | 可選 |
| `NOTIFICATION_DAILY_DIGEST_ENABLED` | 每日摘要预留开关；当前不会发送摘要或持久化摘要内容 | 可選 |
| `MARKDOWN_TO_IMAGE_MAX_CHARS` | 超过此长度不转图片，避免超大图片（預設 15000） | 可選 |
| `MD2IMG_ENGINE` | 转图引擎：`wkhtmltoimage`（預設，需 wkhtmltopdf）或 `markdown-to-file`（emoji 更好，需 `npm i -g markdown-to-file`） | 可選 |
| `PREFETCH_REALTIME_QUOTES` | 设为 `false` 可禁用实时行情预取，避免 efinance/akshare_em 全市场拉取（預設 true） | 可選 |

> 相容性说明：`REPORT_SHOW_LLM_MODEL` 维持預設 `true` 的原始展示语义，關閉时只影响底部模型文案輸出。该配置不会变更 provider/model/Base URL、LiteLLM 路由、模型保存、迁移或清理语义；回退方式为恢復或刪除该變數，并设为 `true`。

#### 其他配置

| Secret 名称 | 说明 | 必填 |
|------------|------|:----:|
| `STOCK_LIST` | 自选股代碼，如 `600519,300750,002594` | ✅ |
| `ANSPIRE_API_KEYS` | [Anspire AI Search](https://aisearch.anspire.cn/) 针对中文内容特别最佳化；同一 Key 可用于搜尋与 Anspire 大模型网关的兜底示例（是否可用以控制台与账号權限为准） | 推荐 |
| `SERPAPI_API_KEYS` | [SerpAPI](https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis) 搜尋引擎结果补强，适合实时金融新闻 | 推荐 |
| `TAVILY_API_KEYS` | [Tavily](https://tavily.com/) 搜尋 API（新闻搜尋） | 可選 |
| `BOCHA_API_KEYS` | [博查搜尋](https://open.bocha.cn/) Web Search API（中文搜尋最佳化，支援AI摘要，多个key用逗号分隔） | 可選 |
| `BRAVE_API_KEYS` | [Brave Search](https://brave.com/search/api/) API（隐私優先，美股最佳化，多个key用逗号分隔） | 可選 |
| `MINIMAX_API_KEYS` | [MiniMax](https://platform.minimax.io/) Coding Plan Web Search（结构化搜尋结果） | 可選 |
| `SEARXNG_BASE_URLS` | SearXNG 自建实例（无配額兜底，需在 settings.yml 启用 format: json）；留空时預設自动发现公共实例 | 可選 |
| `SEARXNG_PUBLIC_INSTANCES_ENABLED` | 是否在 `SEARXNG_BASE_URLS` 为空时自动从 `searx.space` 獲取公共实例（預設 `true`） | 可選 |
| `TUSHARE_TOKEN` | [Tushare Pro](https://tushare.pro/weborder/#/login?reg=834638 ) Token | 可選 |
| `LONGBRIDGE_APP_KEY` | [Longbridge OpenAPI](https://open.longbridge.com/) App Key（美股/港股量比、换手率、PE 兜底） | 可選 |
| `LONGBRIDGE_APP_SECRET` | Longbridge App Secret | 可選 |
| `LONGBRIDGE_ACCESS_TOKEN` | Longbridge Access Token | 可選 |
| `LONGBRIDGE_STATIC_INFO_TTL_SECONDS` | 长桥 `static_info` 程式内快取秒数（預設 86400，0=不快取） | 可選 |
| `LONGBRIDGE_CONNECTION_COOLDOWN_SECONDS` | 长桥連線關閉类例外后的冷却秒数（預設 15；冷却期内暫時略過 Longbridge，避免頻繁重连） | 可選 |
| `LONGBRIDGE_HTTP_URL` | HTTP 介面地址（預設 `https://openapi.longbridge.com`） | 可選 |
| `LONGBRIDGE_QUOTE_WS_URL` | 行情 WebSocket 地址（預設 `wss://openapi-quote.longbridge.com/v2`） | 可選 |
| `LONGBRIDGE_TRADE_WS_URL` | 交易 WebSocket 地址（預設 `wss://openapi-trade.longbridge.com/v2`） | 可選 |
| `LONGBRIDGE_REGION` | 覆盖接入点；SDK 会按網路自动选择，預設 `hk`，若判斷不正确可设置（如 `cn`、`hk`） | 可選 |
| `LONGBRIDGE_ENABLE_OVERNIGHT` | 是否开启夜盘行情 `true` / `false`，預設 `false` | 可選 |
| `LONGBRIDGE_PUSH_CANDLESTICK_MODE` | K 线推送模式：`realtime` 或 `confirmed`（預設 `realtime`） | 可選 |
| `LONGBRIDGE_PRINT_QUOTE_PACKAGES` | 連線时是否打印行情包（未设置时預設 `false`；设为 `1`/`true`/`yes` 开启） | 可選 |
| `ENABLE_CHIP_DISTRIBUTION` | 启用筹码分布（Actions 預設 false；需筹码數據时在 Variables 中设为 true，介面可能不稳定） | 可選 |

> **GitHub Actions：** 倉庫自带 `daily_analysis.yml` 已把上表中的 `LONGBRIDGE_*` 映射到工作環境。若未在 **Settings → Secrets and variables → Actions** 中配置 `LONGBRIDGE_APP_KEY`、`LONGBRIDGE_APP_SECRET`、`LONGBRIDGE_ACCESS_TOKEN`，CI 内不会呼叫长桥（日誌中一般看不到 `[Longbridge]` 相關行情行）。可選接入点變數（如 `LONGBRIDGE_REGION`）可放在 **Variables** 或 **Secrets**。

> **Longbridge 執行时行为：** 未配置凭据时不会实例化 Longbridge 这个可選 fetcher；若執行时遇到 `client is closed`、`context closed`、`connection closed` 等連線關閉类例外，会进入冷却期（預設 15 秒，可用 `LONGBRIDGE_CONNECTION_COOLDOWN_SECONDS` 調整），冷却期内美股/港股的实时与日线請求会自动略過 Longbridge，退回 YFinance / AkShare 等兜底鏈路。

> 补充说明
- TUSHARE_TOKEN，当此參數配置后，但不具备港股日线介面權限时，也会出现港股數據查詢不出来或者錯誤的情况，和老版本提示不支援港股效果相同

#### ✅ 最小配置示例

如果你想快速开始，最少需要配置以下项：

1. **AI 模型**：`ANSPIRE_API_KEYS`（一 Key 同时启用大模型和搜尋）、`AIHUBMIX_KEY`（[AIHubmix](https://aihubmix.com/?aff=CfMq)，一 Key 多模型）、`GEMINI_API_KEY` 或 `OPENAI_API_KEY`
2. **通知渠道**：至少配置一个，如 `WECHAT_WEBHOOK_URL` 或 `EMAIL_SENDER` + `EMAIL_PASSWORD`
3. **股票列表**：`STOCK_LIST`（必填）
4. **搜尋 API**：`ANSPIRE_API_KEYS` 或 `SERPAPI_API_KEYS`（推荐，用于新闻与舆情搜尋）

> 💡 配置完以上 4 项即可开始使用！

### 3. 启用 Actions

1. 进入你 Fork 的倉庫
2. 点击顶部的 `Actions` 標籤
3. 如果看到提示，点击 `I understand my workflows, go ahead and enable them`

### 4. 手动測試

1. 进入 `Actions` 標籤
2. 左侧选择 `每日股票分析` workflow
3. 点击右侧的 `Run workflow` 按钮
4. 选择執行模式
5. 点击绿色的 `Run workflow` 确认

### 5. 完成！

預設每个工作日 **18:00（北京时间）** 自动執行。

---

## 環境變數完整列表

### AI 模型配置

> 完整说明见 [LLM 配置指南](LLM_CONFIG_GUIDE.md)（三层配置、渠道模式、Vision、Agent、排错）；常用服務商预设、Actions 變數对照和錯誤排障见 [LLM 服務商配置指南](llm-providers.md)。
> 相容性说明（Issue #1306）：本次改动只复用已有历史写入鏈路展示大盤复盘结果，不修改模型名、provider、Base URL、`LiteLLM` 清理/相容语义。回退路徑为回滚本版本。相容驗證来源见 `requirements.txt`（`litellm` 版本約束）、`docs/LLM_CONFIG_GUIDE*.md`，以及迴歸用例 `tests/test_analysis_api_contract.py`、`tests/test_analysis_history.py`、`tests/test_market_review.py`；官方源參考：[LiteLLM OpenAI-compatible](https://docs.litellm.ai/docs/providers/openai_compatible)、[OpenAI Chat Completion API](https://platform.openai.com/docs/api-reference/chat)。
> 本节仅同步模型/渠道配置清单，不额外引入新的外部 provider / Base URL 相容约定；相容语义以当前倉庫 `requirements.txt` 依賴約束和相關測試为准，历史回退路徑见上述两份文档中“回退/恢復”说明。

| 變數名 | 说明 | 預設值 | 必填 |
|--------|------|--------|:----:|
| `LITELLM_MODEL` | 主模型，格式 `provider/model`（如 `gemini/gemini-3.1-pro-preview`），推荐優先使用 | - | 否 |
| `AGENT_LITELLM_MODEL` | Agent 主模型（可選）；留空继承主模型，无 provider 前綴按 `openai/<model>` 解析 | - | 否 |
| `LITELLM_FALLBACK_MODELS` | 備選模型，逗号分隔 | - | 否 |
| `LLM_CHANNELS` | 渠道名称列表（逗号分隔），配合 `LLM_{NAME}_*` 使用，详见 [LLM 配置指南](LLM_CONFIG_GUIDE.md) | - | 否 |
| `LITELLM_CONFIG` | 進階模型路由 YAML 配置文件路徑（進階） | - | 否 |
| `ANSPIRE_API_KEYS` | [Anspire](https://open.anspire.cn/?share_code=QFBC0FYC) API Key，一 Key 同时启用大模型网关和搜尋 | - | 可選 |
| `AIHUBMIX_KEY` | [AIHubmix](https://aihubmix.com/?aff=CfMq) API Key，一 Key 切換使用全系模型，無需额外配置 Base URL | - | 可選 |
| `GEMINI_API_KEY` | Google Gemini API Key | - | 可選 |
| `GEMINI_MODEL` | 主模型名称（legacy，`LITELLM_MODEL` 優先） | `gemini-3.1-pro-preview` | 否 |
| `GEMINI_MODEL_FALLBACK` | 備選模型（legacy） | `gemini-3-flash-preview` | 否 |
| `OPENAI_API_KEY` | OpenAI 相容 API Key | - | 可選 |
| `OPENAI_BASE_URL` | OpenAI 相容 API 地址 | - | 可選 |
| `OLLAMA_API_BASE` | Ollama 本機服務地址（如 `http://localhost:11434`），详见 [LLM 配置指南](LLM_CONFIG_GUIDE.md) | - | 可選 |
| `OPENAI_MODEL` | OpenAI 模型名称（legacy，AIHubmix 使用者可填如 `gemini-3.1-pro-preview`、`gpt-5.5`） | `gpt-5.5` | 可選 |
| `ANTHROPIC_API_KEY` | Anthropic Claude API Key | - | 可選 |
| `ANTHROPIC_MODEL` | Claude 模型名称 | `claude-sonnet-4-6` | 可選 |
| `ANTHROPIC_TEMPERATURE` | Claude 温度參數（0.0-1.0） | `0.7` | 可選 |
| `ANTHROPIC_MAX_TOKENS` | Claude 回應最大 token 数 | `8192` | 可選 |

> *注：`ANSPIRE_API_KEYS`、`AIHUBMIX_KEY`、`GEMINI_API_KEY`、`ANTHROPIC_API_KEY`、`OPENAI_API_KEY` 或 `OLLAMA_API_BASE` 至少配置一个。`ANSPIRE_API_KEYS` 与 `AIHUBMIX_KEY` 無需配置 `OPENAI_BASE_URL`，系統自动適配。

### 通知渠道配置

更多通知配置基线、診斷和部署場景说明见 [通知专题文档](notifications.md)。

| 變數名 | 说明 | 必填 |
|--------|------|:----:|
| `WECHAT_WEBHOOK_URL` | 企业微信机器人 Webhook URL | 可選 |
| `FEISHU_WEBHOOK_URL` | 飞书机器人 Webhook URL | 可選 |
| `FEISHU_WEBHOOK_SECRET` | 飞书机器人簽名密钥（仅在机器人安全设置启用“簽名校验”时填写） | 可選 |
| `FEISHU_WEBHOOK_KEYWORD` | 飞书机器人關鍵词（仅在机器人安全设置启用“關鍵词”时填写） | 可選 |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | 可選 |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | 可選 |
| `TELEGRAM_MESSAGE_THREAD_ID` | Telegram Topic ID | 可選 |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL | 可選 |
| `DISCORD_BOT_TOKEN` | Discord Bot Token（与 Webhook 二选一） | 可選 |
| `DISCORD_MAIN_CHANNEL_ID` | Discord Channel ID（使用 Bot 时需要） | 可選 |
| `DISCORD_INTERACTIONS_PUBLIC_KEY` | Discord Public Key（仅入站 Interaction/Webhook 回调验签时需要） | 可選 |
| `DISCORD_MAX_WORDS` | Discord 最大字数限制（預設 免费服務器限制2000） | 可選 |
| `SLACK_BOT_TOKEN` | Slack Bot Token（推荐，支援图片上傳；同时配置时優先于 Webhook） | 可選 |
| `SLACK_CHANNEL_ID` | Slack Channel ID（使用 Bot 时需要） | 可選 |
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL（仅文本，不支援图片） | 可選 |
| `EMAIL_SENDER` | 发件人邮箱 | 可選 |
| `EMAIL_PASSWORD` | 邮箱授權码（非登录密碼） | 可選 |
| `EMAIL_RECEIVERS` | 收件人邮箱（逗号分隔，留空发给自己） | 可選 |
| `EMAIL_SENDER_NAME` | 发件人顯示名称 | 可選 |
| `STOCK_GROUP_N` / `EMAIL_GROUP_N` | 電郵分組路由（Issue #268）：`STOCK_GROUP_N` 应为 `STOCK_LIST` 子集，仅影响電郵收件人，不改变分析範圍或其他通知渠道 | 可選 |
| `CUSTOM_WEBHOOK_URLS` | 自定义 Webhook（逗号分隔） | 可選 |
| `CUSTOM_WEBHOOK_BEARER_TOKEN` | 自定义 Webhook Bearer Token | 可選 |
| `WEBHOOK_VERIFY_SSL` | 讀取该配置的 webhook-style HTTPS 通知請求证书校验（預設 true）。设为 false 可支援自簽名。警告：關閉有严重安全風險 | 可選 |
| `PUSHOVER_USER_KEY` | Pushover 使用者 Key | 可選 |
| `PUSHOVER_API_TOKEN` | Pushover API Token | 可選 |
| `NTFY_URL` | ntfy 完整 topic endpoint，必须包含 topic path，例如 `https://ntfy.sh/my-topic` | 可選 |
| `NTFY_TOKEN` | ntfy Bearer Token（可選） | 可選 |
| `GOTIFY_URL` | Gotify server base URL，不包含 `/message` | 可選 |
| `GOTIFY_TOKEN` | Gotify application token，通过 `X-Gotify-Key` Header 发送 | 可選 |
| `PUSHPLUS_TOKEN` | PushPlus Token（国内推送服務） | 可選 |
| `SERVERCHAN3_SENDKEY` | Server酱³ Sendkey | 可選 |
| `ASTRBOT_URL` | AstrBot Webhook URL | 可選 |
| `ASTRBOT_TOKEN` | AstrBot Bearer Token（可選） | 可選 |
| `NOTIFICATION_REPORT_CHANNELS` | report 路由渠道，逗号分隔；允許值：wechat,feishu,telegram,email,pushover,ntfy,gotify,pushplus,serverchan3,custom,discord,slack,astrbot | 可選 |
| `NOTIFICATION_ALERT_CHANNELS` | alert 路由渠道，逗号分隔；留空保持全渠道 | 可選 |
| `NOTIFICATION_SYSTEM_ERROR_CHANNELS` | system_error 预留路由渠道，逗号分隔；留空保持全渠道 | 可選 |
| `NOTIFICATION_DEDUP_TTL_SECONDS` | 通知去重 TTL 秒数，`0` 關閉 | 可選 |
| `NOTIFICATION_COOLDOWN_SECONDS` | 通知冷却秒数，`0` 關閉 | 可選 |
| `NOTIFICATION_QUIET_HOURS` | 静默时段，格式 `HH:MM-HH:MM`，支援跨午夜 | 可選 |
| `NOTIFICATION_TIMEZONE` | 静默时段时区，如 `Asia/Shanghai`；留空跟随 `TZ` 或系統本機时区 | 可選 |
| `NOTIFICATION_MIN_SEVERITY` | 最低通知級別：info, warning, error, critical；留空保持现状 | 可選 |
| `NOTIFICATION_DAILY_DIGEST_ENABLED` | 每日摘要预留开关；当前不会发送摘要 | 可選 |

> 说明：預設 `daily_analysis` GitHub Actions workflow 只映射固定變數名，不会自动匯入任意编号的 `STOCK_GROUP_N` / `EMAIL_GROUP_N`。因此分組邮箱目前仅在本機 `.env`、Docker 或其他已显式注入这些環境變數的執行環境中生效；若你要在自己的 GitHub Actions 中使用，需在 workflow 的 job `env:` 中逐组显式映射。

#### 飞书云文档配置（可選，解決訊息截斷議題）

| 變數名 | 说明 | 必填 |
|--------|------|:----:|
| `FEISHU_APP_ID` | 飞书应用 ID | 可選 |
| `FEISHU_APP_SECRET` | 飞书应用 Secret | 可選 |
| `FEISHU_FOLDER_TOKEN` | 飞书云盘文件夹 Token | 可選 |

> 飞书云文档配置步骤：
> 1. 在 [飞书开发者后台](https://open.feishu.cn/app) 建立应用
> 2. 配置 GitHub Secrets
> 3. 建立群組并添加应用机器人
> 4. 在云盘文件夹中添加群組为协作者（可管理權限）
>
> 说明：`FEISHU_APP_ID` / `FEISHU_APP_SECRET` 用于飞书应用、云文档或 Stream Bot 模式，不会直接启用群 Webhook 推送。只想收通知时，请優先配置 `FEISHU_WEBHOOK_URL`。

### 搜尋服務配置

| 變數名 | 说明 | 必填 |
|--------|------|:----:|
| `ANSPIRE_API_KEYS` | Anspire Open API Key（可用于搜尋与大模型网关共享場景的配置示例；是否可用取决于账号權限与网关可见性，可有效增强 A 股分析效果） | 推荐 |
| `SERPAPI_API_KEYS` | SerpAPI 搜尋引擎结果补强，适合实时金融新闻 | 推荐 |
| `TAVILY_API_KEYS` | Tavily 搜尋 API Key | 可選 |
| `BOCHA_API_KEYS` | 博查搜尋 API Key（中文最佳化） | 可選 |
| `BRAVE_API_KEYS` | Brave Search API Key（美股最佳化） | 可選 |
| `MINIMAX_API_KEYS` | MiniMax Coding Plan Web Search（结构化搜尋结果） | 可選 |
| `SOCIAL_SENTIMENT_API_KEY` | Stock Sentiment API Key（Reddit / X / Polymarket，可選） | 可選 |
| `SOCIAL_SENTIMENT_API_URL` | Stock Sentiment API 地址（預設 `https://api.adanos.org`） | 可選 |
| `SEARXNG_BASE_URLS` | SearXNG 自建实例（无配額兜底，需在 settings.yml 启用 format: json）；留空时預設自动发现公共实例 | 可選 |
| `SEARXNG_PUBLIC_INSTANCES_ENABLED` | 是否在 `SEARXNG_BASE_URLS` 为空时自动从 `searx.space` 獲取公共实例（預設 `true`） | 可選 |
| `NEWS_STRATEGY_PROFILE` | 新闻策略窗口档位：`ultra_short`(1天)/`short`(3天)/`medium`(7天)/`long`(30天)；實際窗口取与 `NEWS_MAX_AGE_DAYS` 的最小值 | 預設 `short` |
| `NEWS_MAX_AGE_DAYS` | 新闻最大时效（天），搜尋时限制结果在近期内 | 預設 `3` |
| `BIAS_THRESHOLD` | 乖离率閾值（%），超过提示不追高；强势趨勢股自动放宽到 1.5 倍 | 預設 `5.0` |

> 行为说明：搜尋服務与社交舆情服務为可選增强鏈路。任一服務初始化失败时，系統会记录 warning 并降級为略過该服務，仅影响对应环节，不会阻塞技术面主鏈路和主工作流。

### 數據源配置

| 變數名 | 说明 | 預設值 | 必填 |
|--------|------|--------|:----:|
| `TUSHARE_TOKEN` | Tushare Pro Token | - | 可選 |
| `TICKFLOW_API_KEY` | TickFlow API Key；配置后 A 股大盤复盘指數優先嘗試 TickFlow，若套餐支援标的池查詢则市场統計也会優先嘗試 TickFlow | - | 可選 |
| `LONGBRIDGE_APP_KEY` | [Longbridge OpenAPI](https://open.longbridge.com/) App Key；配置后美股/港股的量比、换手率、PE 等 YFinance 缺失欄位会自动从长桥补充 | - | 可選 |
| `LONGBRIDGE_APP_SECRET` | Longbridge App Secret | - | 可選 |
| `LONGBRIDGE_ACCESS_TOKEN` | Longbridge Access Token | - | 可選 |
| `LONGBRIDGE_*`（可選） | 见官方 [環境變數](https://open.longbridge.com/zh-CN/docs/getting-started#環境變數)；另有 `LONGBRIDGE_STATIC_INFO_TTL_SECONDS` 与 `LONGBRIDGE_CONNECTION_COOLDOWN_SECONDS` | - | 可選 |
| `ENABLE_REALTIME_QUOTE` | 启用实时行情（關閉后使用历史收盤价分析） | `true` | 可選 |
| `ENABLE_REALTIME_TECHNICAL_INDICATORS` | 盘中实时技术面：启用时用实时价计算 MA5/MA10/MA20 与多头排列（Issue #234）；關閉则用昨日收盤 | `true` | 可選 |
| `ENABLE_CHIP_DISTRIBUTION` | 启用筹码分布分析（该介面不稳定，云端部署建议關閉）。GitHub Actions 使用者需在 Repository Variables 中设置 `ENABLE_CHIP_DISTRIBUTION=true` 方可启用；workflow 預設關閉。 | `true` | 可選 |
| `ENABLE_EASTMONEY_PATCH` | 东财介面补丁：东财介面頻繁失败（如 RemoteDisconnected、連線被關閉）时建议设为 `true`，注入 NID 令牌与隨機 User-Agent 以降低被限流機率 | `false` | 可選 |
| `REALTIME_SOURCE_PRIORITY` | 实时行情數據源優先级（逗号分隔），如 `tencent,akshare_sina,efinance,akshare_em` | 见 .env.example | 可選 |
| `ENABLE_FUNDAMENTAL_PIPELINE` | 基本面聚合总开关；關閉时仅傳回 `not_supported` 块，不改变原分析鏈路 | `true` | 可選 |
| `FUNDAMENTAL_STAGE_TIMEOUT_SECONDS` | 基本面阶段总时延预算（秒） | `8.0` | 可選 |
| `FUNDAMENTAL_FETCH_TIMEOUT_SECONDS` | 单能力源呼叫逾時（秒） | `3.0` | 可選 |
| `FUNDAMENTAL_RETRY_MAX` | 基本面能力重試次数（含首次） | `1` | 可選 |
| `FUNDAMENTAL_CACHE_TTL_SECONDS` | 基本面聚合快取 TTL（秒），短快取减轻重复拉取 | `120` | 可選 |
| `FUNDAMENTAL_CACHE_MAX_ENTRIES` | 基本面快取最大条目数（TTL 内按时间淘汰） | `256` | 可選 |

> 行为说明：
> - A 股：按 `valuation/growth/earnings/institution/capital_flow/dragon_tiger/boards` 聚合能力傳回；
> - ETF：傳回可得项，缺失能力标记为 `not_supported`，整体不影响原流程；
> - 美股/港股：傳回 `not_supported` 兜底块；
> - 任何例外走 fail-open，仅记录錯誤，不影响技术面/新闻/筹码主鏈路。
> - 配置 `TICKFLOW_API_KEY` 后，仅 A 股大盤复盘会额外優先嘗試 TickFlow 的主要指數行情；若当前套餐支援标的池查詢，市场漲跌統計也会優先嘗試 TickFlow。個股鏈路和实时行情優先级不变。
> - TickFlow 能力按套餐權限分層：有限權限套餐仍可使用主指數查詢；支援 `CN_Equity_A` 标的池查詢的套餐才会启用 TickFlow 市场統計。
> - 官方 quickstart 已文档化 `quotes.get(universes=["CN_Equity_A"])`，但线上 smoke test 进一步确认：`TICKFLOW_API_KEY` 不等于一定具备该權限，且 `quotes.get(symbols=[...])` 单次存在标的数量限制。
> - TickFlow 實際傳回的 `change_pct` / `amplitude` 为比例值；系統已在接入层统一轉換为百分比值，確保与现有數據源欄位语义一致。
> - A 股大盤复盘报告采用盘后工作台式结构：固定包含大盤红绿灯、盘面温度、指數明细、板塊 Top 表、新闻催化、明日交易计划和風險提示；若部分數據源缺失，则保留可用区块并在对应位置降級展示。
> - 欄位契约：
>   - `fundamental_context.belong_boards` = 個股關聯板塊列表（当前仅 A 股写入；无數據时为 `[]`）；
>   - `fundamental_context.boards.data` = `sector_rankings`（板塊漲跌榜，结构 `{top, bottom}`）；
>   - `fundamental_context.earnings.data.financial_report` = 财报摘要（报告期、营收、归母净利潤、经营现金流、ROE）；
>   - `fundamental_context.earnings.data.dividend` = 分红指標（仅现金分红税前口径，含 `events`、`ttm_cash_dividend_per_share`、`ttm_dividend_yield_pct`）；
>   - `get_stock_info.belong_boards` = 個股所属板塊列表；
>   - `get_stock_info.boards` 为相容别名，值与 `belong_boards` 相同（未来仅在大版本考虑移除）；
>   - `get_stock_info.sector_rankings` 与 `fundamental_context.boards.data` 保持一致。
>   - `AnalysisReport.details.belong_boards` = 结构化报告详情中的關聯板塊列表；
>   - `AnalysisReport.details.sector_rankings` = 结构化报告详情中的板塊漲跌榜（用于前端板塊联动展示）。
> - 板塊漲跌榜使用數據源顺序：与全局 priority 一致。
> - 逾時控制为 `best-effort` 软逾時：阶段会按预算快速降級繼續執行，但不保证硬中断底层三方呼叫。
> - `FUNDAMENTAL_STAGE_TIMEOUT_SECONDS=8.0` 表示新增基本面阶段的目标预算，不是严格硬 SLA；Windows、Docker 或免费數據源被限流时可繼續调高到 `12-15s`。
> - 若要硬 SLA，请在后续版本升級为子程式隔離執行并在逾時后強制终止。

### 其他配置

| 變數名 | 说明 | 預設值 |
|--------|------|--------|
| `STOCK_LIST` | 自选股代碼（逗号分隔） | - |
| `ADMIN_AUTH_ENABLED` | Web 登录：设为 `true` 启用密碼保护；首次訪問在网页设置初始密碼，可在「系統设置 > 修改密碼」修改；忘记密碼執行 `python -m src.auth reset_password`。Web 的 `.env` 備份匯入匯出仅在开启该开关后可用（桌面端不受此限制）。 | `false` |
| `TRUST_X_FORWARDED_FOR` | 单层可信反向代理部署时设为 `true`，取 `X-Forwarded-For` 最右值作为真实客户端 IP（用于登录限流等）；直连公网时保持 `false` 防伪造。多级代理/CDN 場景下限流 key 可能退化为边缘代理 IP，需额外評估 | `false` |
| `MAX_WORKERS` | 並行執行緒数 | `3` |
| `MARKET_REVIEW_ENABLED` | 启用大盤复盘 | `true` |
| `MARKET_REVIEW_REGION` | 大盤复盘市场区域：cn(A股)、hk(港股)、us(美股)、both(三市场)，us 适合仅关注美股的使用者 | `cn` |
| `MARKET_REVIEW_COLOR_SCHEME` | 大盤复盘指數漲跌颜色：`green_up`=绿涨红跌（預設），`red_up`=红涨绿跌 | `green_up` |
| `TRADING_DAY_CHECK_ENABLED` | 交易日檢查：預設 `true`，非交易日略過執行；设为 `false` 或使用 `--force-run` 可強制執行（Issue #373） | `true` |
| `SCHEDULE_ENABLED` | 启用定时工作 | `false` |
| `SCHEDULE_TIME` | 定时執行时间 | `18:00` |
| `LOG_DIR` | 日誌目錄 | `./logs` |

---

## Docker 部署

Dockerfile 使用多阶段构建，前端会在构建镜像时自动打包并内置到 `static/`。
如需覆盖静态资源，可挂载本機 `static/` 到容器内 `/app/static`。
執行中的 `server` 容器預設直接复用 `/app/static` 里的预构建产物，不要求容器内保留 `apps/dsa-web` 源码目錄或執行时安裝 `npm`；若 WebUI 無法打开，请優先确认 `/app/static/index.html` 是否存在。

当前官方镜像發佈地址：

- GHCR：`ghcr.io/zhulinsen/daily_stock_analysis:<tag>`
- Docker Hub：`<DOCKERHUB_USERNAME>/daily_stock_analysis:<tag>`（由發佈者的 `DOCKERHUB_USERNAME` secret 决定，官方發佈为 `zhulinsen/daily_stock_analysis`）

### 快速啟動

```bash
# 1. 克隆倉庫
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git
cd daily_stock_analysis

# 2. 配置環境變數
cp .env.example .env
vim .env  # 填入 API Key 和配置

# 3. 啟動容器
docker-compose -f ./docker/docker-compose.yml up -d server     # Web 服務模式（推荐，提供 API 与 WebUI）
docker-compose -f ./docker/docker-compose.yml up -d analyzer   # 定时工作模式
docker-compose -f ./docker/docker-compose.yml up -d            # 同时啟動两种模式

# 4. 訪問 WebUI
# http://localhost:8000

# 5. 查看日誌
docker-compose -f ./docker/docker-compose.yml logs -f server
```

### 直接拉官方镜像執行

如果你不打算在目标机器上保留源码，可以直接拉取官方镜像：

```bash
# Web/API 模式
docker pull zhulinsen/daily_stock_analysis:latest
docker run -d \
  --name dsa-server \
  --env-file .env \
  -p 8000:8000 \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/reports:/app/reports" \
  -v "$(pwd)/.env:/app/.env" \
  zhulinsen/daily_stock_analysis:latest \
  python main.py --serve-only --host 0.0.0.0 --port 8000

# 定时工作模式
docker run -d \
  --name dsa-analyzer \
  --env-file .env \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/reports:/app/reports" \
  -v "$(pwd)/.env:/app/.env" \
  zhulinsen/daily_stock_analysis:latest
```

如需固定版本或便于回滚，请将 `latest` 替換为具体版本 tag，例如 `v3.13.0`。

### 執行模式说明

| 命令 | 说明 | 端口 |
|------|------|------|
| `docker-compose -f ./docker/docker-compose.yml up -d server` | Web 服務模式，提供 API 与 WebUI | 8000 |
| `docker-compose -f ./docker/docker-compose.yml up -d analyzer` | 定时工作模式，每日自动執行 | - |
| `docker-compose -f ./docker/docker-compose.yml up -d` | 同时啟動两种模式 | 8000 |

### Docker Compose 配置

`docker-compose.yml` 使用 YAML 锚点复用配置：

```yaml
version: '3.8'

x-common: &common
  build:
    context: ..
    dockerfile: docker/Dockerfile
  restart: unless-stopped
  env_file:
    - ../.env
  environment:
    - TZ=Asia/Shanghai
  volumes:
    - ../data:/app/data
    - ../logs:/app/logs
    - ../reports:/app/reports
    - ../.env:/app/.env

services:
  # 定时工作模式
  analyzer:
    <<: *common
    container_name: stock-analyzer

  # FastAPI 模式
  server:
    <<: *common
    container_name: stock-server
    command: ["python", "main.py", "--serve-only", "--host", "0.0.0.0", "--port", "8000"]
    ports:
      - "8000:8000"
```

### `.env` 与數據目錄映射说明

无论你使用 `docker run` 还是 Compose，建议同时保留下面两种映射：

- 環境變數注入：`--env-file .env` 或 Compose 的 `env_file`
  作用：把 `.env` 中的键值作为容器啟動时的環境變數传入 Python 程式。
- 文件映射：`-v "$(pwd)/.env:/app/.env"` 或 Compose 的 `../.env:/app/.env`
  作用：让容器内的 Web 设置页和后端读写同一份 `.env` 文件，修改后可持久化到宿主机。

推荐同时映射这几个目錄：

- `./data:/app/data`：資料庫、快取和執行时數據
- `./logs:/app/logs`：日誌輸出
- `./reports:/app/reports`：生成的分析报告
- `./strategies:/app/strategies:ro`：自定义策略 YAML（只读挂载）

官方 Docker 镜像啟動时会自动建立并修复 `/app/data`、`/app/logs`、`/app/reports` 的挂载目錄權限，然后降权为容器内非 root 使用者 `dsa`（UID/GID `1000:1000`）執行应用。普通 Docker / Compose 部署不需要手动 `chown` 或 `chmod` 宿主机目錄。

如果你通过 `--user` 或 Compose `user:` 指定了其他執行使用者，或使用只读挂载、rootless Docker、NFS 等限制 `chown` 的存储環境，自动修复可能無法生效。此时请確保實際執行使用者对 `data`、`logs`、`reports` 具备写入權限，或改用可写卷。

如果你需要覆盖内置静态资源，还可以额外挂载：

- `./static:/app/static:ro`

### 常用命令

```bash
# 查看執行狀態
docker-compose -f ./docker/docker-compose.yml ps

# 查看日誌
docker-compose -f ./docker/docker-compose.yml logs -f server

# 停止服務
docker-compose -f ./docker/docker-compose.yml down

# 重建镜像（代碼更新后）
docker-compose -f ./docker/docker-compose.yml build --no-cache
docker-compose -f ./docker/docker-compose.yml up -d server
```

### 手动构建镜像

```bash
docker build -f docker/Dockerfile -t stock-analysis .
docker run -d \
  --name dsa-server-local \
  --env-file .env \
  -p 8000:8000 \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/reports:/app/reports" \
  -v "$(pwd)/.env:/app/.env" \
  stock-analysis \
  python main.py --serve-only --host 0.0.0.0 --port 8000
```

---

## 本機執行詳細配置

### 安裝依賴

```bash
# Python 3.10+ 推荐
pip install -r requirements.txt

# 或使用 conda
conda create -n stock python=3.10
conda activate stock
pip install -r requirements.txt
```

**智能匯入依賴**：`pypinyin`（名称→代碼拼音匹配）和 `openpyxl`（Excel .xlsx 解析）已包含在 `requirements.txt` 中，執行上述 `pip install -r requirements.txt` 时会自动安裝。若使用智能匯入（图片/CSV/Excel/剪贴板）功能，请確保依賴已正确安裝；缺失时可能报 `ModuleNotFoundError`。

### 命令行參數

```bash
python main.py                        # 完整分析（個股 + 大盤复盘）
python main.py --market-review        # 仅大盤复盘
python main.py --no-market-review     # 仅個股分析
python main.py --stocks 600519,300750 # 指定股票
python main.py --dry-run              # 仅獲取數據，不 AI 分析
python main.py --no-notify            # 不发送推送
python main.py --schedule             # 定时工作模式
python main.py --force-run            # 非交易日也強制執行（Issue #373）
python main.py --debug                # 调试模式（詳細日誌）
python main.py --workers 5            # 指定並行数
```

---

## 定时工作配置

### GitHub Actions 定时

编辑 `.github/workflows/daily_analysis.yml`:

```yaml
schedule:
  # UTC 时间，北京时间 = UTC + 8
  - cron: '0 10 * * 1-5'   # 週一到週五 18:00（北京时间）
```

常用时间对照：

| 北京时间 | UTC cron 表达式 |
|---------|----------------|
| 09:30 | `'30 1 * * 1-5'` |
| 12:00 | `'0 4 * * 1-5'` |
| 15:00 | `'0 7 * * 1-5'` |
| 18:00 | `'0 10 * * 1-5'` |
| 21:00 | `'0 13 * * 1-5'` |

#### GitHub Actions 非交易日手动執行（Issue #461 / #466）

`daily_analysis.yml` 支援两种控制方式：

- `TRADING_DAY_CHECK_ENABLED`：倉庫级配置（`Settings → Secrets and variables → Actions`），預設 `true`
- `workflow_dispatch.force_run`：手动触发时的单次开关，預設 `false`

推荐優先级理解：

| 配置组合 | 非交易日行为 |
|---------|-------------|
| `TRADING_DAY_CHECK_ENABLED=true` + `force_run=false` | 略過執行（預設行为） |
| `TRADING_DAY_CHECK_ENABLED=true` + `force_run=true` | 本次強制執行 |
| `TRADING_DAY_CHECK_ENABLED=false` + `force_run=false` | 始终執行（定时和手动都不檢查交易日） |
| `TRADING_DAY_CHECK_ENABLED=false` + `force_run=true` | 始终執行 |

手动触发步骤：

1. 打开 `Actions → 每日股票分析 → Run workflow`
2. 选择 `mode`（`full` / `market-only` / `stocks-only`）
3. 若当天是非交易日且希望仍執行，将 `force_run` 设为 `true`
4. 点击 `Run workflow`

### 本機定时工作

内建的定时工作调度器支援每天在指定时间（預設 18:00）執行分析。

#### 命令行方式

```bash
# 啟動定时模式（啟動时立即執行一次，随后每天 18:00 執行）
python main.py --schedule

# 啟動定时模式（啟動时不執行，仅等待下次定时触发）
python main.py --schedule --no-run-immediately
```

> 说明：定时模式每次触发前都会重新讀取当前保存的 `STOCK_LIST`。如果同时传入 `--stocks`，该參數不会锁定后续计划執行的股票列表；需要暫時只跑指定股票时，请使用非定时的单次執行命令。
>
> 从 `python main.py --schedule`、`python main.py --serve --schedule` 或等价内置调度模式啟動后，WebUI 保存新的 `SCHEDULE_TIME` 会在下一轮调度檢查内自动重绑 daily job，無需重啟程式；旧的執行时间不会繼續保留。

#### 環境變數方式

你也可以通过環境變數配置定时行为（适用于 Docker 或 .env）：

| 變數名 | 说明 | 預設值 | 示例 |
|--------|------|:-------:|:-----:|
| `SCHEDULE_ENABLED` | 是否启用定时工作 | `false` | `true` |
| `SCHEDULE_TIME` | 每日執行时间 (HH:MM) | `18:00` | `09:30` |
| `SCHEDULE_RUN_IMMEDIATELY` | 定时模式啟動时是否立即執行一次；未显式设置时沿用 `RUN_IMMEDIATELY` 的執行时覆盖语义 | `true` | `false` |
| `RUN_IMMEDIATELY` | 非定时模式啟動时是否立即執行一次；同时作为未显式设置 `SCHEDULE_RUN_IMMEDIATELY` 时的 legacy 回退 | `true` | `false` |
| `TRADING_DAY_CHECK_ENABLED` | 交易日檢查：非交易日略過執行；设为 `false` 可強制執行 | `true` | `false` |

例如在 Docker 中配置：

```bash
# 设置啟動时不立即分析
docker run -e SCHEDULE_ENABLED=true -e SCHEDULE_RUN_IMMEDIATELY=false ...
```

> 相容说明：如果執行时显式传入 `RUN_IMMEDIATELY`，但没有单独传 `SCHEDULE_RUN_IMMEDIATELY`，内置调度模式会繼續继承前者，避免被 `.env` 中持久化的 `SCHEDULE_RUN_IMMEDIATELY` 旧值反向覆盖。

#### 交易日判斷（Issue #373）

預設根据自选股市场（A 股 / 港股 / 美股）和 `MARKET_REVIEW_REGION` 判斷是否为交易日：
- 使用 `exchange-calendars` 区分 A 股 / 港股 / 美股各自的交易日历（含節假日）
- 混合持倉时，每只股票只在其市场开市日分析，休市股票当日略過
- 全部相關市场均为非交易日时，整体略過執行（不啟動 pipeline、不发推送）
- 断点续传和 `--dry-run` 的“數據已存在”判斷共用同一套“最新可复用交易日”解析邏輯，不再直接使用服務器自然日
- `最新可复用交易日` 会按股票所属市场的本機时区解析：A 股使用 `Asia/Shanghai`，港股使用 `Asia/Hong_Kong`，美股使用 `America/New_York`
- 非交易日（週末 / 節假日）執行时，会回退到最近一个交易日檢查本機數據；若该交易日數據已存在，则略過重复抓取，否则繼續补数
- 交易日盘中或收盤前執行时，会以上一个已完成交易日作为复用目标；交易日收盤后執行时，当日數據已存在则可直接略過，不存在则繼續抓取
- 覆盖方式：`TRADING_DAY_CHECK_ENABLED=false` 或 命令行 `--force-run`

#### 使用 Crontab

如果不想使用常驻程式，也可以使用系統的 Cron：

```bash
crontab -e
# 添加：0 18 * * 1-5 cd /path/to/project && python main.py
```

---

## 通知渠道詳細配置

通知渠道矩阵、minimal/advanced key 分層、`--check-notify` 診斷口径和場景化配置说明见 [通知专题文档](notifications.md)。

### 企业微信

1. 在企业微信群聊中添加"群机器人"
2. 复制 Webhook URL
3. 设置 `WECHAT_WEBHOOK_URL`

### 飞书

> ⚠️ **關鍵区分**：`FEISHU_WEBHOOK_SECRET`（Webhook 簽名密钥）和 `FEISHU_APP_SECRET`（飞书应用 Secret）是两个完全不同的配置，不能互换。

**最小可用配置（无安全限制）：**

```env
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/your_hook_token
```

**完整步骤：**

1. **在飞书群聊中建立自定义机器人**：
   - 打开目标群聊 → 右上角「群设置」→「群机器人」→「添加机器人」→「自定义机器人」
   - 填写机器人名称，复制生成的 **Webhook URL**（格式：`https://open.feishu.cn/open-apis/bot/v2/hook/...`）
2. 设置 `FEISHU_WEBHOOK_URL`（即上一步复制的 URL）。
3. 查看机器人**安全设置**，根据启用的安全项决定是否需要补充配置：
   - **无额外安全设置**：仅填 `FEISHU_WEBHOOK_URL` 即可。
   - **开启了「簽名校验」**：把飞书顯示的 secret 填到 `FEISHU_WEBHOOK_SECRET`。两端必须同时启用或同时不填，否则飞书傳回簽名校验失败。
   - **开启了「關鍵词」**：把同一个關鍵词填到 `FEISHU_WEBHOOK_KEYWORD`；系統会自动在每条訊息前补上，無需手动修改报告模板。
   - **开启了 IP 白名单**：確保当前執行環境的出口 IP 在白名单中（本機/Docker/GitHub Actions 出口 IP 各不相同）。
4. `FEISHU_APP_ID` / `FEISHU_APP_SECRET` 是飞书应用 / Stream Bot / 云文档模式专用，不会触发群 Webhook 推送，不要用它们替代 `FEISHU_WEBHOOK_URL`。

**常见失败原因：**
- 只填了 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`，没有配置 `FEISHU_WEBHOOK_URL`
- 飞书机器人开启了「簽名校验」，但 `FEISHU_WEBHOOK_SECRET` 未配置（或误填为 `FEISHU_APP_SECRET`）
- 飞书机器人开启了「關鍵词」，但本機没有同步配置 `FEISHU_WEBHOOK_KEYWORD`
- 机器人没有被加入目标群，或群管理员限制了机器人发言
- 飞书侧额外配置了 IP 白名单，但当前執行環境 IP 不在白名单中
- 訊息内容超长：飞书单条訊息有长度限制，系統会自动分段发送；如需在一个文档内查看完整内容，可配置飞书云文档功能（`FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_FOLDER_TOKEN`）

更完整的图文排查请看 [docs/bot/feishu-bot-config.md](bot/feishu-bot-config.md)。
### Telegram

1. 与 @BotFather 对话建立 Bot
2. 獲取 Bot Token
3. 獲取 Chat ID（可通过 @userinfobot）
4. 设置 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID`
5. (可選) 如需发送到 Topic，设置 `TELEGRAM_MESSAGE_THREAD_ID` (从 Topic 链接末尾獲取)

### 電郵

1. 开启邮箱的 SMTP 服務
2. 獲取授權码（非登录密碼）
3. 设置 `EMAIL_SENDER`、`EMAIL_PASSWORD`、`EMAIL_RECEIVERS`

支援的邮箱：
- QQ 邮箱：smtp.qq.com:465
- 163 邮箱：smtp.163.com:465
- Gmail：smtp.gmail.com:587

**股票分組发往不同邮箱**（Issue #268，可選）：
配置 `STOCK_GROUP_N` 与 `EMAIL_GROUP_N` 可實現不同股票组的报告发送到不同邮箱，例如多人共享分析时互不干扰。`STOCK_LIST` 仍决定本次實際分析的股票集合，`STOCK_GROUP_N` 应写成 `STOCK_LIST` 的子集；它只影响電郵收件人，不会改变 Telegram、企业微信、Webhook 等其他渠道收到的完整报告。大盤复盘会发往所有配置的邮箱。

> GitHub Actions 限制：截至 2026-03-29，倉庫自带 `daily_analysis.yml` 不会自动匯入任意编号的 `STOCK_GROUP_N` / `EMAIL_GROUP_N`。因此如果你只在倉庫 Secrets / Variables 中新增这些變數，而没有修改 workflow 显式映射，它们不会进入執行程式，看起来就像“分組配置不生效”。

```bash
STOCK_LIST=600519,300750,002594,AAPL
STOCK_GROUP_1=600519,300750
EMAIL_GROUP_1=user1@example.com
STOCK_GROUP_2=002594,AAPL
EMAIL_GROUP_2=user2@example.com
```

### 自定义 Webhook

支援任意 POST JSON 的 Webhook，包括：
- 钉钉机器人
- Discord Webhook
- Slack Webhook
- Bark（iOS 推送）
- 自建服務

设置 `CUSTOM_WEBHOOK_URLS`，多个用逗号分隔。

如需適配 AstrBot、NapCat 或自建服務的特殊 body，可设置 `CUSTOM_WEBHOOK_BODY_TEMPLATE`。这是全局模板，会先于 Bark、Slack、Discord 等 URL 自动识别 payload 生效；如果渲染后不是 JSON object，系統会回退預設 payload。推荐使用 `$content_json` / `$title_json` 避免换行和引号破坏 JSON：

```env
CUSTOM_WEBHOOK_BODY_TEMPLATE={"msg_type":"text","content":$content_json}
```

可用占位符：`$content_json`、`$content`、`$title_json`、`$title`。其中 `$content` / `$title` 是裸字符串，不做 JSON 转义；正文含双引号或换行时可能触发 fallback。

Bark 使用全局模板时需显式写出 Bark body：

```env
CUSTOM_WEBHOOK_BODY_TEMPLATE={"title":$title_json,"body":$content_json,"group":"stock"}
```

NapCat / OneBot 示例需按實際 endpoint、`user_id` 或 `group_id` 調整：

```env
CUSTOM_WEBHOOK_BODY_TEMPLATE={"user_id":123456,"message":$content_json}
```

### ntfy / Gotify

ntfy 和 Gotify 都是一等通知渠道，只发送文本 / JSON，不参与 Markdown 转图片。

ntfy 使用完整 topic endpoint，最后一个 path segment 会作为 topic：

```env
NTFY_URL=https://ntfy.sh/my-topic
NTFY_TOKEN=
```

Gotify 使用 server base URL，系統会自动拼接固定 `/message` API，并通过 `X-Gotify-Key` Header 发送 application token。`GOTIFY_URL` 可包含反向代理 path prefix，但不要包含 `/message`：

```env
GOTIFY_URL=https://gotify.example
GOTIFY_TOKEN=app-token
```

```env
# 實際請求会发送到 https://example.com/gotify/message
GOTIFY_URL=https://example.com/gotify
GOTIFY_TOKEN=app-token
```

`NTFY_URL` 与 `GOTIFY_URL` 的语义不同是两个服務 API 設計不同导致的刻意选择：ntfy 由使用者 topic 构成 endpoint，Gotify 的 `/message` 是固定服務 API。

### Discord

Discord 支援两种方式推送：

**方式一：Webhook（推荐，簡單）**

1. 在 Discord 频道设置中建立 Webhook
2. 复制 Webhook URL
3. 配置環境變數：

```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx/yyy
```

**方式二：Bot API（需要更多權限）**

1. 在 [Discord Developer Portal](https://discord.com/developers/applications) 建立应用
2. 建立 Bot 并獲取 Token
3. 邀请 Bot 到服務器
4. 獲取频道 ID（开发者模式下右键频道复制）
5. 配置環境變數：

```bash
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_MAIN_CHANNEL_ID=your_channel_id
```

如果你要接收 Discord Slash Command / Interaction 回调，而不仅是向 Discord 推送訊息，还需要在 Discord Developer Portal 的 `General Information -> Public Key` 复制公钥并配置：

```bash
DISCORD_INTERACTIONS_PUBLIC_KEY=your_public_key
```

未配置该公钥时，系統会拒絕所有 Discord 入站 webhook 請求。

### Slack

Slack 支援两种方式推送，同时配置时優先使用 Bot API，確保文本与图片发送到同一频道：

**方式一：Bot API（推荐，支援图片上傳）**

1. 建立 Slack App：https://api.slack.com/apps → Create New App
2. 添加 Bot Token Scopes：`chat:write`、`files:write`
3. 安裝到工作区并獲取 Bot Token (xoxb-...)
4. 獲取频道 ID：频道详情 → 底部复制频道 ID
5. 配置環境變數：

```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_CHANNEL_ID=C01234567
```

**方式二：Incoming Webhook（配置簡單，仅文本）**

1. 在 Slack App 管理页面建立 Incoming Webhook
2. 复制 Webhook URL
3. 配置環境變數：

```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T.../B.../xxx
```

### Pushover（iOS/Android 推送）

[Pushover](https://pushover.net/) 是一个跨平台的推送服務，支援 iOS 和 Android。

1. 注册 Pushover 账号并下載 App
2. 在 [Pushover Dashboard](https://pushover.net/) 獲取 User Key
3. 建立 Application 獲取 API Token
4. 配置環境變數：

```bash
PUSHOVER_USER_KEY=your_user_key
PUSHOVER_API_TOKEN=your_api_token
```

特点：
- 支援 iOS/Android 双平台
- 支援通知優先级和声音设置
- 免费額度足够个人使用（每月 10,000 条）
- 訊息可保留 7 天

### Markdown 转图片（可選）

配置 `MARKDOWN_TO_IMAGE_CHANNELS` 可将报告以图片形式发送至不支援 Markdown 的渠道（telegram, wechat, custom, email, slack）。

**依賴安裝**：

1. **imgkit**：已包含在 `requirements.txt`，執行 `pip install -r requirements.txt` 时会自动安裝
2. **wkhtmltopdf**（預設引擎）：系統级依賴，需手动安裝：
   - **macOS**：`brew install wkhtmltopdf`
   - **Debian/Ubuntu**：`apt install wkhtmltopdf`
3. **markdown-to-file**（可選，emoji 支援更好）：`npm i -g markdown-to-file`，并设置 `MD2IMG_ENGINE=markdown-to-file`

未安裝或安裝失败时，将自动回退为 Markdown 文本发送。

**单股推送 + 图片发送**（Issue #455）：

单股推送模式（`SINGLE_STOCK_NOTIFY=true`）下，若希望 Telegram 等渠道以图片形式推送，需同时配置 `MARKDOWN_TO_IMAGE_CHANNELS=telegram` 并安裝转图工具（wkhtmltopdf 或 markdown-to-file）。個股日报汇总同样支援转图，無需额外配置。

**故障排查**：若日誌出现「Markdown 转图片失败，将回退为文本发送」，请檢查 `MARKDOWN_TO_IMAGE_CHANNELS` 配置及转图工具是否已正确安裝（`which wkhtmltoimage` 或 `which m2f`）。

---

## 數據源配置

系統預設使用 AkShare（免费），也支援其他數據源：

### AkShare（預設）
- 免费，無需配置
- 數據来源：东方财富爬虫

### Tushare Pro
- 需要注册獲取 Token
- 更稳定，數據更全
- 设置 `TUSHARE_TOKEN`

### Baostock
- 免费，無需配置
- 作为备用數據源

### YFinance
- 免费，無需配置
- 支援美股/港股數據
- 美股历史數據与实时行情均统一使用 YFinance，以避免 akshare 美股复权例外导致的技术指標錯誤

### Longbridge（长桥）
- 美股/港股數據兜底，补充 YFinance 缺失的量比、换手率、PE 等欄位
- 需从 [open.longbridge.com](https://open.longbridge.com/) 注册并獲取 App Key / App Secret / Access Token
- 设置 `LONGBRIDGE_APP_KEY`、`LONGBRIDGE_APP_SECRET`、`LONGBRIDGE_ACCESS_TOKEN`
- 可選设置 `LONGBRIDGE_CONNECTION_COOLDOWN_SECONDS` 控制連線關閉类例外后的冷却秒数（預設 15）
- 接入点可配 `LONGBRIDGE_HTTP_URL`、`LONGBRIDGE_QUOTE_WS_URL`、`LONGBRIDGE_TRADE_WS_URL`、`LONGBRIDGE_REGION`
- 其余可選參數见官方 [環境變數说明](https://open.longbridge.com/zh-CN/docs/getting-started#環境變數)
- 仅在 YFinance（美股）或 AkShare（港股）傳回數據不完整时自动触发，不影响 A 股鏈路
- 未配置凭据时不会实例化该可選數據源；若執行时出现連線關閉类例外，会在冷却期内暫時略過 Longbridge，避免請求级頻繁重连

### 东财介面頻繁失败时的處理

若日誌出现 `RemoteDisconnected`、`push2his.eastmoney.com` 連線被關閉等，多为东财限流。建议：

1. 在 `.env` 中设置 `ENABLE_EASTMONEY_PATCH=true`
2. 将 `MAX_WORKERS=1` 降低並行
3. 若已配置 Tushare，可優先使用 Tushare 數據源

---

## 進階功能

### 港股支援

使用 `hk` 前綴指定港股代碼：

```bash
STOCK_LIST=600519,hk00700,hk01810
```

港股日线会略過 efinance、pytdx、baostock 等不支援港股日线的數據源，避免把港股代碼错配到非港股市场；預設改由 AkShare/Tushare/YFinance/Longbridge 等港股路徑繼續兜底。

### ETF 与指數分析

针对指數跟踪型 ETF 和美股指數（如 VOO、QQQ、SPY、510050、SPX、DJI、IXIC），分析仅关注**指數走勢、跟踪误差、市场流动性**，不纳入基金管理人/发行方的公司层面風險（诉讼、声誉、高管变动等）。風險警报与业绩预期均基于指數成分股整体表现，避免将基金公司新闻误判为标的本身利空。详见 Issue #274。

### 多模型切換

配置多个模型，系統自动切換：

```bash
# Gemini（主力）
GEMINI_API_KEY=xxx
GEMINI_MODEL=gemini-3.1-pro-preview

# OpenAI 相容（備選）
OPENAI_API_KEY=xxx
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-v4-flash
# deepseek-chat / deepseek-reasoner 仍相容，但官方已标记为 2026/07/24 后废弃
```

### 進階模型路由（底层由 LiteLLM 驱动）

详见 [LLM 配置指南](LLM_CONFIG_GUIDE.md)。預設使用时你只需要理解主模型、備選模型和模型渠道；如果进入这一节，说明你要直接使用底层 [LiteLLM](https://github.com/BerriAI/litellm) 路由能力，無需单独啟動 Proxy 服務。

**两层機制**：同一模型多 Key 轮换（Router）与跨模型降級（Fallback）分層独立，互不干扰。

**多 Key + 跨模型降級配置示例**：

```env
# 主模型：3 个 Gemini Key 轮换，任一 429 时 Router 自动切換下一个 Key
GEMINI_API_KEYS=key1,key2,key3
LITELLM_MODEL=gemini/gemini-3.1-pro-preview

# 跨模型降級：主模型全部 Key 均失败时，按序嘗試 Claude → GPT
# 需配置对应 API Key：ANTHROPIC_API_KEY、OPENAI_API_KEY
LITELLM_FALLBACK_MODELS=anthropic/claude-sonnet-4-6,openai/gpt-5.4-mini
```

**预期行为**：首次請求用 `key1`；若 429，Router 下次用 `key2`；若 3 个 Key 均不可用，则切換到 Claude，再失败则切換到 GPT。

> ⚠️ `LITELLM_MODEL` 必须包含 provider 前綴（如 `gemini/`、`anthropic/`、`openai/`），
> 否则系統無法识别应使用哪组 API Key。旧格式的 `GEMINI_MODEL`（无前綴）仅用于未配置 `LITELLM_MODEL` 时的自动推断。

**依賴说明**：`requirements.txt` 中保留 `openai>=1.0.0`，因 LiteLLM 内部依賴 OpenAI SDK 作为统一介面；显式保留可確保版本相容性，使用者無需单独配置。

**视觉模型（图片提取股票代碼）**：详见 [LLM 配置指南 - Vision](LLM_CONFIG_GUIDE.md#41-vision-模型图片识别股票代碼)。

从图片提取股票代碼（如 `/api/v1/stocks/extract-from-image`）使用统一视觉模型接入，底层采用 LiteLLM Vision 与 OpenAI `image_url` 格式，支援 Gemini、Claude、OpenAI、DeepSeek 等 Vision-capable 模型。傳回 `items`（code、name、confidence）及相容的 `codes` 数组。

> 相容性说明：`/api/v1/stocks/extract-from-image` 回應在原 `codes` 基礎上新增 `items` 欄位。若下游客户端使用严格 JSON Schema 且不接受未知欄位，请同步更新 schema。

**智能匯入**：除图片外，还支援 CSV/Excel 文件及剪贴板粘贴（`/api/v1/stocks/parse-import`），自动解析代碼/名称列，名称→代碼解析支援本機映射、拼音匹配及 AkShare 在线 fallback。依賴 `pypinyin`（拼音匹配）和 `openpyxl`（Excel 解析），已包含在 `requirements.txt` 中。

- **AkShare 名称解析快取**：名称→代碼解析使用 AkShare 在线 fallback 时，结果快取 1 小时（TTL），避免頻繁請求；首次呼叫或快取过期后会自动刷新。
- **CSV/Excel 列名**：支援 `code`、`股票代碼`、`代碼`、`name`、`股票名称`、`名称` 等（不区分大小写）；无表头时預設第 1 列为代碼、第 2 列为名称。
- **常见解析失败**：文件过大（>2MB）、編碼非 UTF-8/GBK、Excel 工作表为空或损坏、CSV 分隔符/列数不一致时，API 会傳回具体錯誤提示。

- **模型優先级**：`VISION_MODEL` > `LITELLM_MODEL` > 根据已有 API Key 推断（`OPENAI_VISION_MODEL` 已废弃，请改用 `VISION_MODEL`）
- **Provider 回退**：主模型失败时，按 `VISION_PROVIDER_PRIORITY`（預設 `gemini,anthropic,openai`）自动切換到下一个可用 provider
- **主模型不支援 Vision 时**：若主模型为 DeepSeek 等非 Vision 模型，可显式配置 `VISION_MODEL=openai/gpt-5.5` 或 `gemini/gemini-3.1-pro-preview` 供图片提取使用
- **配置校验**：若配置了 `VISION_MODEL` 但未配置对应 provider 的 API Key，啟動时会輸出 warning，图片提取功能将不可用

### 调试模式

```bash
python main.py --debug
```

日誌文件位置：
- 常规日誌：`logs/stock_analysis_YYYYMMDD.log`
- 调试日誌：`logs/stock_analysis_debug_YYYYMMDD.log`

调试日誌預設保留项目自身 DEBUG 資訊，但会将 LiteLLM 内部日誌压低到 `WARNING`，避免流式生成时按 token 写入大量第三方调试日誌；如需排查 LiteLLM 内部细节，可在 `.env` 中暫時设置 `LITELLM_LOG_LEVEL=DEBUG`。

### SQLite 写入稳态配置

預設文件型 SQLite 会在連線建立时启用 `WAL` 并设置 `busy_timeout`，`save_daily_data()` 也已改为按 `(code, date)` 批量原子 upsert，以降低批量更新和並行回写时的锁竞争。

如需調整，可在 `.env` 中设置：

| 變數 | 預設值 | 说明 |
|------|-------|------|
| `SQLITE_WAL_ENABLED` | `true` | 文件型 SQLite 是否启用 `journal_mode=WAL` |
| `SQLITE_BUSY_TIMEOUT_MS` | `5000` | SQLite 等锁逾時（毫秒） |
| `SQLITE_WRITE_RETRY_MAX` | `3` | 遇到 `database is locked` / `database table is locked` 时的最大重試次数 |
| `SQLITE_WRITE_RETRY_BASE_DELAY` | `0.1` | 写入重試基礎退避时间（秒，按指數退避递增） |

---

## 分析决策可操作性

個股报告的操作建议会结合支撑位、压力位、量能/筹码、主力資金流向和風險事件進行校准，避免仅因单日漲跌或評分跨线在“買入/賣出”之间剧烈切換。若价格处在支撑与压力之间且資金流不明確，报告会優先给出“持有、震荡观望、洗盘观察”等中性可執行建议；只有接近支撑确认、有效突破压力且量价/資金配合时才给出買入，跌破關鍵支撑或主力資金持续流出时才给出賣出/减仓。
该项調整会影响可操作决策的執行时落盘与提示词約束鏈路，但不变更 LLM 模型、LiteLLM 路由、Provider/Key 及其相容邊界，不影响配置保存/清理语义。
相容性核验结论：除配置和模型侧语义外，该决策稳定性鏈路覆盖 `src/analyzer.py`、`src/core/pipeline.py`、`src/core/backtest_engine.py`、`src/report_language.py` 及 `src/agent` 决策路徑的執行时行为，建议复核报告决策类型映射与回测入口联动。
核验路徑：相關邏輯在上述執行时路徑与对应測試（`tests/test_backtest_engine.py`、`tests/test_analyzer_news_prompt.py`、`tests/test_decision_stability.py`、`tests/test_agent_pipeline.py` 等）中生效；未在 `src/config.py`、`src/report.py`、存储/持久化鏈路新增配置欄位或清理邏輯。

## 回测功能

回测模組自动对历史 AI 分析记录進行事后驗證，評估分析建议的准确性。

### 工作原理

1. 选取已过冷却期（預設 14 天）的 `AnalysisHistory` 记录
2. 獲取分析日之后的日线數據（前向 K 线）
3. 根据操作建议推断预期方向，与實際走勢对比
4. 評估止盈/止损命中情况，模拟執行收益
5. 汇总为整体和单股两个维度的表现指標

### 操作建议映射

| 操作建议 | 仓位推断 | 预期方向 | 胜利條件 |
|---------|---------|---------|---------|
| 買入/加仓/strong buy | long | up | 涨幅 ≥ 中性带 |
| 賣出/减仓/strong sell | cash | down | 跌幅 ≥ 中性带 |
| 持有/持有观察/震荡观望/洗盘观察/hold/hold and watch/range-bound watch/shakeout watch | long | not_down | 未显著下跌 |
| 观望/等待/wait | cash | flat | 价格在中性带内 |

### 配置

在 `.env` 中设置以下變數（均有預設值，可選）：

| 變數 | 預設值 | 说明 |
|------|-------|------|
| `BACKTEST_ENABLED` | `true` | 是否在每日分析后自动執行回测 |
| `BACKTEST_EVAL_WINDOW_DAYS` | `10` | 評估窗口（交易日数） |
| `BACKTEST_MIN_AGE_DAYS` | `14` | 仅回测 N 天前的记录，避免數據不完整 |
| `BACKTEST_ENGINE_VERSION` | `v1` | 引擎版本号，升級邏輯时用于区分结果 |
| `BACKTEST_NEUTRAL_BAND_PCT` | `2.0` | 中性區間閾值（%），±2% 内视为震荡 |

### 自动執行

回测在每日分析流程完成后自动触发（非阻塞，失败不影响通知推送）。也可通过 API 手动触发。

### 評估指標

| 指標 | 说明 |
|------|------|
| `direction_accuracy_pct` | 方向預測準確率（预期方向与實際一致） |
| `win_rate_pct` | 胜率（胜 / (胜+负)，不含中性） |
| `avg_stock_return_pct` | 平均股票收益率 |
| `avg_simulated_return_pct` | 平均模拟執行收益率（含止盈止损退出） |
| `stop_loss_trigger_rate` | 止损触发率（仅統計配置了止损的记录） |
| `take_profit_trigger_rate` | 止盈触发率（仅統計配置了止盈的记录） |

---

## 本機 WebUI 管理界面

WebUI 与 FastAPI API 服務共用同一服務程式，啟動后可在浏览器中完成配置管理、手动分析、工作进度查看、历史报告、回测、持倉管理和智能匯入等操作。認證、云服務器訪問和 API 呼叫细节见下方说明。

### FastAPI API 服務

FastAPI 提供 RESTful API 服務，支援配置管理和触发分析。

### 啟動方式

| 命令 | 说明 |
|------|------|
| `python main.py --serve` | 啟動 API 服務 + 執行一次完整分析 |
| `python main.py --serve-only` | 仅啟動 API 服務，手动触发分析 |

### 功能特性

- 📝 **配置管理** - 查看/修改自选股列表
- 🚀 **快速分析** - 通过 API 介面触发個股分析；首页也提供“大盤复盘”按钮，可在 Docker/server 模式下后台触发大盤复盘
- 🎯 **策略选择** - 首页支援显式选择分析策略 skill；不传 `skills` 时按系統預設策略執行，便于保持与历史行为相容
- 🧭 **首次配置提示** - 首页会讀取只读配置狀態，缺少 LLM 主渠道、自选股等基礎项时提示缺口并引导进入系統设置
- 📊 **实时进度** - 分析工作狀態实时更新，支援多工作并行；普通分析鏈路在进入 LLM 阶段后会優先嘗試 LiteLLM 流式生成，并通过工作 SSE 回灌更细粒度的 `message/progress`
- 🗂️ **大盤复盘工作可见性** - 首页触发大盤复盘后会傳回 `task_id` 并轮询 `GET /api/v1/analysis/status/{task_id}`，在進行中/完成/失败場景给出可见反馈，失败时直接透出报错内容
- 🧾 **市场复盘历史可复用** - 大盤复盘工作会持久化到分析历史，`report_type` 为 `market_review`，可直接通过历史列表/详情打开对应 Markdown 或详情页，不会重新触发分析重算
- 📈 **回测驗證** - 評估历史分析準確率，查詢方向胜率与模拟收益
- 🔗 **API 文档** - 訪問 `/docs` 查看 Swagger UI

### API 介面

| 介面 | 方法 | 说明 |
|------|------|------|
| `/api/v1/analysis/analyze` | POST | 触发股票分析 |
| `/api/v1/analysis/market-review` | POST | 后台触发大盤复盘；請求体可传 `{"send_notification": true}`；与 `main.py --market-review` 与 `bot` 复用同一套 `GeminiAnalyzer/SearchService/NotificationService` 组装语义 |
| `/api/v1/analysis/tasks` | GET | 查詢工作列表 |
| `/api/v1/analysis/tasks/stream` | GET (SSE) | 订阅工作实时狀態流 |
| `/api/v1/analysis/status/{task_id}` | GET | 查詢工作狀態 |
| `/api/v1/history` | GET | 查詢分析历史 |
| `/api/v1/usage/summary?period=today|month|all` | GET | 按呼叫类型与模型维度汇总 LLM 呼叫次数和 Token 用量 |
| `/api/v1/backtest/run` | POST | 触发回测 |
| `/api/v1/backtest/results` | GET | 查詢回测结果（分页） |
| `/api/v1/backtest/performance` | GET | 獲取整体回测表现 |
| `/api/v1/backtest/performance/{code}` | GET | 獲取单股回测表现 |
| `/api/v1/stocks/extract-from-image` | POST | 从图片提取股票代碼（multipart，逾時 60s） |
| `/api/v1/stocks/parse-import` | POST | 解析 CSV/Excel/剪贴板（multipart file 或 JSON `{"text":"..."}`，文件≤2MB，文本≤100KB） |
| `/api/health` | GET | 健康檢查 |
| `/docs` | GET | API Swagger 文档 |

> 说明：`POST /api/v1/analysis/analyze` 在 `async_mode=false` 时仅支援单只股票；批量 `stock_codes` 需使用 `async_mode=true`。非同步 `202` 回應对单股傳回 `task_id`，对批量傳回 `accepted` / `duplicates` 汇总结构。
> 说明：`POST /api/v1/analysis/analyze` 支援使用 `skills` 传入策略 skill ID 列表；若未传则按服務端預設策略執行。为相容历史呼叫，`strategies` 欄位仍作为相容别名保留。
> 说明：Web 侧首页策略下拉为显式可選策略入口。使用者未手动选择时不会携带 `skills`，与历史客户端行为一致；选择策略后将透传到该介面并在工作狀態与历史快照中保留。
> 说明：`POST /api/v1/analysis/market-review` 采用后端与 CLI/Bot 共用的配置路徑（`GeminiAnalyzer(config=...)` 与同样的搜尋/提示词构造入口）。Provider 相容路由会優先识别并使用 `litellm_model`、`llm_model_list`，若未配置则回退 legacy `GEMINI_*`、`OPENAI_*`、`ANTHROPIC_*`、`DEEPSEEK_*` 键；不会新增/調整 provider、Base URL 或 LiteLLM 路由语义。
> 审计依据：優先级与回退语义以 `src/config.py` 的 `Config._load_from_env()` 为准（`LITELLM_CONFIG` > `LLM_CHANNELS` > legacy）。配套迴歸见 `tests/test_llm_channel_config.py`（配置源解析）与 `tests/test_market_review_runtime.py`（共享装配路徑）。该介面当前仅提供单程式/单机级防重复能力，若为多实例部署需通过外部工作隊列或分布式锁补齐全局幂等。
> 说明：`POST /api/v1/analysis/market-review` 触发后，报告会以 `report_type=market_review` 写入历史库；你可直接查詢 `/api/v1/history` 或 `/api/v1/history/{record_id}` 獲取历史 Markdown，避免再次触发分析重算。
> 说明：该端点若傳回 `task_id`，WebUI 会轮询 `GET /api/v1/analysis/status/{task_id}` 展示狀態。狀態为 `completed` 时给出完成提示（报告已生成并按配置推送），狀態为 `failed` 时在前端錯誤区域顯示 `error` 原因。

> 相容性审计证据：
> - 官方来源：LiteLLM OpenAI-compatible provider 文档 <https://docs.litellm.ai/docs/providers/openai_compatible>；OpenAI Chat API 文档 <https://platform.openai.com/docs/api-reference/chat/create>；DeepSeek API 文档 <https://api-docs.deepseek.com/>。
> - 依賴版本：项目約束为 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`（见 `requirements.txt`），以上相容语义迴歸測試在该版本窗口内執行。
> - 可复核測試：
>   - `tests/test_llm_channel_config.py`（配置源優先级与 provider/base url 映射）
>   - `tests/test_market_review_runtime.py`（`build_market_review_runtime` 复用装配路徑）
>   - `tests/test_analysis_api_contract.py`（`/api/v1/analysis/market-review` 合约与工作狀態鏈路）
> - 回滚/回退：若新路徑有議題，可先恢復历史 `LITELLM_MODEL`、`LITELLM_FALLBACK_MODELS` 与 legacy `GEMINI_*` / `OPENAI_*` / `ANTHROPIC_*` / `DEEPSEEK_*`，或通过桌面端備份或已啟用管理员鉴权的 Web 端 `POST /api/v1/system/config/import` 回滚并重啟；在執行时級別可暂时清空 `LITELLM_CONFIG` / `LLM_CHANNELS` 触发 legacy 回退。

> 进度流说明：`GET /api/v1/analysis/tasks/stream` 除 `task_created / task_started / task_completed / task_failed` 外，新增 `task_progress` 事件。普通分析鏈路会在“行情准备 / 新闻检索 / 上下文整理 / LLM 生成 / 报告保存”等阶段持续更新 `progress` 与 `message`。LiteLLM 流式傳回仅在服務端累积完整文本，最終 JSON 解析成功后才会持久化历史报告；若流式在首个 chunk 前不可用，会自动回退到原非流式呼叫；若已产生部分 chunk 后失败，系統先嘗試同模型非流式重試，失败后再按既有主模型->备用模型顺序繼續嘗試。  
> 如果工作进度回调例外，主鏈路不会中断，系統会提升警報为 warning 級別并在服務端日誌中輸出完整例外，便于排查 SSE 推送断点。
>  
> 说明：该特性属于執行时 SSE 与回退鏈路细节，優先记录于完整指南（`full-guide*.md`），不在 `README.md` 中展开詳細行为分支。

**呼叫示例**：
```bash
# 健康檢查
curl http://127.0.0.1:8000/api/health

# 触发分析（A股）
curl -X POST http://127.0.0.1:8000/api/v1/analysis/analyze \
  -H 'Content-Type: application/json' \
  -d '{"stock_code": "600519"}'

# 透传策略（可選）
curl -X POST http://127.0.0.1:8000/api/v1/analysis/analyze \
  -H 'Content-Type: application/json' \
  -d '{"stock_code": "600519", "skills": ["bull_trend", "growth_quality"]}'

# 查詢工作狀態
curl http://127.0.0.1:8000/api/v1/analysis/status/<task_id>

# 查詢今日 LLM 用量
curl "http://127.0.0.1:8000/api/v1/usage/summary?period=today"

# 触发回测（全部股票）
curl -X POST http://127.0.0.1:8000/api/v1/backtest/run \
  -H 'Content-Type: application/json' \
  -d '{"force": false}'

# 触发回测（指定股票）
curl -X POST http://127.0.0.1:8000/api/v1/backtest/run \
  -H 'Content-Type: application/json' \
  -d '{"code": "600519", "force": false}'

# 查詢整体回测表现
curl http://127.0.0.1:8000/api/v1/backtest/performance

# 查詢单股回测表现
curl http://127.0.0.1:8000/api/v1/backtest/performance/600519

# 分页查詢回测结果
curl "http://127.0.0.1:8000/api/v1/backtest/results?page=1&limit=20"
```

### 自定义配置

修改預設端口或允許局域网訪問：

```bash
python main.py --serve-only --host 0.0.0.0 --port 8888
```

### 支援的股票代碼格式

| 类型 | 格式 | 示例 |
|------|------|------|
| A股 | 6位数字 | `600519`、`000001`、`300750` |
| 北交所 | 8/4/92 开头 6 位，支援 `BJ` 前綴或 `.BJ` 后缀 | `920748`、`BJ920493`、`920493.BJ` |
| 港股 | hk + 5位数字 | `hk00700`、`hk09988` |
| 美股 | 1-5 字母（可選 .X 后缀） | `AAPL`、`TSLA`、`BRK.B` |
| 美股指數 | SPX/DJI/IXIC 等 | `SPX`、`DJI`、`NASDAQ`、`VIX` |

### 注意事项

- 浏览器訪問：`http://127.0.0.1:8000`（或您配置的端口）
- 在云服務器上部署后，不知道浏览器该輸入什么地址？请看 [云服務器 Web 界面訪問指南](deploy-webui-cloud.md)
- 分析完成后自动推送通知到配置的渠道
- 此功能在 GitHub Actions 環境中会自动禁用
- 另见 [openclaw Skill 集成指南](openclaw-skill-integration.md)

---

## 常见議題

### Q: 推送訊息被截斷？
A: 企业微信/飞书有訊息长度限制，系統已自动分段发送。如需完整内容，可配置飞书云文档功能。

### Q: 數據獲取失败？
A: AkShare 使用爬虫機制，可能被暫時限流。系統已配置重試機制，一般等待几分钟后重試即可。

### Q: 如何添加自选股？
A: 修改 `STOCK_LIST` 環境變數，多个代碼用逗号分隔。

### Q: GitHub Actions 没有執行？
A: 檢查是否启用了 Actions，以及 cron 表达式是否正确（注意是 UTC 时间）。

---

更多議題请 [提交 Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues)

## Agent 工具數據快取与持久化

- `get_daily_history` 会先嘗試复用本機 `stock_daily` 日线快取；快取新鲜且至少覆盖首页預設的 30 条记录时，不再重复請求外部數據源。
- 当 Agent 請求的天数多于本機快取记录数时，工具会傳回實際可用记录，并通过 `partial_cache=true`、`requested_days`、`actual_records` 标明这是部分快取命中。
- 快取缺失或过期时，工具仍会按原邏輯从數據源獲取日线數據；獲取成功后会 best-effort 写回 `stock_daily`，保存失败不会阻断 Agent 回复。
- `search_stock_news` 与 `search_comprehensive_intel` 成功傳回后会 best-effort 写入 `news_intel`，复用现有 URL / fallback key 去重邏輯。
- `get_realtime_quote` 不复用 `stock_daily` 作为实时行情快取，也不会把盘中实时行情写入日线表；如需实时行情快取，应单独設計实时行情存储。

## Agent 事件警報監控

`AGENT_EVENT_MONITOR_ENABLED=true` 后，schedule 模式会按 `AGENT_EVENT_MONITOR_INTERVAL_MINUTES` 執行警報 worker。worker 每轮讀取 Alert API 建立并启用的持久化規則，同时繼續相容 `AGENT_EVENT_ALERT_RULES_JSON` 中的 legacy 規則；触发后仍发送到现有通知渠道。Alert API / Web 持久化規則支援实时价、漲跌幅、成交量和日线技术指標；legacy JSON 仍仅支援三类基礎規則。

> 相容与迁移说明：本节记录当前事件警報規則（含 `price_change_percent`）執行时行为，未变更模型名、provider、Base URL、LiteLLM、`OPENAI_*`、`DEEPSEEK_*`、`GEMINI_*` 等外部模型/API 配置语义。legacy JSON 不会被自动迁移、刪除或改写；若需回退，刪除或關閉 `AGENT_EVENT_MONITOR_ENABLED` 即可停止后台警報 worker。

| `alert_type` | 方向欄位 | 閾值欄位 | 说明 |
| --- | --- | --- | --- |
| `price_cross` | `above` / `below` | `price` | 当前价上破或下破指定价格 |
| `price_change_percent` | `up` / `down` | `change_pct` | 漲跌幅达到指定百分比 |
| `volume_spike` | - | `multiplier` | 最新成交量超过近 20 日均量的指定倍数 |
| `ma_price_cross` | `above` / `below` | `window` | 日线 close 相對 MA(window) 边缘上穿或下穿 |
| `rsi_threshold` | `above` / `below` | `period`、`threshold` | RSI 边缘上穿或下穿閾值 |
| `macd_cross` | `bullish_cross` / `bearish_cross` | `fast_period`、`slow_period`、`signal_period` | DIF/DEA 边缘金叉或死叉 |
| `kdj_cross` | `bullish_cross` / `bearish_cross` | `period`、`k_period`、`d_period` | K/D 边缘金叉或死叉 |
| `cci_threshold` | `above` / `below` | `period`、`threshold` | CCI 边缘上穿或下穿閾值 |

示例：

```env
AGENT_EVENT_MONITOR_ENABLED=true
AGENT_EVENT_MONITOR_INTERVAL_MINUTES=5
AGENT_EVENT_ALERT_RULES_JSON=[{"stock_code":"600519","alert_type":"price_cross","direction":"above","price":1800},{"stock_code":"300750","alert_type":"price_change_percent","direction":"down","change_pct":3.0},{"stock_code":"000858","alert_type":"volume_spike","multiplier":2.5}]
```

worker 会把 `triggered`、`skipped`、`degraded`、`failed` 写入 `alert_triggers` 作为評估历史；正常未触发不写历史。真实触发后会把每个通知渠道的 attempt 写入 `alert_notifications`，并为 Alert API 建立的持久化規則写入 `alert_cooldowns` 业务冷却狀態；若讀取持久化冷却失败，worker 会暫時使用程式内 fingerprint 防止 DB 例外期间重复推送。legacy `AGENT_EVENT_ALERT_RULES_JSON` 規則繼續使用程式内 fingerprint 抑制，不写持久化冷却；通知基礎设施的 `notification_noise.py` 降噪仍独立生效。Web 規則列表使用后端傳回的 `cooldown_active` 判斷冷却狀態，避免浏览器本機时区解析影响展示。

技术指標規則只使用日线 close 的边缘触发，partial bar 處理是服務器本機时区 + 16:00 的启发式，不做市场日历精確判定。WebUI 的“警報”页面可以管理持久化規則、執行一次性 dry-run 測試，并查看触发历史、通知嘗試结果和只读冷却狀態；詳細邊界见 [实时警報中心](alerts.md)。

## 持倉管理说明

### `/portfolio` 页面可做什么

- 查看全量持倉或切換到单个账户视角。
- 在 `fifo` / `avg` 两种成本法之间切換，查看快照 KPI、風險摘要和 Top Positions 集中度图表。
- 直接在 Web 页面新增账户，或录入交易、现金流水、公司行动等事件。
- 通过 CSV 匯入持倉记录，支援先 `dry_run` 预览，再决定是否正式写入。
- 在事件列表中按账户、日期、方向、代碼等條件篩選，并对单账户事件做刪除修正。

### 相關介面

| 介面 | 方法 | 说明 |
|------|------|------|
| `/api/v1/portfolio/snapshot` | GET | 查詢持倉快照 |
| `/api/v1/portfolio/risk` | GET | 查詢風險摘要 |
| `/api/v1/portfolio/trades` | GET | 分页查詢交易记录 |
| `/api/v1/portfolio/cash-ledger` | GET | 分页查詢现金流水 |
| `/api/v1/portfolio/corporate-actions` | GET | 分页查詢公司行动 |
| `/api/v1/portfolio/imports/csv/brokers` | GET | 查詢内建 CSV 券商解析器 |
| `/api/v1/portfolio/fx/refresh` | POST | 手动刷新汇率快取 |
| `/api/v1/portfolio/trades/{trade_id}` | DELETE | 刪除交易记录 |
| `/api/v1/portfolio/cash-ledger/{entry_id}` | DELETE | 刪除现金流水 |
| `/api/v1/portfolio/corporate-actions/{action_id}` | DELETE | 刪除公司行动 |

> 查詢类介面统一支援 `account_id`、`date_from`、`date_to`、`page`、`page_size` 等常见篩選參數；事件列表会傳回统一的 `items`、`total`、`page`、`page_size` 结构。

### 使用行为说明

- CSV 匯入内建 `huatai`、`citic`、`cmb` 解析器；若券商列表介面失败，Web 端会自动回退到这些内建选项。
- 匯入流程会先把 CSV 解析成標準化记录，再逐条提交到持倉账本；遇到忙碌行会计入 `failed_count`，不会因为单行冲突让整批請求整体失败。
- 交易去重優先使用账户内唯一的 `trade_uid`，缺失时回退到基于日期、代碼、方向、数量、价格、费用、税费、币种的確定性哈希。
- 賣出会先校验可用数量，超卖傳回 `409 portfolio_oversell`；並行写入冲突时可能傳回 `409 portfolio_busy`。
- 持倉快照的 `positions[]` 会傳回 `price_source`、`price_date`、`price_stale`、`price_available` 等价格元資訊；当天快照会先嘗試实时行情，实时价不可用或非正值时再回退到 `as_of` 当天或之前最近的历史收盤价，历史 `as_of` 快照不会拉取实时价，也不会再把成本价静默当作现价；缺价持倉会标记 `price_available=false` 并从市值与未實現盈亏汇总中排除。
- 汇率刷新会先嘗試在线源；若在线獲取失败，则回退到最近一次快取并标记 `is_stale=true`，避免快照和風險页整体不可用。
- 当 `PORTFOLIO_FX_UPDATE_ENABLED=false` 时，手动刷新介面会明確傳回“在线刷新已禁用”，页面不会误导为“当前没有可刷新的汇率对”。
- 風險摘要包含集中度、回撤、止损接近度等資訊；`sector_concentration` 会優先嘗試按板塊归类，失败时降級到 `UNCLASSIFIED`，不会阻断風險结果傳回。

### Agent 讀取持倉

- Agent 可通过 `get_portfolio_snapshot` 獲取面向账户的紧凑持倉摘要，預設包含精简風險块，适合控制 Token 开销。
- 可選參數包括 `account_id`、`cost_method`、`as_of`、`include_positions`、`include_risk`。
- 若風險块生成失败，快照仍会傳回；若当前環境未启用持倉模組，工具会傳回结构化 `not_supported`。
