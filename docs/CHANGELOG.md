# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

> For user-friendly release highlights, see the [GitHub Releases](https://github.com/ZhuLinsen/daily_stock_analysis/releases) page.

## [Unreleased]

<!-- 新条目格式：- [类型] 描述（类型取值：新功能/改进/修复/文档/測試/chore）-->
<!-- 每条独立一行追加到本段末尾，無需分類标题，合併时冲突最小 -->
- [修复] 抽出 LiteLLM 生成參數適配层，对严格 temperature 模型按請求暫時固定或省略參數，避免 GPT-5 / o 系列与 Kimi K2.6 拒絕預設温度請求。
- [改进] LiteLLM 參數錯誤支援一次請求内自动修正重試，并在成功后程式内快取策略，降低新模型參數相容議題的人工配置成本。
- [文档] 补充 Issue #1316 參數自愈改动的外部相容依据、執行时配置清理邊界与回滚证据；并在 `tests/test_system_config_service.py` 增加清理路徑下 `LLM_TEMPERATURE` 保持不变的迴歸用例。
- [文档] 补充严格 temperature 相容语义的官方来源、執行时依賴約束与 `LLM_TEMPERATURE` 回退/不回写路徑说明。
- [改进] 警報中心 P2 新增后台評估 worker，schedule 模式可同时評估持久化 active rules 与 legacy JSON 規則，并记录 `triggered` / `skipped` / `degraded` / `failed` 最小評估历史。
- [修复] 统一 Windows 桌面安裝包与自动更新元數據文件名，避免 Release 中出现重复安裝包并阻断 `latest.yml` 指向不存在附件。
- [修复] 桌面端啟動 WebUI 时为入口页增加 no-cache 回應头和版本化 cache-busting URL，避免安裝新版后 Electron 繼續复用旧 WebUI 快取。
- [文档] 扩展 Web 设置页帮助資訊，补充 Agent 模型、LiteLLM fallback/config/temperature 与 LLM 渠道编辑器欄位说明。
- [新功能] 新增 Finnhub / AlphaVantage 美股數據源適配器，扩展美股日线 failover 链至 Finnhub(P2) -> AlphaVantage(P3) -> Yfinance(P4) -> Longbridge(P5)。
- [修复] AlphaVantage 適配器在 newest-first 原始數據下 pct_chg 计算錯誤：改为先按日期升序排序再计算漲跌幅。
- [修复] 美股日线路由未包含 Finnhub / AlphaVantage：扩展 `get_daily_data()` 美股分支的 source_order 以覆盖新增數據源。
- [文档] 新增小白客户端安裝与配置指南，说明桌面客户端下載、基礎模型配置、新闻源配置和常见議題。
- [新功能] Web 首页個股分析支援选择策略。
- [新功能] 新增热点题材、事件驱动、成长质量和预期重估策略。
- [新功能] Web 新增警報中心 MVP，支援现有三类警報規則的建立、列表、启停、刪除、dry-run 測試和触发历史查看。
- [新功能] 警報中心 P4 记录真实通知嘗試结果，并为持久化規則新增可查詢的业务冷却狀態。
- [修复] 持倉快照在当天刷新时優先使用实时行情重算当前价、市值与未實現盈亏，避免复用旧收盤价导致页面刷新后盈亏不变。
- [新功能] 警報中心 P5 支援 MA、RSI、MACD、KDJ、CCI 日线技术指標規則，并复用现有触发历史、通知结果和持久化冷却鏈路。

## [3.17.1] - 2026-05-16

### 發佈亮点

- fix: 桌面端 Windows / macOS 打包脚本显式關閉 electron-builder 自动發佈，避免 tag 构建时因缺少 `GH_TOKEN` 在本機打包完成后失败；Release workflow 繼續负责上傳和發佈产物。

### What's Changed

- fix: Add `--publish never` to the Windows and macOS Electron packaging scripts so tag builds only create local artifacts and GitHub Actions handles release upload/publish.

## [3.17.0] - 2026-05-16

### 發佈亮点

- feat: 新增 Alert API MVP，支援警報規則 CRUD、启停、一次性測試以及触发/通知结果查詢，首版覆盖 `price_cross` / `price_change_percent` / `volume_spike` 并保持 legacy 配置相容。
- feat: 通知网关新增 ntfy 与 Gotify 一等渠道，并补齐通知降噪、静态渠道隔離、診斷、Web 測試和 GitHub Actions env 对照校验。
- feat: Windows 桌面安裝版接入自动更新安裝鏈路，支援后台下載、确认重啟安裝、執行时文件備份/恢復和發佈产物元數據校验。
- improve: 大盤复盘新增概念排行、人气股、漲停池等底层數據源，支援指數漲跌颜色语义配置，并将复盘结果写入历史记录。
- improve: Web 设置页支援 `.env` 配置備份匯入/匯出和通知/Agent 区域局部錯誤兜底；报告新增 `REPORT_SHOW_LLM_MODEL` 开关控制模型資訊展示。
- improve: Docker 啟動入口自动修复挂载目錄權限并在日誌目錄不可写时降級到控制台，减少普通部署的手动修复步骤。
- fix: 數據源缺凭据或連線失败时更温和降級，Longbridge / Pytdx 加入冷却，資金流缺失时避免輸出高置信買入结论。
- fix: 分析与报告鏈路相容 OpenAI-compatible `content_blocks` 回應，归一策略价格欄位，并修复大盤复盘滚动和历史记录丢失議題。
- docs: 补齐通知、警報中心、桌面打包、README / 指南和 PR title 治理说明，明確多处配置相容邊界与回滚路徑。
- test: 增加 Alert API、通知降噪/路由、Docker entrypoint、數據源预取、桌面更新鏈路和分析历史等迴歸覆盖。

### What's Changed

- feat: Add an Alert API MVP with rule CRUD, enable/disable, one-shot testing, trigger history, notification results, and legacy config compatibility.
- feat: Promote ntfy and Gotify to first-class notification channels with Web tests, routing, Actions integration, diagnostics, and noise control.
- feat: Add the Windows desktop auto-update install flow with runtime state backup/restore and release artifact metadata verification.
- improve: Extend market review data sources, add configurable index color semantics, and persist market review results into analysis history.
- improve: Add Web `.env` backup import/export, local settings panel error boundaries, and a report model visibility toggle.
- improve: Harden Docker startup by repairing mounted directory permissions and falling back to console logging when mounted logs are not writable.
- fix: Cool down unavailable optional fetchers, reduce noisy Longbridge/Pytdx retries, and downgrade buy advice when capital flow data is missing.
- fix: Handle OpenAI-compatible `content_blocks`, normalize strategy price fields, and recover market review scrolling/history behavior.
- docs/tests: Update notification, alert, desktop packaging, README/guide, and governance docs; add focused regression coverage for the new release paths.

## [3.16.0] - 2026-05-10

### 發佈亮点

- feat: Web 首页新增“大盤复盘”触发入口、工作轮询与完成后报告直出；首次啟動配置狀態可提示缺口并引导到系統设置。
- feat: 新增通知路由策略，支援按 report、alert、system_error 将通知收窄到指定渠道；Web 设置页支援通知渠道一键測試。
- feat: 系統设置页新增配置项帮助入口与多语言帮助文案基礎设施，首批覆盖自选股、LLM 主模型、LLM 渠道、飞书 Webhook 与 WebUI 监听地址。
- improve: 大盤复盘 API、CLI、Bot 共用 `build_market_review_runtime` 装配路徑，补齐 `litellm_model` / `llm_model_list` 与 legacy key 回退说明。
- improve: 個股报告操作建议结合支撑/压力、量能、筹码与主力資金流校准，减少買入/賣出剧烈切換，并补强 Agent 决策兜底。
- improve: Docker 镜像支援非 root 使用者執行，LiteLLM 依賴約束放宽到后续安全 1.x 修复版本。
- fix: 修正 LLM 渠道測試中 `Model disabled`、provider blocked 等錯誤分類，避免被误报为網路例外。
- fix: 港股日线略過不支援港股的内置历史數據源；北交所 `BJ` 前綴与 `.BJ` 后缀代碼校验保持一致。
- fix: Web 大盤复盘按钮可观测性、Windows fallback 锁程式探测和催化线索展示更稳健。
- docs: 新增文档中心与配置帮助维护说明，清理 README、完整指南与配置指南中的暫時 PR/文档同步说明。

### What's Changed

- feat: Add a Web home market-review trigger with task polling and inline report display; setup status now points users to missing configuration.
- feat: Add notification routing by report, alert, and system_error; add one-click notification channel testing in Web settings.
- feat: Add settings field help infrastructure with multilingual help text for the first batch of core configuration fields.
- improve: Share `build_market_review_runtime` across API, CLI, and Bot market review paths; document `litellm_model` / `llm_model_list` and legacy key fallback behavior.
- improve: Calibrate stock advice with support/resistance, volume, chips, and main-force capital flow; strengthen Agent decision fallback behavior.
- improve: Run Docker images as a non-root user and relax LiteLLM constraints to allow safe future 1.x fixes.
- fix: Classify `Model disabled`, provider blocked, and related LLM channel test errors more accurately instead of reporting them as generic network failures.
- fix: Avoid unsupported built-in historical providers for Hong Kong daily data; align Beijing Stock Exchange `BJ` prefix and `.BJ` suffix validation.
- fix: Improve Web market-review observability, Windows fallback lock probing, and market catalyst snippet rendering.
- docs: Add the documentation index and settings-help maintenance guide; remove temporary PR/doc-sync notes from README and user-facing guides.

## [3.15.0] - 2026-05-05

### 發佈亮点

- LLM 渠道配置体验繼續升級：新增 Anspire OpenAI-compatible 网关接入，并补齐常用服務商预设、官方来源、能力標籤、配置注意事项和 GitHub Actions 显式映射。
- Web LLM 配置检测更可診斷：细分錯誤 reason，并支援使用者显式触发 JSON、tools、vision、stream 執行时 smoke。
- LLM 執行时配置清理更稳健：只清理托管 provider 的失效執行时选择，并保留 `cohere/*`、`google/*`、`xai/*` 等直连 provider 相容语义。
- 通知与 Bot 狀態可观测性增强：自定义 Webhook 支援 JSON body 模板，Bot `/status` 展示更完整的 LLM、Agent 与通知渠道狀態。
- 大盤复盘、实时警報、Agent weak 兜底和持倉估值繼續补强，降低預設值覆盖、缺价污染和配置排障成本。

### 新功能

- 支援 `ANSPIRE_API_KEYS` 預設接入 Anspire OpenAI-compatible 大模型网关，并在 LLM 渠道编辑器补充 Anspire Open 预设。
- 自定义 Webhook 支援 `CUSTOM_WEBHOOK_BODY_TEMPLATE` JSON body 模板，便于適配 AstrBot、NapCat 和自建推送服務。
- 大盤复盘结构化区块新增大盤红绿灯结论，基于盘面温度輸出 green/yellow/red、核心原因和操作建议。
- EventMonitor 支援 `price_change_percent` 漲跌幅閾值規則，可按上涨或下跌方向触发实时警報。
- Web LLM 渠道编辑器新增常用服務商配置模板与预设，覆盖 MiniMax、火山方舟、OpenAI、Claude、Gemini、Kimi、Qwen、GLM、豆包等入口。

### 改进

- Web LLM 配置检测补充细分錯誤分類，并新增显式触发的 JSON/tools/vision/stream 執行时 smoke；預設測試和保存流程不变，检测结果仅作为当前配置的一次 best-effort 診斷。
- Bot `/status` 展示统一 LLM 主模型、Agent 模型、渠道模式、YAML 配置和更多通知渠道狀態。
- Web LLM 渠道编辑器展示 provider 能力標籤、官方来源链接和配置注意事项提示；这些標籤仅用于配置參考，不代表執行时能力已驗證通过。
- 抽出 Web LLM provider preset 单一模板數據源，保持现有配置保存语义不变。
- 补齐 LLM provider channel 在 GitHub Actions 中的显式映射，并同步 `.env` 示例与配置文档。

### 修复

- Agent weak 完整性兜底在模型缺少評分、趨勢、操作建议或 dashboard 關鍵块时優先保留本機趨勢分析结果，并只补齐真正缺失的仪表盘欄位，避免首页評分被預設 50 覆盖。
- 统一持倉快照輸出现价、市值、浮盈亏、收益率与价格元資訊，避免缺价或 stale 价格污染持倉估值。
- LLM 渠道測試补充结构化診斷与设置页排障提示，便于定位 provider、模型、Base URL 和鉴权配置議題。
- 明確 runtime 清理相容邊界：仅对托管 provider（`gemini`、`vertex_ai`、`anthropic`、`openai`、`deepseek`）触发保存前失效值清理，`cohere/*`、`google/*`、`xai/*` 直连值按 legacy 相容路徑保留，不做无提示迁移或覆写。
- 将 MiniMax 预设調整为官方 OpenAI-compatible Base URL 和当前模型示例，并补充 MiniMax、火山方舟、LiteLLM 相容来源与回退说明。
- 移除截图识别对 Gemini 3 Vision 模型的过时降級邏輯，預設推断改用当前 Gemini 模型配置。

### 文档

- 完善 LLM provider 配置文档，补充配置方式选择、Actions 變數对照、執行时检测邊界、錯誤 reason 排障和回滚路徑（#1180）。
- 补充 LLM 渠道编辑器的官方来源、依賴相容窗口、保存时的執行时模型清理規則，以及旧配置回退路徑说明。
- 为 `cohere/*`、`google/*`、`xai/*` 直连语义补充官方 provider/model 说明、`litellm>=1.80.10,<1.82.7` 相容依据引用，并明確示例模型名仅为配置保留行为说明而非可用性背书。
- 明確 `price_change_percent` 事件警報仅为配置与執行时規則扩展，未变更模型/provider/base URL/LiteLLM 相容语义；回退路徑为關閉/移除 Event Monitor 配置。
- 同步 README、DEPLOY、full-guide、Anspire、AIHubMix 与 SerpAPI 相關说明，统一外链、配置口径和评审一致性说明。

### 測試

- 补齐 AI 配置页与 `task_queue` 的 LLM 執行时清理/同步迴歸证据：恢復渠道模型时保留 fallback、编辑模型列表期间不静默清空執行时选择，渠道无可用模型时清理失效 runtime 引用，并覆盖 legacy key 与 `cohere/*`、`google/*`、`xai/*` 直连 provider 保留语义。
- 覆盖 Web LLM 配置检测的细分錯誤分類，以及 JSON、tools、vision、stream 執行时 smoke 的显式触发路徑。

## [3.14.2] - 2026-04-30

### 發佈亮点

- 大盤复盘扩展到港股，并让 Bot `/market` 与 CLI/调度入口使用一致的交易日过滤语义。
- 问股与 Agent 鏈路增强配置缺失、决策 fallback 和多策略选择体验。
- LLM 与分析报告鏈路提升稳定性：非法 JSON 回應会繼續嘗試备用模型，LiteLLM DEBUG 日誌預設降噪。
- 新增只读首次啟動配置狀態介面，为后续配置向导和 smoke run 奠定基礎。

### 新功能

- 大盤复盘支援港股市场：`MARKET_REVIEW_REGION` 新增 `hk` 选项；`both` 扩展为 A股+港股+美股，并新增港股指數（HSI/HSTECH/HSCEI）复盘鏈路。
- 新增只读首次啟動配置狀態介面 `GET /api/v1/system/config/setup/status`，用于识别 LLM、Agent、自选股、通知和本機存储配置缺口；该介面不会重載執行时、写入 `.env` 或建立資料庫文件。

### 改进

- 问股页面支援组合选择多个 Agent 策略。

### 修复

- Bot `/market` 命令复用 `get_open_markets_today()` / `compute_effective_region()` 做交易日过滤：结果作为 `override_region` 透传给 `run_market_review`；若结果为空字符串则略過复盘并推送“今日相關市场休市”，与 CLI/调度入口行为一致。
- 问股 Agent 在未配置可用 LLM 时保留后端真实錯誤原因并维持 `done.success=false` 失败语义，避免前端把配置缺失误当成成功回答。
- Agent 模式未生成有效决策仪表盘时保留本機趨勢分析的評分、趨勢和操作建议，并将强买/强卖 fallback 归一到相容的 `buy`/`sell` 决策类型，避免首页结果被 `50 / 观望 / 未知` 缺省值覆盖。
- 持倉快照现价缺失时不再静默回退为持倉成本；当天快照優先使用历史收盤价，仅在缺失时使用实时价 fallback，缺价持倉不再污染市值与未實現盈亏汇总，并为持倉明细傳回价格来源、日期、stale 与缺价狀態。
- 分析 Prompt 在注入 `trend_analysis` 前按最終 `trend_status` / `ma_alignment` 清洗互斥理由：空头结构移除看多理由、多头结构移除空头结构風險，并在事件/技术冲突与例外放量（>10 倍）时強制提示“事件先行、技术待确认”与量能降权。
- LLM 傳回非 JSON 回應时同样触发备用模型切換：主模型成功傳回但無法解析 JSON 时，不再立即降級为纯文本 fallback，而是依次嘗試 `LITELLM_FALLBACK_MODELS` 中的备用模型；所有模型均無法傳回合法 JSON 时，再降級为文本 fallback。
- LiteLLM 内部 DEBUG 日誌預設压低到 WARNING，避免流式生成时 token 级日誌污染 `stock_analysis_debug_*.log`；如需排查 LiteLLM 内部细节，可暫時设置 `LITELLM_LOG_LEVEL=DEBUG`（Fixes #1156）。

### 文档

- 补充 LLM 配置指南与 FAQ，明確问股 Agent 对 `LITELLM_CONFIG` / `LLM_CHANNELS` / legacy `GEMINI_*` `OPENAI_*` `ANTHROPIC_*` 的相容優先级、回退路徑与“不静默迁移旧配置”的结论。

### 測試

- 新增 `tests/test_bot_market_command.py`，覆盖 `MARKET_REVIEW_REGION=both` + open markets `{"cn","us"}` / `{"cn","hk"}` 的 `override_region` 透传断言，并覆盖全市场休市略過与關閉交易日檢查路徑；新增 `tests/test_yfinance_hk_indices.py` 覆盖港股指數符号映射与部分/全部失败降級路徑。
- 补齐 `task_queue` 轻量匯入 stub 的股票代碼規範化函數，恢復 `tests/test_task_queue_config_sync.py` 收集与執行。

## [3.14.1] - 2026-04-26
- [測試] 修正大盤复盘 prompt 測試对“明日交易计划”标题的断言，并同步桌面端版本号，恢復發佈 gate。

## [3.14.0] - 2026-04-26

### 發佈亮点

- 📊 **大盤复盘升級为盘后工作台式结构** — A 股复盘固定輸出盘面温度、指數明细、板塊 Top 表、新闻催化、明日交易计划和風險提示，减少纯文字复盘的重复与空泛。
- 🖥️ **桌面端新增 GitHub Release 更新提醒** — Windows/macOS 桌面端啟動后自动检测新版本，也可从设置页手动檢查并跳转下載页。
- 🤖 **Pipeline Agent 數據加载大幅降噪** — K 线工具改为 DB-first 并预热 240 天历史數據，避免同一只股票重复 HTTP 請求。
- 🐳 **Docker 發佈鏈路整理** — 發佈工作流收斂为正式發佈与手动补发两条路徑，官方 Docker Hub 镜像名统一为 `zhulinsen/daily_stock_analysis`。
- 🔧 **LLM 渠道与 DeepSeek V4 配置补强** — GitHub Actions 定时分析补齐多渠道變數透传，DeepSeek 官方渠道预设与示例同步到 V4。
- 🧩 **桌面端静态资源一致性校验** — 打包鏈路和執行时都能更早发现静态资源错配，降低 Release 包白屏排查成本。

### 新功能

- 🏠 **Web 首页历史报告区新增重新分析入口** — 支援基于原始 prompt 重做同一只股票同日期的分析。
- 🖥️ **Windows/macOS 桌面端新增 GitHub Release 更新提醒** — 啟動后自动检测新版本，并支援从设置页手动檢查后跳转下載页。

### 改进

- 📊 **A 股大盤复盘报告改为结构化盘后工作台版式** — 固定輸出盘面温度、指數明细、板塊 Top 表、新闻催化和明日交易计划。
- 🐳 **Docker 發佈工作流收斂** — 更清晰地区分正式發佈与手动补发鏈路，并统一官方 Docker Hub 镜像名为 `zhulinsen/daily_stock_analysis`。
- 🤖 **Agent 日线工具優先复用本機快取** — 同时持久化新獲取的日线与新闻情报，减少重复數據源呼叫。

### 修复

- 🤖 **Pipeline Agent K 线工具 DB-first 加载** — `get_daily_history` / `analyze_trend` / `calculate_ma` / `get_volume_analysis` / `analyze_pattern` 改为優先讀取本機 DB，消除同一只股票 9x5=45 次重复 HTTP 請求（Fixes #1066）。
- 🤖 **Pipeline Agent 執行前按需预热 240 天 K 线历史到 DB** — 正常情况下 K 线工具呼叫無需重复網路請求。
- 🕒 **冻结 `target_date` 并通过 ContextVar 透传到 Pipeline Agent K 线工具執行緒** — 消除跨收盤邊界时间漂移。
- 🪟 **Windows 桌面端后端日誌转抄編碼修复** — 转抄 stdout/stderr 时優先使用 UTF-8，并相容本機代碼页回退，避免中文日誌乱码。
- ⚙️ **GitHub Actions 每日分析工作流补齐 LLM 渠道變數透传** — 支援 `LLM_CHANNELS`、多 Key 与常用 `LLM_<NAME>_*`，避免本機可用的多模型配置在云端定时工作中失效（Fixes #1063, #872）。
- 📈 **历史报告详情介面修正 `change_pct` 取值** — 使用 `is None` 判斷避免把 0.0（平盘）当作缺失值丢弃，移除錯誤的 `change_60d` 兜底，并在缺失时回退到原始实时行情欄位（Fixes #1084）。
- 🔧 **DeepSeek 官方渠道预设与示例配置同步到 V4** — 保留 legacy `deepseek-chat` 預設值并增加废弃提示，同时修正模型发现后旧執行时选择导致保存失败的議題（Fixes #1108, #1109）。
- 🧩 **桌面端打包鏈路新增静态资源一致性檢查** — `scripts/check_static_assets.py` 会在源 `static/` 与 PyInstaller 产物中校验 `index.html` 引用的资源是否真实存在，執行时也会在错配时写入明確日誌，避免重现 Release 包打开后白屏（Refs #1064 / #1065 / #1050）。
- 🧩 **后端 `/assets/*` 改为显式路由托管** — 资源缺失时傳回与請求扩展名匹配的 `text/javascript` / `text/css` 404，减少預設 JSON 錯誤回應带来的排查误导（Refs #1064）。
- 🌙 **`kimi-k2.6` 自动使用固定温度** — 主分析、大盤复盘和 Agent 呼叫该模型时自动使用 `temperature=1.0`，避免模型拒絕預設温度請求（Fixes #1102）。

### 文档

- 🐳 **补充官方 Docker 镜像使用说明** — 增加镜像拉取、`docker run` 用法与 `.env` / 數據目錄映射说明，不再只覆盖 Compose 部署路徑。
- 📨 **修正飞书自定义机器人 Webhook 示例** — `feishu_sender.py` 中的示例改为 interactive card JSON，并补充飞书自動化 Webhook 触发器配置教程。
- 📚 **最佳化根 README 结构** — 保留首页级功能特性、技术栈、快速开始、推送效果、Web、Agent、赞助商和新闻源入口，将细配置、交易纪律和基本面语义收口到完整指南，并将 Docker 徽章指向官方镜像页。
- 🌐 **同步英文与繁中 README 的精简入口结构** — 同时补齐完整指南中的 LLM 用量 API 与持倉管理说明。
- 🤝 **調整 AI 协作与 PR 模板中的 README 维护規則** — 明確 README 非必要不更新，细节優先进入专题文档。

### 測試

- 🧪 **稳定市场复盘相關測試的 LiteLLM stub 行为** — 避免本机安裝的 LiteLLM 在測試收集顺序变化时影响市场复盘单元測試。
- 🧪 **pytest 預設略過前端依賴目錄** — 本機存在 `apps/dsa-web/node_modules` 时不再被后端測試遞歸扫描，避免發佈前 gate 被无关目錄拖慢。

## [3.13.0] - 2026-04-21

### 發佈亮点

- 🌉 **长桥 OpenAPI 數據源接入** — 美股/港股行情優先使用 Longbridge，YFinance / AkShare 自动兜底；未配置时行为不变。
- 📈 **Tushare 港股全鏈路扩展** — 港股日线通过 `hk_daily` 獲取；筹码分布对港股傳回 `None`；换算单位跟随港股口径，不再套用 A 股手/千元規則。
- 🔍 **Anspire Search 语义搜尋接入** — 配置 `ANSPIRE_*` 后即可使用 Anspire Search 獲取实时行情及资讯，未配置时完全透明。
- 🚀 **普通分析鏈路支援 LLM 流式生成** — 首页工作 SSE 新增 `task_progress` 事件，进度更细化；不支援流式的 provider 自动回退到非流式呼叫。
- 🤖 **Web 渠道编辑器支援按需拉取可用模型列表** — `/v1/models` 统一模型发现入口，多选写回 `LLM_{CHANNEL}_MODELS`，拉取失败时保留手动輸入降級。
- 🛡️ **Agent 稳定性与预算护栏全面补强** — `AGENT_MAX_STEPS` 语义统一、技能降級不中断管线、SSE 例外透传、技能加载 warning 日誌补齐。
- 🛠️ **SQLite 写入鏈路原子化** — 批量原子 upsert + WAL + `busy_timeout` + 有限写入重試，显著降低批量分析並行锁竞争。

### 新功能

- 🌉 **集成 Longbridge OpenAPI 作为美股/港股可選數據源**（fixes #981）— 配置 `LONGBRIDGE_*` 后優先使用长桥獲取日线与实时行情，YFinance / AkShare 兜底；未配置时行为与此前一致。联调使用 `tests/longbridge_live_smoke.py`（手动脚本，不参与 pytest 收集）。
- 📈 **Tushare 支援港股日线查詢** — 配置 Tushare 凭证后呼叫 `hk_daily` 介面獲取港股數據；權限不足时拋出例外，与原流程一致。
- 🔍 **集成 Anspire Search 可選语义搜尋后端** — 配置 `ANSPIRE_*` 可使用 Anspire Search 獲取实时行情及新闻资讯；未配置时行为与此前一致。联调使用 `tests/test_anspire_search.py`（手动脚本）。
- 🚀 **普通分析鏈路支援 LiteLLM 流式生成与更细工作进度** — 股票分析在 LLM 阶段優先嘗試 `stream=True` 并在服務端累积 chunk，首页工作 SSE 新增 `task_progress` 事件与更细的 `message/progress` 更新；仅在最終 JSON 解析成功后持久化历史报告；不支援流式的 provider 自动回退到非流式呼叫。
- 🤖 **Web AI 模型配置支援按渠道獲取可用模型列表** — 渠道编辑器支援呼叫 `/v1/models` 拉取可用模型，并以多选方式写回 `LLM_{CHANNEL}_MODELS`；拉取失败时保留手动輸入作为降級路徑。

### 改进

- 🔎 **SerpAPI 正文补抓範圍收斂** — 自然搜尋结果不再逐条同步抓取网页正文；仅对极少数高位且摘要不足的结果做延遲补抓，優先复用 SerpAPI 已傳回的结构化摘要，降低搜尋鏈路尾延遲与慢站点放大風險。
- 🤖 **LLM 接入体验简化** — 面向使用者的 AI 模型接入文案统一为"主模型 / Agent 主模型 / 備選模型 / 模型渠道"，不再把 LiteLLM 当作普通使用者必学概念，现有 `LITELLM_*` / `LLM_CHANNELS` 配置键保持相容。
- 🧠 **IntelAgent 新增公司公告搜尋与主力資金流工具** — 增加上交所/深交所/cninfo 公告搜尋维度与 `get_capital_flow` 工具，修复 Agent 模式下公告和資金流數據经常缺失的議題。
- 📦 **后端股票名称解析優先复用 `stocks.index.json`** — 懒加载快取前端静态索引，纯后端/缺失静态资源場景静默降級回 `STOCK_NAME_MAP` 与原有數據源回退鏈路。
- 📊 **TushareFetcher 港股单位適配** — `get_chip_distribution` 对港股直接傳回 `None`（港股暂不支援筹码分布）；`_normalize_data` 对港股（`hk_daily`）不再做 A 股手→股、千元→元的缩放，与 Tushare 港股欄位语义一致。
- ⏱️ **Agent 超步数錯誤增加 `AGENT_MAX_STEPS` 調整提示** — 帮助使用者自助排查步数限制議題。
- ⚙️ **GitHub Actions 分析工作逾時支援 `vars` 配置** — `daily_analysis.yml` 工作逾時从 repository variables 讀取，無需修改代碼即可調整執行逾時上限（fixes #1014）。

### 修复

- 📣 **大盤复盘鏈路接入 `REPORT_LANGUAGE`** — `REPORT_LANGUAGE=en` 时，A 股/合併复盘的 Prompt、章节标题、模板兜底文案与通知包装标题统一輸出英文，避免英文正文搭配中文标题的混排議題。
- 📈 **EfinanceFetcher 指數開盤价映射相容**（fixes #1043）— `get_main_indices()` 的開盤价映射改为相容 `今开 → 開盤 → open`，修复部分 efinance 版本下指數開盤价被读成缺失值的議題。
- 🤖 **AGENT_MAX_STEPS 语义统一**（fixes #1026）— 在 orchestrator 多 Agent 模式下明確为"各子 Agent 步数上限而非硬覆盖"；TechnicalAgent 等高預設值 Agent 会被封顶，低預設值 Agent 保持原值；使用者主动调高（>10）时统一覆盖所有子 Agent。修复了使用者设置 12 但 TechnicalAgent 仍以預設 6 步執行并报 "Agent exceeded max steps" 的議題。
- 🛡️ **Specialist（Skill）Agent 失败改为优雅降級** — 技能 Agent 失败不再中断整个分析管线，与 intel/risk 保持相同的降級策略。
- 🔧 **MiniMax-M2.7 連線測試修复** — 修复 LLM 通道連線測試在 MiniMax-M2.7 下傳回 "Empty response" 的議題；将 `max_tokens` 上限从 8 提升至 256 以容纳思考过程，并添加 `content_blocks` 格式解析邏輯。
- 📊 **移除 `sentiment_score` 範圍約束**（fixes #942）— 移除 `HistoryItem` 与 `ReportSummary` 回應 Schema 中 `sentiment_score` 的 `ge=0/le=100` 約束，历史库中存储的超範圍值不再触发 Pydantic ValidationError。
- 🖥️ **WebUI 前端资源缺失时发出明確警告** — `webui_frontend.py` 在 `static/index.html` 存在但 `static/assets/` 缺失时发出 warning，避免 CSS/JS 资源缺失导致页面例外变大却无从排查（fixes #944）。
- 🔗 **分析管线可選服務降級初始化** — `StockAnalysisPipeline` 搜尋服務与社交舆情服務任一初始化例外时，记录 warning 并以禁用狀態繼續執行，避免外部依賴抖动阻塞主分析鏈路。
- 🖥️ **桌面端版本展示统一讀取 `package.json`** — 统一讀取 `apps/dsa-desktop/package.json`，移除 preload 中硬編碼的 `0.1.0`，设置页展示真实桌面端版本；修复版本号顯示錯誤（fixes #1048）。
- 🐋 **港股名称獲取失败修复**（fixes #940）— 修复主數據源欄位缺失时無法正确回退到备用欄位獲取港股名称的議題。
- 🔄 **SSE 工作流斷開时 `CancelledError` 正确 re-raise**（fixes #967）— 修复 SSE 流中断时例外被静默吞掉导致故障无日誌可查的議題。
- 🔄 **Agent SSE 清理阶段后台工作例外正确上报**（fixes #969）— 流结束时后台執行器例外现在正确记录并上报，避免錯誤無法感知。
- 🔇 **技能加载例外补充 `logger.warning` 日誌**（fixes #970）— 在 `ask.py`、`skills/aggregator.py`、`skills/router.py` 的静默 except 块补充日誌，確保技能列表为空时有日誌可查。
- 🛠️ **SQLite 写入鏈路原子化**（fixes #878）— `stock_daily(code,date)` 使用批量原子 upsert；文件型 SQLite 連線預設启用 WAL + `busy_timeout` + 有限写入重試；"新增数"改按本次真正插入窗口计算。
- 💰 **多 Agent / 单 Agent 预算护栏语义统一** — 剩余预算低于最小閾值时主动略過并降級；已完成阶段可构建降級报告时傳回 `success=True` 并携带非空内容，否则傳回 `success=False`。
- ⚙️ **GitHub Actions `daily_analysis.yml` 补齐 `REPORT_LANGUAGE` 注入**（fixes #1013）— 修复使用者在 Secrets/Variables 中配置 `REPORT_LANGUAGE` 后不生效的議題。
- 📊 **工作狀態 API 补齐实时价格欄位**（fixes #983）— `GET /api/v1/analysis/status/{task_id}` 从資料庫回填已完成工作时补齐 `current_price` / `change_pct`，修复首页报告股票名旁不顯示实时价格的議題。
- 📅 **非交易日數據傳回最近交易日**（fixes #1009）— 修复非交易日（週末/節假日）筹码分布与板塊排行傳回倒数第二个交易日數據的議題，现在正常傳回最近交易日數據。
- 🔍 **A 股资讯搜尋恢復中文優先** — `search_stock_news()` 在首个 provider 主要傳回英文资讯时繼續嘗試后续引擎，并将同批结果中的中文资讯排到前面；非美股查詢不再預設沿用 Brave 的 `en/US` 区域语言偏好。
- 📨 **飞书群机器人通知支援簽名校验** — 飞书通知现在支援 `FEISHU_WEBHOOK_SECRET` / `FEISHU_WEBHOOK_KEYWORD`；Web 设置与文档明確区分 Webhook 推送模式和 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` 应用模式，降低误配風險。
- ⚡ **LLM 適配层新增 `RateLimitError` 和 `ContextWindowExceeded` 检测** — 识别并處理速率限制与上下文窗口超出錯誤，提升分析鏈路在高负载或长文本場景下的健壮性（fixes #1002）。

### 測試

- 🧪 **TushareFetcher 港股相關单元測試** — 新增 `get_chip_distribution` 筹码分布獲取与 `_normalize_data` 港股/A 股/ETF 单位處理的单元測試，覆盖港股特殊路徑。

### 文档

- 📘 **DEPLOY.md 补充 UI 元素例外变大排查步骤** — 新增重建 Docker 镜像或手动執行 `npm run build` 的排查指南；`deploy-webui-cloud.md` 同步更新。
- 📨 **飞书 Webhook 配置说明补全** — 强调 `FEISHU_WEBHOOK_URL` 是群通知必填项、簽名校验须两端同时启用或關閉、`FEISHU_APP_SECRET` 仅用于应用/Stream Bot 模式；`.env.example` 补充内联注释；同步英文指南。
- 🤝 **FAQ 补充 Ollama 連線失败排障条目（Q12c）** — 覆盖服務未啟動、URL 配置錯誤、模型前綴缺失、模型未下載、遠端防火墙等 5 个檢查点（fixes #854）。
- 🌉 **README 补充长桥數據源使用说明** — 中/英/繁 README 明確长桥"首选 / 兜底 / 未配置不呼叫"邊界；`docs/` 内相對路徑链接修复；`LONGBRIDGE_PRINT_QUOTE_PACKAGES` 配置与代碼及 `.env.example` 对齐。
- 🐋 **Docker 安裝場景版本说明** — 补充最小化文档，明確 Docker 安裝場景下应以 Git tag / 镜像 tag 判斷版本（fixes #1091）。

## [3.12.0] - 2026-04-01

### 發佈亮点

- 📊 **回测页新增"次日驗證"视图** — 可按股票与日期範圍查看 AI 預測 vs 次日實際漲跌，复用历史分析与 1 日回测结果，快速驗證分析準確率。
- 🔧 **LLM 接入体验简化** — 使用者侧文案统一收口为"主模型 / 備選模型 / 模型渠道"，不再把 LiteLLM 当作普通使用者必学概念，现有配置键保持相容。
- 🐳 **Docker / WebUI 執行时稳态补强** — 修复系統设置保存后配置不生效、啟動早期日誌缺失、预构建静态资源复用等議題，降低容器化部署的运维摩擦。
- 🔒 **安全与並行稳定性同步增强** — Discord 入站 Webhook 补齐 Ed25519 验签，修复並行執行时共享狀態未加锁、单股推送模式通知並行复用等議題。
- 🖥️ **桌面端与定时工作细节打磨** — Windows 安裝器支援自选安裝目錄，内置定时调度器感知執行中 SCHEDULE_TIME 变更，断点续传改按市场时区判斷。

### 新功能

- 📊 **回测页新增"次日驗證 / 1 日窗口"视图** — 可按股票代碼与分析日期範圍查看 AI 預測、次日實際漲跌及篩選區間準確率，复用历史分析与 1 日回测结果實現。
- 🏷️ **Web 设置页新增版本資訊卡片** — `apps/dsa-web` 现在会在构建时注入前端包版本与构建时间，系統设置页新增只读"版本資訊"区块，展示 `WebUI 版本 / 构建标识 / 构建时间`；当 `package.json` 仍为占位版本 `0.0.0` 时，会自动回退为构建标识，方便 Docker 重建后快速确认当前静态资源是否已經生效。
- 🪟 **Windows 桌面安裝器支援自选安裝目錄** — 安裝器改为支援在安裝向导中自定义安裝目錄，安裝到非預設盘符后仍沿用现有打包态目錄邏輯在安裝目錄旁读写 `.env`、`data/stock_analysis.db` 和 `logs/desktop.log`，同时保留 `win-unpacked` 免安裝分发方式。安裝器仅支援当前使用者安裝、已禁用管理员提权（`allowElevation: false`），并通过 NSIS `.onVerifyInstDir` 阻止选择系統保护目錄。

### 改进

- 🔎 **SerpAPI 正文补抓範圍收斂** — 自然搜尋结果不再逐条同步抓取网页正文；现在仅对极少数高位且摘要明显不足的结果，在更短逾時预算内做延遲补抓，并優先复用 SerpAPI 已傳回的结构化摘要，降低搜尋鏈路尾延遲与慢站点放大風險。
- 🤖 **LLM 接入体验简化** — 面向使用者的 AI 模型接入文案已统一收口为"主模型 / Agent 主模型 / 備選模型 / 模型渠道 / 進階模型路由配置"；Web 设置页、配置元數據、校验提示与中英文文档不再把 LiteLLM 当作普通使用者預設必学概念，现有 `LITELLM_*` / `LLM_CHANNELS` 配置键仍保持相容。

### 修复

- 🚀 **啟動早期失败时暴露真实根因** — `python main.py` 现在通过 stderr 暴露真实根因，bootstrap 阶段不再向硬編碼 `logs/` 目錄写入文件日誌，文件日誌推迟到 `config.log_dir` 可用后建立，避免健康啟動在非预期路徑残留日誌文件。
- 🐳 **Docker WebUI 執行时優先复用预构建静态资源** — `prepare_webui_frontend_assets()` 现在会先檢查镜像内已有的 `static/index.html` 是否可直接复用；当容器執行时不包含 `apps/dsa-web` 源码目錄且未安裝 `npm` 时，也不会误报"未找到前端项目，無法自动构建"，从而恢復 Docker 部署后的 WebUI 打开能力。
- 🐳 **Docker WebUI 系統设置保存后配置生效** — Docker 場景下 WebUI 保存 `STOCK_LIST`、`SCHEDULE_ENABLED`、`SCHEDULE_TIME`、`SCHEDULE_RUN_IMMEDIATELY`、`RUN_IMMEDIATELY` 后，`Config` 会優先讀取持久化 `.env` 中的新值，避免被容器建立时注入的旧環境變數覆盖。
- 📈 **市场复盘 LLM max_tokens 提升** — 市场复盘生成鏈路将 LLM `max_tokens` 从 `2048` 提升到 `8192`，降低长复盘輸出因 `MAX_TOKENS` 提前截斷导致内容未完成的機率。
- ⏰ **内置定时调度器感知 SCHEDULE_TIME 執行时变更** — 调度器现在会在執行中感知 WebUI 保存后的 `SCHEDULE_TIME` 变化，并在下一轮檢查时重绑 daily job。
- 🪟 **Windows Release 渠道编辑器保留 MiniMax 模型前綴** — 渠道模式下填写 `minimax/<模型名>` 时，后端归一化与 Web 设置页執行时模型列表都会保留该值原样，不再误改写成 `openai/minimax/<模型名>`。
- 🤖 **Discord 入站 Webhook 补齐 Ed25519 验签** — `DiscordPlatform` 现在会基于 `X-Signature-Ed25519`、`X-Signature-Timestamp` 和原始請求体校验 Discord Interaction 簽名；缺失簽名头、公钥格式非法或簽名不匹配时直接拒絕請求，同时对 timestamp 做 ±5 分钟时效窗口校验以防御重放攻击。
- ⚙️ **STOCK_GROUP_N / EMAIL_GROUP_N 配置关系明確化** — 明確与 `STOCK_LIST` 的关系，并在配置校验中对超出 `STOCK_LIST` 的電郵分組给出 warning。
- 🗓️ **断点续传改按市场时区和交易日历判斷**（fixes #880）— 股票數據存在性檢查不再直接使用服務器自然日，而是按 A 股 / 港股 / 美股各自市场时区解析"最新可复用交易日"。
- 📨 **单股推送模式不再並行复用共享通知实例** — `StockAnalysisPipeline.run()` 现在会保留個股分析並行，但把 `SINGLE_STOCK_NOTIFY=true` 下的即时通知挪到结果收集侧串行发送。
- 🔇 **实时行情降級提示收口为单次警報** — 分析主流程獲取股票名称时不再提前触发一次实时行情查詢，只有在全部數據源都不可用时才提示已降級为历史收盤价繼續分析。
- 🔍 **A 股中文资讯搜尋恢復中文優先** — `search_stock_news()` 现在会在首个 provider 主要傳回英文资讯时繼續嘗試后续引擎，并将同批结果中的中文资讯排到前面。
- 🔒 **並行執行时共享狀態补齐统一加锁** — 修复並行執行时共享狀態缺少统一加锁的議題，避免多執行緒場景下的數據竞争。

### 測試

- 🧪 **补充设置页版本資訊迴歸測試** — 新增 Web 设置页版本資訊渲染断言，并覆盖占位版本 `0.0.0` 自动回退为构建标识的邏輯。
- 🧪 **UI 治理与關鍵路徑迴歸补强** — 补充 `SidebarNav`、`ChatPage`、`BacktestPage` 等組件測試，并新增 UI governance 守卫，持续防止交互元素重新引入原生 `title` 属性或旧 `input-terminal` 样式回流。同步更新 smoke / markdown drawer 相關驗證，覆盖主题升級后的關鍵主鏈路。

## [3.11.0] - 2026-03-27

### 發佈亮点

- 🎨 **Web 工作台完成一轮 UI 统一与双主题升級** — 首页、问股、回测、持倉和设置页进一步收口到统一設計 token、輸入表面和狀態表达；新增完整浅色主题，并支援浅色 / 深色一键切換与持久化保存。
- 🤖 **Bot / Agent 能力重新补回主分支** — 恢復 `/history`、`/strategies`、`/research` 等命令，`/ask` 繼續支援多股对比与组合视角；Deep Research、事件監控与 schedule 轮询鏈路重新接回主线能力。
- 🔒 **安全性与執行稳态同步补强** — 修复 `X-Forwarded-For` 限流绕过風險，恢復 LiteLLM 官方 PyPI 安裝路徑，Tushare 初始化不再依賴本機 SDK，降低 Docker、桌面打包和環境重建时的脆弱点。
- 🖥️ **日常使用细节繼續打磨** — 修复首页港股自动补全提交、登录页首屏主题闪烁、历史长股票名重叠，以及 Telegram Markdown 解析失败时整条通知发送中断等議題。

### 新功能

- 🎨 **全新浅色主题与双主题切換上线** — Web 工作台新增完整浅色主题，并支援在侧边栏中一键切換浅色 / 深色模式；主题选择会持久化保存，刷新页面后仍保持当前偏好。此次升級不是局部配色微調，而是对卡片層級、邊界对比、輸入表面、狀態提示和页面背景做了一整套 light theme 重绘。
- 🤖 **补回主分支缺失的 Agent / Bot 能力** — `#648` / `#649` 已重新补回 `main`：Bot 恢復 `/history`、`/strategies`、`/research`，`/ask` 保留多股对比与组合视角；Deep Research 与 Event Monitor 的配置重新在 Web 设置页可见并可编辑，schedule 模式也重新接入事件警報轮询。

### 改进

- 🖥️ **核心页面统一到同一套工作台视觉语言** — `Home / Chat / Backtest / Portfolio / Settings` 进一步收口到共享設計 token、`input-surface` 輸入体系、空态/錯誤态表达和抽屉遮罩语义，减少页面之间的视觉割裂与局部私有样式漂移。
- 💬 **问股交互可达性与反馈增强** — 问股页补强了會話匯出、通知发送、訊息复制、历史刪除与追问上下文提示；AI 回复操作不再过度依賴 hover，触屏设备和小屏場景下也能直接触达關鍵按钮。
- 📊 **回测与持倉页表面和狀態表达繼續標準化** — 回测页篩選控件、布尔狀態、结果表格与汇总卡片统一到共享輸入/狀態原语；持倉页的匯入反馈、汇率刷新提示、空态与警示資訊进一步归口到共享組件，减少页面级重复實現。
- 🧭 **导航与页面壳层协同最佳化** — 侧边栏主题切換、问股完成角标、移动端抽屉遮罩和主内容滚动契约进一步统一，首页、问股和回测在桌面端与移动端的切页体验更稳定。

### 測試

- 🧪 **UI 治理与關鍵路徑迴歸补强** — 补充 `SidebarNav`、`ChatPage`、`BacktestPage` 等組件測試，并新增 UI governance 守卫，持续防止交互元素重新引入原生 `title` 属性或旧 `input-terminal` 样式回流。同步更新 smoke / markdown drawer 相關驗證，覆盖主题升級后的關鍵主鏈路。

### 修复

- 🌗 **Web 首屏預設主题预设为深色** — `apps/dsa-web/index.html` 现在会在 React 挂载前讀取本機保存的主题偏好；若没有已保存值，则立即给 `<html>` 预设 `dark` 并同步 `color-scheme`，避免首页和登录页首屏先闪出浅色主题。
- 🔐 **登录页独立主题层收口** — 登录页輸入框、標籤、切換按钮和按钮文案现在使用独立的 `--login-*` 视觉 token，不再继承全局浅/深主题文字色；即使浏览器快取了浅色主题，登录页仍保持稳定的深色视觉与青色密碼輸入表现，避免密碼圆点和文案落成黑色。
- 🖥️ **首页港股代碼輸入修复** — Web 首页分析輸入框现在可正确接受港股代碼与自动完成选中的港股项，补齐 `00700.HK` / `HK00700` 等格式识别，避免提交时误报“请輸入有效的股票代碼或股票名称”。

- 🔒 **認證限流 X-Forwarded-For 取值修复（CWE-345）**（#841 / #842）— `get_client_ip()` 从取 `X-Forwarded-For` 最左值改为最右值，防止攻击者通过伪造首部旋转限流桶绕过暴力破解保护；仅影响 `TRUST_X_FORWARDED_FOR=true` 且单层可信反向代理的部署場景，多级代理環境需按部署文档評估配置。
- 📦 **恢復 LiteLLM 官方 PyPI 安裝并锁定安全上限** — `requirements.txt` 重新使用 `pip install litellm` 的官方 PyPI 安裝路徑，并在保留历史最低要求 `>=1.80.10` 的同时增加 `<1.82.7` 的安全上限，避免误装已被移除的 `1.82.7` / `1.82.8` 風險版本；Windows 桌面打包脚本也同步回退到標準 `pip install -r requirements.txt` 鏈路，减少特殊下載分支带来的维护成本。
- 📨 **Telegram Markdown 解析失败回退纯文本**（fixes #850）— `src/notification_sender/telegram_sender.py` 现在会在 Telegram 傳回 `HTTP 400` 且包含 `can't parse entities` / Markdown 解析錯誤时，自动去掉 `parse_mode` 后重試纯文本发送，避免 `*ST` 等正文内容直接导致整条通知失败。
- 🔢 **A 股同码实时行情保留交易所提示**（fixes #852）— `DataFetcherManager` 与 `TushareFetcher` 现在会保留 `SZ000001` / `000001.SZ` 这类显式滬深提示，旧版 Tushare 实时行情降級分支不再把深市 `000001` 误判成 `sh000001` 上证指數。
- 🎯 **多 Agent 次优买点不再盲目复制理想买点**（fixes #851）— 当多智能体结果缺少独立 `secondary_buy` 时，仪表盘现在優先展示 `N/A` 而不是把 fallback 值硬拷贝成与 `ideal_buy` 完全相同，减少误导性的双买点展示。
- 🧩 **Tushare 初始化不再强依賴本機 SDK 包** — `TushareFetcher` 现在直接使用内置 HTTP client 訪問 Tushare Pro，不再在啟動阶段先 `import tushare` 才能初始化；修复了 Docker、桌面打包或環境重建后因缺少 `tushare` 包而提前报 `No module named 'tushare'` 的議題，并补充对应迴歸測試。
- ⚙️ **`daily_analysis` 工作流补齐 `DEEPSEEK_API_KEY` 映射** — GitHub Actions 每日分析工作流现在会正确透传 `DEEPSEEK_API_KEY`，避免云端工作配置了密钥却在執行时拿不到对应環境變數。
- 🖥️ **历史列表过长股票名称截斷与悬停展示**（fixes #815）— 历史列表中过长的股票名称, 现在会按字符类型自动截斷（英文15/中文8/混合10字符），預設顯示截斷结果，悬停时展示完整名称；解決 1920x1080 分辨率下股票名称与右侧狀態標籤文字重叠的議題。新增 `stockName.ts` 工具函數并补充对应測試。

### 文档

- 🧾 **README 捐赠入口更新为小红书二维码** — README 及中英文说明中的赞助入口更新为小红书二维码素材，保持展示口径一致。

## [3.10.1] - 2026-03-24

### 新功能

- 🔔 **Web 端分析推送通知开关**（#808）— 首页分析按钮旁新增「推送通知」复选框，預設勾选；取消勾选时本次分析不发送 Telegram/企业微信等推送。API `POST /api/v1/analysis/analyze` 新增 `notify` 欄位（`bool`，預設 `true`），不传时行为与修改前一致，Bot 和定时工作不受影响。

### 改进

- 🖥️ **问股 / 回测页面布局与壳层协同最佳化** — 统一 Chat / Backtest 页面容器、共享 UI 狀態和跟随问答交互路徑，移除部分硬編碼高度限制，让导航框架内的填充与滚动行为更连贯。
- 🎨 **全局视觉与共享組件繼續收斂** — Light theme 引入动态 HSL 阴影体系，统一侧边栏激活态、警報組件对比度和聊天气泡样式，并把部分零散内联样式收口为语义化 CSS 變數，提升一致性与可维护性。

### 修复

- 🖼️ **系統设置智能匯入文件选择恢復** — 修复了“系統设置 > 基礎设置 > 智能匯入”模組中 “选择图片 / 选择文件” 两个按钮点击无回應的議題。
- 🖥️ **移动端滚动与交互層級修复** — 解決主题切換菜单在移动端被主内容遮挡的 z-index 冲突，并恢復首页长报告場景下的正常縱向滚动，不影响其他页面现有滚动行为。
- 🧾 **Markdown 纯文本复制清洗增强** — 改进纯文本匯出演演算法，复制分析报告时会更稳定地清除表格分隔符等 Markdown 痕迹，提升分享和归档内容的纯净度。
- 🧠 **Trading philosophy injection 覆盖 legacy + Agent 全鏈路**（#810）— `GeminiAnalyzer`、单 Agent 模式和 skill-aware Prompt 现在共享同一套策略注入狀態；只有隐式回落到内置預設 `bull_trend` 时才保留旧的趨勢型提示，显式策略选择或自定义預設 skill 不再被偷偷叠加 `MA5>MA10>MA20` 多头基线。
- 🛠️ **后端 CI 依賴安裝鏈路稳态化**（#835）— 拆分 backend gate 阶段、为依賴安裝增加重試，并把 CI 用的 `litellm` 安裝来源調整为更稳定的 GitHub 源，降低依賴解析抖动导致的 backend gate 偶发失败。
- 🪟 **Windows 桌面发版构建恢復 LiteLLM 安裝相容性** — `scripts/build-backend.ps1` 现在会先过滤 `requirements.txt` 中的 LiteLLM GitHub 源包，再下載对应 tag 的 zipball 到本機移除上游可選 `enterprise/` 目錄后安裝，绕过 Windows runner 上 Poetry 构建 wheel 时把目錄误当文件打包导致的失败；同时补上 `pip install` 退出码檢查，避免依賴安裝失败后只在后续 `python-multipart` 校验阶段才暴露成次生报错。

### 測試

- 🧪 **问股 / 回测 / 智能匯入迴歸覆盖补齐** — 同步更新 E2E 冒烟期望，补充 `DashboardStateBlock`、Chat 页、智能匯入文件选择与相關交互迴歸断言，確保近期 UI 調整后的關鍵路徑仍可稳定通过。

## [3.10.0] - 2026-03-24

### 發佈亮点

- 🔎 **自动补全与索引工具扩展到三市场** — 补全索引生成鏈路现在同时覆盖 A 股、港股、美股，配套新增 Tushare 股票列表抓取工具与更完整的静态索引數據，让首页搜尋入口从“能用”走向“更全、更稳”。
- 🖥️ **Dashboard 与报告查看体验繼續收口** — 首页 Dashboard 面板、狀態邊界、字体層級和完整报告表格密度完成一轮统一；报告详情也补齐了 Markdown/纯文本复制与更可靠的按钮交互，减少历史报告查看与分享时的摩擦。
- 🤖 **Agent skill 与市场语义邊界更清晰** — skill bundle、預設策略、回测汇总语义和相容介面进一步收斂；同时分析 Prompt 不再預設写死 A 股上下文，美股和港股分析也能按各自市场規則生成更贴切的内容。
- ⏰ **定时与桌面配置能力更贴近真实使用場景** — 桌面端支援 `.env` 匯入匯出；`python main.py --schedule --stocks ...` 也不再把啟動时股票快照錯誤带入后续计划執行，定时工作会跟随最新保存的 `STOCK_LIST`。
### 新功能

- 💾 **桌面端 `.env` 備份/恢復入口**（#754）— 桌面模式下的系統设置页新增 `匯出 .env` / `匯入 .env` 按钮，可直接備份当前已保存配置，或把備份文件中的键值合併恢復到当前桌面端 `.env`；匯入沿用现有 `config_version` 冲突保护与執行时重載鏈路，不改变现有桌面端便携模式路徑。
- 📊 **Tushare 股票列表獲取工具** — 新增 `scripts/fetch_tushare_stock_list.py`，支援从 Tushare Pro 獲取 A股、港股、美股列表資訊并保存为 CSV，配有分页讀取、智能限流、錯誤處理和进度提示；新增对应使用文档 `docs/TUSHARE_STOCK_LIST_GUIDE.md`。
- 🔎 **索引生成脚本多市场支援** — `generate_index_from_csv.py` 重构为支援 Tushare 和 AkShare 双數據源，同时覆盖 A股、港股、美股三个市场；新增按市场分類的别名映射（A股、港股常见别名，美股常用股票英文缩写）；添加 `--source` 參數切換數據源、`--test` 參數驗證模式；严格过滤美股 DUMMY 记录。
- 🔎 **索引生成脚本增强** — `generate_stock_index.py` 新增 `--test`/`-t` 測試模式和 `--verbose`/`-v` 詳細輸出模式，添加市场分布統計，最佳化 JSON 輸出格式。
- 📋 **首页完整报告支援双模式复制** — 历史报告详情头部新增“复制 Markdown 源码”和“复制纯文本”工具按钮；前者保留原始 Markdown 结构，后者去除常见 Markdown 格式符号，方便分享、归档和跨报告比对。复制按钮文案会跟随 `REPORT_LANGUAGE` 保持中英文一致，避免英文报告页出现中文固定文案。
- 🧩 **個股分析页补齐關聯板塊展示**（#669）— A 股分析写路徑现在会把 `belong_boards` 一次性写入 `fundamental_context` / `fundamental_snapshot`，结构化报告详情同步新增 `belong_boards` 与 `sector_rankings` 欄位，Web 個股分析页首屏可直接展示所属板塊及其是否命中当日板塊漲跌榜；无數據时保持 fail-open 隱藏，不影响现有分析主流程。

### 改进

- 🖥️ **Dashboard 面板统一化（PR7-2）** — 新增 `DashboardPanelHeader` 和 `DashboardStateBlock` 作为历史、报告、资讯、工作和透明度等面板的通用組件；统一了各面板标题層級、加载/空态/錯誤态和 CSS 變數 token。
- 🖥️ **HomePage 狀態邊界收口（PR7-2）** — 引入 `useHomeDashboardState` hook，集中 `stockPoolStore` 狀態选取邏輯，移除 `HomePage` 中重复的本機狀態派生和回调定义。
- 🧭 **Agent skill 统一到单一配置语义** — Multi-Agent runtime、API、Web chat 和配置元數據统一围绕 `skill` 概念收斂；`/api/v1/agent/skills` 成为主发现入口，`AGENT_SKILL_*` 成为主配置面，内置 skill 元數據也开始声明預設启用、排序優先级、market regime tag 等資訊，减少預設策略散落在代碼里的隐式耦合。
- 🔎 **自动补全索引數據更新** — 重新生成 `stocks.index.json`，涵盖 A股、港股、美股三个市场，提升自动补全覆盖率。
- 🧾 **Dashboard 字体与完整报告表格密度微調** — 收斂首页侧栏、空狀態、历史操作区的字体層級，并将完整 Markdown 报告表格 `th/td` 的内边距調整到更紧凑的 4-6px 區間，让資訊密度与现有 Dashboard 视觉节奏更一致。

### 修复

- ⏰ **定时模式不再锁定啟動时 CLI 股票快照** — `python main.py --schedule --stocks ...` 现在不会让后续计划執行沿用啟動时的旧股票列表；定时工作每次触发前都会重新讀取最新保存的 `STOCK_LIST`，確保 WebUI 或 `.env` 更新后的自选股配置能参与后续推送。
- 🌍 **LLM Prompt 按股票市场动态注入上下文** — 分析鏈路不再把市场規則写死成 A 股；系統 Prompt 会根据股票代碼识别 A 股、港股或美股，并注入对应的角色描述与交易規則提示，减少跨市场分析出现口径错位或结论失真的議題。
- 🔎 **美股自动补全复用 ticker 去重** — `generate_index_from_csv.py` 在匯入 Tushare `us_basic` CSV 时会先按 `ts_code` 折叠复用的美股 ticker，優先保留更可能仍在使用的记录，避免 `stocks.index.json` 出现重复 `canonicalCode` 后让 Web 自动补全展示历史名称或提交歧义代碼。
- 🧾 **Web 报告详情复制交互稳定性修复**（#749）— `ReportDetails` 中“原始分析结果 / 分析快照”的复制按钮补齐可点击層級，避免被下方 JSON 内容覆盖；两个面板的复制提示也改为各自独立，不再出现复制一个后两个按钮同时顯示“已复制”的误导反馈。
- 📊 **Agent skill 回测与相容介面语义收斂** — `get_skill_backtest_summary` 现在要求显式传入 `skill_id`，缺失时傳回明確校验提示；倉庫尚未持久化真实 skill 级汇总时会傳回明確的 unsupported/info 回應，并保留 `normalized` 与 `*_pct` 相容欄位，避免沿用 overall 指標误导 Agent 或使用者。
- 🔧 **Skill 預設选择与相容层行为加固** — `allowed-tools` 会繼續仅作为 `SKILL.md` bundle 元數據保留，不再泄露到執行时工具选择；`/api/v1/agent/strategies` 恢復旧 payload 形状；显式传入 `skills: []` 时会清空陈旧上下文；当使用者明確选择策略 skill 时不再偷偷叠加預設 bull-trend，而在 `AGENT_SKILLS` 为空时则统一只回落到单一主預設 skill。

### 測試

- 🧪 **Dashboard 組件測試覆盖率扩展（PR7-2）** — 新增 `ReportNews` 和 `TaskPanel` 測試；对 `HistoryList`、`ReportDetails`、`HomePage`、`useDashboardLifecycle` 和 `stockPoolStore` 增强了断言覆盖，包括刪除回退、移动端抽屉和工作生命周期等場景。
- 🧪 **多市场索引生成測試补齐** — 新增 `tests/test_generate_index_from_csv.py`，覆盖 Tushare/AkShare 双數據源解析、多市场判斷、美股 DUMMY 过滤与重复 ticker 去重等核心路徑。
- 🧪 **關聯板塊写入与 API 契约迴歸** — 新增 `tests/test_pipeline_related_boards.py`，并补充分析历史与分析介面契约測試，確保 `belong_boards` / `sector_rankings` 只做增量扩展且保持 fail-open。
- 🧪 **定时模式股票列表语义迴歸測試** — 新增 `tests/test_main_schedule_mode.py`，覆盖定时模式忽略啟動时 `--stocks` 快照、单次執行仍保留 CLI 股票覆盖的邊界場景。

### 文档

- 📘 **新增 Tushare 股票列表工具文档** — 新增 `docs/TUSHARE_STOCK_LIST_GUIDE.md`，说明股票列表抓取工具的使用方法、數據格式和常见議題。
- 🌍 **补齐定时模式与關聯板塊的双语说明** — `docs/full-guide.md` / `docs/full-guide_EN.md` 现在明確说明 scheduled mode 会在每次執行前重新讀取 `STOCK_LIST`，并同步补充個股關聯板塊展示能力说明，减少配置预期偏差。
- 🧭 **調整 Agent 术语相容文案** — README、双语文档、设置页与问股界面繼續以“策略”作为使用者入口主称呼，同时补充 `skill` 作为内部统一命名，降低迁移期理解成本。

## [3.9.0] - 2026-03-20

### 發佈亮点

- 🤖 **模型鏈路与报告语言更灵活** — Agent 现在可以通过 `AGENT_LITELLM_MODEL` 独立选择模型鏈路，普通分析与 Agent 报告也可通过 `REPORT_LANGUAGE=zh|en` 輸出统一语言，减少“英文内容 + 中文壳子”这类混排議題，并允許团队分别权衡主分析与 Agent 的成本、速度和能力。
- 🔎 **首页分析体验完成一轮闭环最佳化** — 首页新增 A 股自动补全，支援代碼、中文名、拼音和别名检索；同时 Dashboard 狀態收口到统一 store，历史、报告、新闻与 Markdown 抽屉的交互更稳定，“Ask AI” 追问也会優先携带当前报告上下文。
- 💬 **通知与检索能力繼續外扩** — 新增 Slack 一等通知渠道；SearXNG 在未配置自建实例时可以自动发现公共实例并按受控轮询降級；Tavily 时效新闻鏈路修复后，严格时效过滤不再錯誤丢光有效结果。
- 💼 **持倉与市场复盘鏈路更稳** — A 股 market review 可選接入 TickFlow 强化指數与漲跌統計；持倉账本写入改为串行化以缩小並行超卖窗口；汇率刷新入口和禁用态提示也更加清晰，减少使用者误判。

### 新功能

- 🔎 **Web 股票自动补全 MVP** — 首页分析輸入框新增本機索引驱动的自动补全，支援股票代碼、中文名、拼音和别名匹配；选中候选后会提交 canonical code，并透传 `stock_name`、`original_query`、`selection_source` 到分析請求、工作狀態和 SSE 事件；索引加载失败时自动退回旧輸入模式，不阻断原有提交流程。同步补充了静态索引加载器、索引生成脚本和前后端契约測試。分阶段進行开发，第一阶段仅支援 A 股。
- 💬 **Slack 一等通知渠道** — 新增 Slack 原生通知支援，同时支援 Bot Token 和 Incoming Webhook 两种接入方式；同时配置时優先使用 Bot API，確保文本与图片发送到同一频道；Bot Token 模式支援图片上傳（raw body POST，不使用 multipart）；新增 `SLACK_BOT_TOKEN`、`SLACK_CHANNEL_ID`、`SLACK_WEBHOOK_URL` 配置项，GitHub Actions 工作流同步补齐对应 Secrets 传递。
- 🌍 **报告輸出语言可配置**（Issue #758）— 新增 `REPORT_LANGUAGE=zh|en`，預設 `zh`；语言设置会同步注入普通分析与 Agent Prompt，并覆盖 Markdown/Jinja 模板、通知 fallback、历史/API `report_language` 元數據及 Web 报告页固定文案，避免“英文内容 + 中文壳子”的混合輸出。
- 🚀 **Agent 与普通分析模型解耦**（Issue #692）— 新增 `AGENT_LITELLM_MODEL`（留空继承 `LITELLM_MODEL`，无前綴按 `openai/<model>` 归一）；Agent 執行鏈路与 `/api/v1/agent/models` 的 `is_primary/is_fallback` 标记改为基于 Agent 實際模型鏈路；系統配置与啟動期校验补齐 `AGENT_LITELLM_MODEL` 的 `unknown_model/missing_runtime_source` 檢查；Web 设置页新增 Agent 主模型选择并与渠道模式執行时配置同步。
- 🔎 **SearXNG 公共实例自动发现与受控轮询**（#752）— 新增 `SEARXNG_PUBLIC_INSTANCES_ENABLED`，在未配置 `SEARXNG_BASE_URLS` 时預設从 `searx.space` 拉取公共实例列表，并按受控轮询顺序选择实例；同次請求内遇到逾時、連線錯誤、HTTP 非 200 或无效 JSON 会自动切換到下一个实例。已配置自建实例的使用者保持原有優先级与语义不变；`daily_analysis` GitHub Actions 工作流也已支援显式透传该开关并在啟動日誌中展示当前狀態。
- 📈 **TickFlow market review enhancement** (#632) — 新增可選 `TICKFLOW_API_KEY`；配置后，A 股大盤复盘的主要指數行情優先嘗試 TickFlow；若当前 TickFlow 套餐支援标的池查詢，市场漲跌統計也会優先嘗試 TickFlow。失败或權限不足时立即回退到现有 `AkShare / Tushare / efinance` 鏈路；板塊漲跌榜回退顺序保持不变。接入层同时適配了真实 SDK 契约：主指數查詢按单次請求上限分批拉取，并将 TickFlow 傳回的比例型 `change_pct` / `amplitude` 统一轉換为项目内部的百分比口径。

### 改进

- **Dashboard state slice and workspace closure** — moved Home / Dashboard state into `stockPoolStore`, consolidated history selection, report loading, task syncing, polling refresh, and markdown drawer handling under a single state slice.
- **Dashboard panel standardization** — kept the current dashboard layout contract stable while unifying history, report, news, and markdown presentation with shared tokens, standardized states, and bounded in-panel scrolling for the history list.
- **Dashboard-to-chat follow-up bridge** — routed “Ask AI” follow-ups through report-context hydration instead of direct cross-page state coupling, while keeping chat sends usable when enriched history context is still loading.
- 💼 **持倉账本並行写入串行化**（#742）— 持倉源事件写入/刪除现在会在 SQLite 下先獲取串行化写锁，减少並行賣出把超售流水写入账本的窗口；直接持倉写介面在锁竞争时傳回 `409 portfolio_busy`，CSV 匯入保持逐条提交并把 busy 计入 `failed_count`。
- 💱 **持倉页汇率手动刷新入口补齐**（#748）— Web `/portfolio` 页面现在会在“汇率狀態”卡片中展示“刷新汇率”按钮，直接呼叫现有 `POST /api/v1/portfolio/fx/refresh` 介面；刷新后会仅重載快照与風險數據，并以内联摘要反馈“已更新 / 仍 stale / 刷新失败”的结果，减少使用者对 `fxStale` 长时间停留的误解。

### 修复

- 🔎 **Web 自动补全 Enter 提交语义修正** — 股票自动补全在搜尋命中候选时不再預設高亮第一项；候选列表展开但使用者尚未用方向键或鼠标明確选中时，按 Enter 会繼續提交原始輸入，避免手动輸入被第一条候选静默覆盖。
- 🌍 **补齐 `REPORT_LANGUAGE` 啟動解析与历史展示本機化邊界** — `Config` 在啟動时繼續遵循“真实環境變數優先、`.env` 兜底”的既有语义，并在两者冲突时輸出显式警報，减少 `REPORT_LANGUAGE` 来源不清带来的误判；同时 `/api/v1/history/{id}` 英文详情回應会同步本機化 `sentiment_label`，历史 Markdown 也会正确识别英文 `bias_status` 的風險等级 emoji，避免出现 `乐观` 或 `🚨Safe` 这类中英混排/误报展示。
- 📰 **Tavily 时效新闻检索發佈时间映射修复**（#782）— Tavily 在股票新闻和严格时效的情报维度中现在会显式使用 `topic="news"`，并相容 `published_date` / `publishedDate` 两种發佈时间欄位；修复了 Tavily 明明傳回结果却在后续硬过滤阶段被全部记为 `drop_unknown` 丢弃的議題，同时将机构分析、业绩预期、行业分析等分析型维度恢復为宽源搜尋，不再被统一壓縮成新闻模式。
- 💱 **持倉页汇率刷新禁用语义修正**（#772）— 当 `PORTFOLIO_FX_UPDATE_ENABLED=false` 时，`POST /api/v1/portfolio/fx/refresh` 现在会傳回显式 `refresh_enabled=false` 与 `disabled_reason`，Web `/portfolio` 页面会明確提示“汇率在线刷新已被禁用”，不再误报“当前範圍无可刷新的汇率对”。
- 🤖 **Agent timeout and config hardening** — `AGENT_ORCHESTRATOR_TIMEOUT_S` now also protects the legacy single-agent ReAct loop, parallel tool batches stop waiting once the remaining budget is exhausted, and invalid numeric `.env` values fall back to safe defaults with warnings instead of crashing startup.
- 🌐 **CORS wildcard + credentials compatibility** — `CORS_ALLOW_ALL=true` no longer combines `allow_origins=["*"]` with credentialed requests, avoiding browser-side cross-origin failures in demo/development setups.
- 🧭 **Unavailable Agent settings hidden from Web UI** — Deep Research / Event Monitor controls are now treated as compatibility-only metadata in the current branch and are removed from the Settings page to avoid exposing non-functional toggles.

### 文档

- 新增 Ollama 本機模型配置说明，同步更新 `README.md` 与 `docs/README_EN.md`（Fixes #690）
- 完善 Ollama 配置说明：`docs/full-guide.md` / `docs/full-guide_EN.md` 環境變數表与 Note 补充 `OLLAMA_API_BASE`，避免英文使用者误以为 Ollama 不能作为独立配置入口；合併重复的 `OLLAMA_API_BASE` 条目为单一条目
- 明確文档同步治理邊界：补充 `README.md`、专题文档、双语文档与交付说明之间的預設同步規則，减少后续文档漂移

## [3.8.0] - 2026-03-17

### 發佈亮点

- 🎨 **Web 界面完成一轮骨架升級** — 新的 App Shell、侧边导航、主题能力、登录与系統设置流程已經串成统一体验，桌面端加载背景也完成对齐。
- 📈 **分析上下文繼續补强** — 美股新增社交舆情情报，A 股补齐财报与分红结构化上下文，Tushare 新接入筹码分布和行业板塊漲跌數據。
- 🔒 **執行稳定性与配置相容性提升** — 退出登录会立即让旧會話失效，定时啟動相容旧配置，執行中的 `MAX_WORKERS` 調整和新闻时效窗口反馈更清晰。
- 💼 **持倉纠错鏈路更完整** — 超售会被前置拦截，錯誤交易/資金流水/公司行为可以直接刪除回滚，便于修复脏數據。

### 新功能

- 📱 **美股社交舆情情报** — 新增 Reddit / X / Polymarket 社交媒体情绪數據源，为美股分析提供实时社交热度、情绪評分和提及量等补充指標；完全可選，仅在配置 `SOCIAL_SENTIMENT_API_KEY` 后对美股生效。
- 📊 **A 股财报与分红结构化增强**（Issue #710）— `fundamental_context.earnings.data` 新增 `financial_report` 与 `dividend` 欄位；分红统一按“仅现金分红、税前口径”计算，并补充 `ttm_cash_dividend_per_share` 与 `ttm_dividend_yield_pct`；分析/历史 API 的 `details` 追加 `financial_report`、`dividend_metrics` 可選欄位，保持 fail-open 与向后相容。
- 🔍 **接入 Tushare 筹码与行业板塊介面** — 新增筹码分布、行业板塊漲跌數據獲取能力，并统一纳入配置化數據源優先级；預設按上海时间区分盘中/盘后交易日取数，優先使用 Tushare 同花顺介面，必要时降級到东财。
- 🧱 **Web UI 基礎骨架升級** — 重建共享設計令牌与通用組件，新增 App Shell、Theme Provider、侧边导航，并同步調整 Electron 加载背景，为 Web / Desktop 的统一体验打底。
- 🔐 **登录与系統设置流程重做** — 重构 Login、Settings 与 Auth 管理流程，补上显式的認證 setup-state 處理，并让 Web 端与執行时認證配置 API 行为对齐。
- 🧪 **前端迴歸与冒烟覆盖补强** — 新增并扩展登录、首页、聊天、移动端 Shell、设置页、回测入口等關鍵路徑的組件測試与 Playwright smoke coverage。

### 变更

- 🧭 **页面接入新 Shell 布局契约** — Home、Chat、Settings、Backtest 已统一接入新的页面容器、抽屉和滚动约定，降低 UI 迁移期间的页面行为不一致。
- 💾 **设置页狀態同步更稳** — 最佳化草稿保留、直接保存同步与冲突處理，减少模組级保存后前后端配置狀態不一致的議題。
- 🎭 **登录页视觉基线迴歸** — 登录页恢復到既有 `006` 分支的视觉基线，同时保留新的認證狀態邏輯和统一表单交互模型。
- 🏛️ **AI 协作治理资产加固** — 收斂并加强 `AGENTS.md`、`CLAUDE.md`、Copilot 指令和校验脚本的一致性約束，降低治理资产长期漂移風險。

### Added

- **Web UI foundation refresh** — rebuilt shared design tokens and common primitives, introduced the app shell, theme provider, sidebar navigation, and Electron loading background alignment for the upgraded desktop/web experience
- **Settings and auth workflow overhaul** — rebuilt the Login, Settings, and Auth management flows, added explicit auth setup-state handling, and aligned the Web UI with the runtime auth configuration APIs
- **UI regression coverage and smoke checks** — expanded targeted frontend tests and added Playwright smoke coverage for login, home, chat, mobile shell, settings, and backtest entry flows

### Changed

- **Shell-driven page integration** — aligned Home, Chat, Settings, and Backtest with the new shell layout contract so routing, drawer behavior, and page-level scrolling are consistent during the UI migration
- **Settings state consistency** — refined draft preservation, direct-save synchronization, and conflict handling so module-level saves no longer leave the page out of sync with backend config state
- **Login visual baseline** — restored the login page visual treatment to the established `006` branch baseline while keeping the newer auth-state logic and unified form interaction model

### 修复

- ⏰ **定时啟動立即執行相容旧配置**（Issue #726）— `SCHEDULE_RUN_IMMEDIATELY` 未设置时会回退讀取 `RUN_IMMEDIATELY`，修复升級后旧 `.env` 在定时模式下的相容性議題；同时澄清 `.env.example` / README 中两个配置项的适用範圍，并注明 Outlook / Exchange 強制 OAuth2 暂不支援。
- 🧵 **執行期 `MAX_WORKERS` 配置生效与可解释性增强**（#633）— 修复非同步分析隊列未按 `MAX_WORKERS` 同步的議題；新增工作隊列並行 in-place 同步機制（空闲即时生效、繁忙延后），并在设置保存反馈与執行日誌中明確輸出 `profile/max/effective`，减少“參數未生效”误解。
- 🔐 **退出登录立即失效现有會話** — `POST /api/v1/auth/logout` 现在会轮换 session secret，避免旧 cookie 在退出后仍可繼續訪問受保护介面；同浏览器標籤页和並行页面会被同步登出。認證开启时，该介面也不再属于匿名白名单，未登录請求会傳回 `401`，避免匿名請求触发全局 session 失效。
- 🧮 **Tushare 板塊/筹码呼叫限流与跨日快取修复** — 新增的 `trade_cal`、行业板塊排行、筹码分布鏈路统一接入 `_check_rate_limit()`；交易日历快取改为按自然日刷新，避免服務跨天執行后繼續沿用旧交易日判斷取数日期。
- 💼 **持倉超售拦截与錯誤流水恢復**（#718）— `POST /api/v1/portfolio/trades` 现在会在写入前校验可卖数量，超售傳回 `409 portfolio_oversell`；持倉页新增交易 / 資金流水 / 公司行为刪除能力，刪除后会同步失效仓位快取与未来快照，便于从錯誤流水中直接恢復。
- 📧 **電郵中文发件人名編碼**（#708）— 電郵通知现在会对包含中文的 `EMAIL_SENDER_NAME` 自动做 RFC 2047 編碼，并在例外路徑补充 SMTP 連線清理，修复 GitHub Actions / QQ SMTP 下 `'ascii' codec can't encode characters` 导致的发送失败。
- 🐛 **港股 Agent 实时行情去重与快速路由** — 统一 `HK01810` / `1810.HK` / `01810` 等港股代碼归一規則；港股实时行情改为直接走单次 `akshare_hk` 路徑，避免按 A 股 source priority 重复触发同一失败介面；Agent 執行期对显式 `retriable=false` 的工具失败增加短路快取，减少同轮分析中的重复失败呼叫。
- 📰 **新闻时效硬过滤与策略分窗**（#697）— 新增 `NEWS_STRATEGY_PROFILE`（`ultra_short/short/medium/long`）并与 `NEWS_MAX_AGE_DAYS` 统一计算有效窗口；搜尋结果在傳回后執行發佈时间硬过滤（时间未知剔除、超窗剔除、未来仅容忍 1 天），并在历史 fallback 鏈路追加相同約束，避免旧闻再次进入“最新动态/風險警报”。

### 文档

- ☁️ **新增云服務器 Web 界面部署与訪問教程**（Fixes #686）— 补充从云端部署到外部訪問的落地说明，降低遠端自托管门槛。
- 🌍 **补齐英文文档索引与协作文档** — 新增英文文档索引、贡献指南、Bot 命令文档，并补充中英双语 issue / PR 模板，方便中英文协作与外部贡献者理解项目入口。
- 🏷️ **本機化 README 补充 Trendshift badge** — 在多语言 README 中同步补上新版能力入口标识，减少中英文说明面不一致。

## [3.7.0] - 2026-03-15

### 新功能

- 💼 **持倉管理 P0 全功能上线**（#677，对应 Issue #627）
  - **核心账本与快照闭环**：新增账户、交易、现金流水、企业行为、持倉快取、每日快照等核心數據模型与 API 端点；支援 FIFO / AVG 双成本法回放；同日事件顺序固定为 `现金 → 企业行为 → 交易`；持倉快照写入采用原子事务。
  - **券商 CSV 匯入**：支援华泰 / 中信 / 招商首批適配，含列名别名相容；两阶段介面（解析预览 + 确认提交）；`trade_uid` 優先、key-field hash 兜底的幂等去重；前导零股票代碼完整保留。
  - **组合風險报告**：集中度風險（Top Positions + A 股板塊口径）、历史回撤監控（支援回填缺失快照）、止损接近预警；多币种统一换算 CNY 口径；汲取失败时回退最近成功汇率并标记 stale。
  - **Web 持倉页**（`/portfolio`）：组合总览、持倉明细、集中度饼图、風險摘要、全组合 / 单账户切換；手工录入交易 / 資金流水 / 企业行为；内嵌账户建立入口；CSV 解析 + 提交闭环与券商选择器。
  - **Agent 持倉工具**：新增 `get_portfolio_snapshot` 數據工具，預設紧凑摘要，可選持倉明细与風險數據。
  - **事件查詢 API**：新增 `GET /portfolio/trades`、`GET /portfolio/cash-ledger`、`GET /portfolio/corporate-actions`，支援日期过滤与分页。
  - **可扩展 Parser Registry**：应用级共享注册，支援執行时注册新券商；新增 `GET /portfolio/imports/csv/brokers` 发现介面。

- 🎨 **前端設計系統与原子組件库**（#662）
  - 引入渐进式双主题架構（HSL 變數化設計令牌），清理历史 Legacy CSS；重构 Button / Card / Badge / Collapsible / Input / Select 等 20+ 核心組件；新增 `clsx` + `tailwind-merge` 类名合併工具；提升历史记录、LLM 配置等页面可读性。

- ⚡ **分析 API 非同步契约与啟動最佳化**（#656）
  - 規範 `POST /api/v1/analysis/analyze` 非同步請求的傳回契约；最佳化服務啟動辅助邏輯；修复前端报告类型联合定义与后端回應对齐議題。

### 修复

- 🔔 **Discord 環境變數向后相容**（#659）：執行时新增 `DISCORD_CHANNEL_ID` → `DISCORD_MAIN_CHANNEL_ID` 的 fallback 讀取；历史配置使用者無需修改即可恢復 Discord Bot 通知；全部相關文档与 `.env.example` 对齐。
- 🔧 **GitHub Actions Node 24 升級**（#665）：将所有 GitHub 官方 actions 升級至 Node 24 相容版本，消除 CI 日誌中的 Node.js 20 deprecation warning（影响 2026-06-02 強制升級窗口）。
- 📅 **持倉页預設日期本機化**：手工录入表单預設日期改用本機时间（`getFullYear/Month/Date`），修复 UTC-N 时区使用者在当天晚间出现日期偏移的議題。
- 🔁 **CSV 匯入去重邏輯加固**：dedup hash 纳入行序号作为区分因子，確保同欄位合法分笔成交不被误折叠；同时在 `trade_uid` 存在时也持久化 hash，防止混合来源重复写入。

### 变更

- `POST /api/v1/portfolio/trades` 在同账户内 `trade_uid` 冲突时傳回 `409`。
- 持倉風險回應新增 `sector_concentration` 欄位（增量扩展），原有 `concentration` 欄位保持不变。
- 分析 API `analyze` 介面非同步行为契约文档化；前端报告类型联合更新。

### 測試

- 新增持倉核心服務測試（FIFO / AVG 部分賣出、同日事件顺序、重复 `trade_uid` 傳回 409、快照 API 契约）。
- 新增 CSV 匯入幂等性、合法分笔成交不误去重、去重邊界、風險閾值邊界、汇率降級行为測試。
- 新增 Agent `get_portfolio_snapshot` 工具呼叫測試。
- 新增分析 API 非同步契约迴歸測試。

## [3.6.0] - 2026-03-14

### Added
- 📊 **Web UI Design System** — implemented dual-theme architecture and terminal-inspired atomic UI components
- 📊 **UI Components Refactoring** — integrated `clsx` and `tailwind-merge` for robust class composition across Web UI

- 🗑️ **History batch deletion** — Web UI now supports multi-selection and batch deletion of analysis history; added `POST /api/v1/history/batch-delete` endpoint and `ConfirmDialog` component.
- 🔐 **Auth settings API** — new `POST /api/v1/auth/settings` endpoint to enable or disable Web authentication at runtime and set the initial admin password when needed
- openclaw Skill 集成指南 — 新增 [docs/openclaw-skill-integration.md](openclaw-skill-integration.md)，说明如何通过 openclaw Skill 呼叫 DSA API
- ⚙️ **LLM channel protocol/test UX** — `.env` and Web settings now share the same channel shape (`LLM_CHANNELS` + `LLM_<NAME>_PROTOCOL/BASE_URL/API_KEY/MODELS/ENABLED`); settings page adds per-channel connection testing, primary/fallback/vision model selection, and protocol-aware model prefixing
- 🤖 **Agent architecture Phase 0+1** — shared protocols (`AgentContext`, `AgentOpinion`, `StageResult`), extracted `run_agent_loop()` runner, `AGENT_ARCH` switch (`single`/`multi`), config registry entries
- 🔍 **Bot NL routing** — two-layer natural-language routing: cheap regex pre-filter (stock codes + finance keywords) → lightweight LLM intent parsing; controlled by `AGENT_NL_ROUTING=true`; supports multi-stock and strategy extraction
- 💬 **`/ask` multi-stock analysis** — comma or `vs` separated codes (max 5), parallel thread execution with 150s timeout (preserves partial results), Markdown comparison summary table at top
- 📋 **`/history` command** — per-user session isolation via `{platform}_{user_id}:{scope}` format (colon delimiter prevents prefix collision); lists both `/chat` and `/ask` sessions; view detail or clear
- 📊 **`/strategies` command** — lists available strategy YAML files grouped by category (趨勢/形态/反转/框架) with ✅/⬜ activation status
- 🔧 **Backtest summary tools** — `get_strategy_backtest_summary` and `get_stock_backtest_summary` registered as read-only Agent tools
- ⚙️ **Agent auto-detection** — `is_agent_available()` auto-detects from `LITELLM_MODEL`; explicit `AGENT_MODE=true/false` takes full precedence
- 🏗️ **Multi-Agent orchestrator (Phase 2)** — `AgentOrchestrator` with 4 modes (`quick`/`standard`/`full`/`strategy`); drop-in replacement for `AgentExecutor` via `AGENT_ARCH=multi`; `BaseAgent` ABC with tool subset filtering, cached data injection, and structured `AgentOpinion` output
- 🧩 **Specialised agents (Phase 2-4)** — `TechnicalAgent` (8 tools, trend/MA/MACD/volume/pattern analysis), `IntelAgent` (news & sentiment, risk flag propagation), `DecisionAgent` (synthesis into Decision Dashboard JSON), `RiskAgent` (7 risk categories, two-level severity with soft/hard override)
- 📈 **Strategy system (Phase 3)** — `StrategyAgent` (per-strategy evaluation from YAML skills), `StrategyRouter` (rule-based regime detection → strategy selection), `StrategyAggregator` (weighted consensus with backtest performance factor)
- 🔬 **Deep Research agent (Phase 5)** — `ResearchAgent` with 3-phase approach (decompose → research sub-questions → synthesise report); token budget tracking; new `/research` bot command with aliases (`/深研`, `/deepsearch`)
- 🧠 **Memory & calibration (Phase 6)** — `AgentMemory` with prediction accuracy tracking, confidence calibration (activates after minimum sample threshold), strategy auto-weighting based on historical win rate
- 📊 **Portfolio Agent (Phase 7)** — `PortfolioAgent` for multi-stock portfolio analysis (position sizing, sector concentration, correlation risk, cross-market linkage, rebalance suggestions)
- 🔔 **Event-driven alerts (Phase 7)** — `EventMonitor` with `PriceAlert`, `VolumeAlert`, `SentimentAlert` rules; async checking, callback notifications, serializable persistence
- ⚙️ **New config entries** — `AGENT_ORCHESTRATOR_MODE`, `AGENT_RISK_OVERRIDE`, `AGENT_DEEP_RESEARCH_BUDGET`, `AGENT_MEMORY_ENABLED`, `AGENT_STRATEGY_AUTOWEIGHT`, `AGENT_STRATEGY_ROUTING` — all registered in `config.py` + `config_registry.py` (WebUI-configurable)

### Changed
- 🔐 **Auth password state semantics** — stored password existence is now tracked independently from auth enablement; when auth is disabled, `/api/v1/auth/status` returns `passwordSet=false` while preserving the saved password for future re-enable
- 🔐 **Auth settings re-enable hardening** — re-enabling auth with a stored password now requires `currentPassword`, and failed session creation rolls back the auth toggle to avoid lockout
- ♻️ **AgentExecutor refactored** — `_run_loop` delegates to shared `runner.run_agent_loop()`; removed duplicated serialization/parsing/thinking-label code
- ♻️ **Unified agent switch** — Bot, API, and Pipeline all use `config.is_agent_available()` instead of divergent `config.agent_mode` checks
- 📖 **README.md** — expanded Bot commands section (ask/chat/strategies/history), added NL routing note, updated agent mode description
- 📖 **.env.example** — added `AGENT_ARCH` and `AGENT_NL_ROUTING` configuration documentation
- 🔌 **Analysis API async contract** — `POST /api/v1/analysis/analyze` now documents distinct async `202` payloads for single-stock vs batch requests, and `report_type=full` is treated consistently with the existing full-report behavior

### Fixed
- 🐛 **Analysis API blank-code guardrails** — `POST /api/v1/analysis/analyze` now drops whitespace-only entries before batch enqueue and returns `400` when no valid stock code remains
- 🐛 **Bare `/api` SPA fallback** — unknown API paths now return JSON `404` consistently for both `/api/...` and the exact `/api` path
- 🎮 **Discord channel env compatibility** — runtime now accepts legacy `DISCORD_CHANNEL_ID` as a fallback for `DISCORD_MAIN_CHANNEL_ID`, and the docs/examples now use the same variable name as the actual workflow/config implementation
- 🐛 **Session secret rotation on Windows** — use atomic replace so auth toggles invalidate existing sessions even when `.session_secret` already exists
- 🐛 **Auth toggle atomicity** — persist `ADMIN_AUTH_ENABLED` before rotating session secret; on rotation failure, roll back to the previous auth state
- 🔧 **LLM runtime selection guardrails** — YAML 模式下渠道编辑器不再覆盖 `LITELLM_MODEL` / fallback / Vision；系統配置校验补上全部渠道禁用后的執行时来源檢查，并修复 `vertexai/...` 这类協議别名模型被重复加前綴的議題
- 🐛 **Multi-stock `/ask` follow-up regressions** — portfolio overlay now shares the same timeout budget as the per-stock phase and is skipped on timeout instead of blocking the bot reply; `/history` now stores the readable per-stock summary instead of raw dashboard JSON; condensed multi-stock output now renders numeric `sniper_points` values
- 🐛 **Decision dashboard enum compatibility** — multi-agent `DecisionAgent` now keeps `decision_type` within the legacy `buy|hold|sell` contract and normalizes stray `strong_*` outputs before risk override, pipeline conversion, and downstream統計/通知汇总
- 🛟 **Multi-Agent partial-result fallback** — `IntelAgent` now caches parsed intel for downstream reuse, shared JSON parsing tolerates lightly malformed model output, and the orchestrator preserves/synthesizes a minimal dashboard on timeout or mid-pipeline parse failure instead of always collapsing to `50/观望/未知`
- 🐛 **Shared LiteLLM routing restored** — bot NL intent parsing and `ResearchAgent` planning/synthesis now reuse the same LiteLLM adapter / Router / fallback / `api_base` injection path as the main Agent flow, so `LLM_CHANNELS` / `LITELLM_CONFIG` / OpenAI-compatible deployments behave consistently
- 🐛 **Bot chat session backward compatibility** — `/chat` now keeps using the legacy `{platform}_{user_id}` session id when old history already exists, and `/history` can still list / view / clear those pre-migration sessions alongside the new `{platform}_{user_id}:chat` format
- 🐛 **EventMonitor unsupported rule rejection** — config validation/runtime loading now reject or skip alert types the monitor cannot actually evaluate yet, so schedule mode no longer silently accepts permanent no-op rules
- 🐛 **P0 基本面聚合稳定性修复** (#614) — 修复 `get_stock_info` 板塊语义迴歸（新增 `belong_boards` 并保留 `boards` 相容别名）、引入基本面上下文精简傳回以控制 token、为基本面快取增加最大条目淘汰，并补齐 ETF 总体狀態聚合与 NaN 板塊欄位过滤，保证 fail-open 与最小入侵。
- 🔧 **GitHub Actions 搜尋引擎環境變數补充** — 工作流新增 `MINIMAX_API_KEYS`、`BRAVE_API_KEYS`、`SEARXNG_BASE_URLS` 環境變數映射，使 GitHub Actions 使用者可配置 MiniMax、Brave、SearXNG 搜尋服務（此前 v3.5.0 已添加 provider 實現但缺少工作流配置）
- 🤖 **Multi-Agent runtime consistency** — `AGENT_MAX_STEPS` now propagates to each orchestrated sub-agent; added cooperative `AGENT_ORCHESTRATOR_TIMEOUT_S` budget to stop overlong pipelines before they cascade further
- 🔌 **Multi-Agent feature wiring** — `AGENT_RISK_OVERRIDE` now actively downgrades final dashboards on hard risk findings; `AGENT_MEMORY_ENABLED` now injects recent analysis memory + confidence calibration into specialised agents; multi-stock `/ask` now runs `PortfolioAgent` to add portfolio-level allocation and concentration guidance
- 🔔 **EventMonitor runtime wiring** — schedule mode can now load alert rules from `AGENT_EVENT_ALERT_RULES_JSON`, poll them at `AGENT_EVENT_MONITOR_INTERVAL_MINUTES`, and send triggered alerts through the existing notification service
- 🛠️ **Follow-up stability fixes** — multi-stock `/ask` now falls back to usable text output when dashboard JSON parsing fails; EventMonitor skips semantically invalid rules instead of aborting schedule startup; background alert polling now runs independently of the main scheduled analysis loop
- 🧪 **Multi-Agent regression coverage** — added orchestrator execution tests for `run()`, `chat()`, critical-stage failure, graceful degradation, and timeout handling
- 🧹 **PortfolioAgent cleanup** — `post_process()` now reuses shared JSON parsing and removed stale unused imports
- 🚦 **Bot async dispatch** — `CommandDispatcher` now exposes `dispatch_async()`; NL intent parsing and default command execution are offloaded from the event loop, DingTalk stream awaits async handlers directly, and Feishu stream processing is moved off the SDK callback thread
- 🌐 **Async webhook handler** — new `handle_webhook_async()` function in `bot/handler.py` for use from async contexts (e.g. FastAPI); calls `dispatch_async()` directly without thread bridging
- 🧵 **Feishu stream ThreadPoolExecutor** — replaced unbounded per-message `Thread` spawning with a capped `ThreadPoolExecutor(max_workers=8)` to prevent thread explosion under message bursts
- 🔒 **EventMonitor safety** — `_check_volume()` now safely handles `get_daily_data` returning `None` (no tuple-unpacking crash); `on_trigger` callbacks support both sync and async callables via `asyncio.to_thread`/`await`
- 🧹 **ResearchAgent dedup** — `_filtered_registry()` now delegates to `BaseAgent._filtered_registry()` instead of duplicating the filtering logic
- 🧹 **Bot trailing whitespace cleanup** — removed W291/W293 whitespace issues across `bot/handler.py`, `bot/dispatcher.py`, `bot/commands/base.py`, `bot/platforms/feishu_stream.py`, `bot/platforms/dingtalk_stream.py`
- 🐛 **Dispatcher `_parse_intent_via_llm` safety** — replaced fragile `'raw' in dir()` with `'raw' in locals()` for undefined-variable guard in `JSONDecodeError` handler
- 🐛 **筹码结构 LLM 未填写时兜底补全** (#589) — DeepSeek 等模型未正确填写 `chip_structure` 时，自动用數據源已獲取的筹码數據补全，保证各模型展示一致；普通分析与 Agent 模式均生效
- 🐛 **历史报告狙击点位顯示原始文本** (#452) — 历史详情页现優先展示 `raw_result.dashboard.battle_plan.sniper_points` 中的原始字符串，避免 `analysis_history` 数值列把區間、说明文字或複雜点位壓縮成单个数字；保留原有数值列作为回退
- 🐛 **Session prefix collision** — user ID `123` could see sessions of user `1234` via `startswith`; fixed with colon delimiter in session_id format
- 🐛 **NL pre-filter false positives** — `re.IGNORECASE` caused `[A-Z]{2,5}` to match common English words like "hello"; removed global flag, use inline `(?i:...)` only for English finance keywords
- 🐛 **Dotted ticker in strategy args** — `_get_strategy_args()` didn't recognize `BRK.B` as a stock code, leaving it in strategy text; now accepts `TICKER.CLASS` format
- ⏱️ **efinance 长呼叫挂起修复** (#660) — 为所有 efinance API 呼叫引入 `_ef_call_with_timeout()` 包装（預設 30 秒，可通过 `EFINANCE_CALL_TIMEOUT` 配置）；使用 `executor.shutdown(wait=False)` 確保逾時后不再阻塞主執行緒，彻底消除 81 分钟挂起議題
- 🛡️ **类型安全内容完整性檢查** (#660) — `check_content_integrity()` 现在将非字符串类型的 `operation_advice` / `analysis_summary` 视为缺失欄位，避免下游 `get_emoji()` 因 `dict.strip()` 崩溃
- 📄 **报告保存与通知解耦** (#660) — `_save_local_report()` 不再依賴 `send_notification` 标志触发，`--no-notify` 模式下本機报告照常保存
- 🔄 **operation_advice 字典归一化** (#660) — Pipeline 和 BacktestEngine 现在将 LLM 傳回的 `dict` 格式 `operation_advice` 通过 `decision_type`（不区分大小写）映射为標準字符串，防止因模型輸出格式变化导致崩溃
- 🛡️ **runner.py usage None 防护** (#660) — `response.usage` 为 `None` 时不再拋出 `AttributeError`，回退为 0 token 计数
- 📋 **orchestrator 静默失败改为日誌警告** (#660) — `IntelAgent` / `RiskAgent` 阶段失败现在记录 `WARNING` 而非静默略過，便于診斷

### Notes
- ⚠️ **Multi-worker auth toggles** — runtime auth updates are process-local; multi-worker deployments must restart/roll workers to keep auth state consistent

## [3.5.0] - 2026-03-12

### Added
- 📊 **Web UI full report drawer** (Fixes #214) — history page adds "Full Report" button to display the complete Markdown analysis report in a side drawer; new `GET /api/v1/history/{record_id}/markdown` endpoint
- 📊 **LLM cost tracking** — all LLM calls (analysis, agent, market review) recorded in `llm_usage` table; new `GET /api/v1/usage/summary?period=today|month|all` endpoint returns aggregated token usage by call type and model
- 🔍 **SearXNG search provider** (Fixes #550) — quota-free self-hosted search fallback; priority: Bocha > Tavily > Brave > SerpAPI > MiniMax > SearXNG
- 🔍 **MiniMax web search provider** — `MiniMaxSearchProvider` with circuit breaker (3 failures → 300s cooldown) and dual time-filtering; configured via `MINIMAX_API_KEYS`
- 🤖 **Agent models discovery API** — `GET /api/v1/agent/models` returns available model deployments (primary/fallback/source/api_base) for Web UI model selector
- 🤖 **Agent chat export & send** (#495) — export conversation to .md file; send to configured notification channels; new `POST /api/v1/agent/chat/send`
- 🤖 **Agent background execution** (#495) — analysis continues when switching pages; badge notification on completion; auto-cancel in-progress stream on session switch
- 📝 **Report Engine P0** — Pydantic schema validation for LLM JSON; Jinja2 templates (markdown/wechat/brief) with legacy fallback; content integrity checks with retry; brief mode (`REPORT_TYPE=brief`); history signal comparison
- 📦 **Smart import** — multi-source import from image/CSV/Excel/clipboard; Vision LLM extracts code+name+confidence; name→code resolver (local map + pinyin + AkShare); confidence-tiered confirmation
- ⚙️ **GitHub Actions LiteLLM config** — workflow supports `LITELLM_CONFIG`/`LITELLM_CONFIG_YAML` for flexible AI provider configuration
- ⚙️ **Config engine refactor & system API** (#602) — unified config registry, validation and API exposure
- 📖 **LLM configuration guide** — new `docs/LLM_CONFIG_GUIDE.md` covering 3-tier config, quick start, Vision/Agent/troubleshooting

### Fixed
- 🐛 **analyze_trend always reports No historical data** (#600) — now fetches from DB/DataFetcher instead of broken `get_analysis_context`
- 🐛 **Chip structure fallback when LLM omits it** (#589) — auto-fills from data source chip data for consistent display across models
- 🐛 **History sniper points show raw text** (#452) — prioritizes original strings over compressed numeric values
- 🐛 **GitHub Actions ENABLE_CHIP_DISTRIBUTION configurable** (#617) — no longer hardcoded, supports vars/secrets override
- 🐛 **`.env` save preserves comments and blank lines** — Web settings no longer destroys `.env` formatting
- 🐛 **Agent model discovery fixes** — legacy mode includes LiteLLM-native providers; source detection aligned with runtime; fallback deployments no longer expanded per-key
- 🐛 **Stooq US stock previous close semantics** — no longer misuses open price as previous close
- 🐛 **Stock name prefetch regression** — prioritizes local `STOCK_NAME_MAP` before remote queries
- 🐛 **AkShare limit-up/down calculation** (#555) — fixed market analysis statistics
- 🐛 **AkShare Tencent source field index & ETF quote mapping** (#579)
- 🐛 **Pytdx stock name cache pagination** (#573) — prevents cache overflow
- 🐛 **PushPlus oversized report chunking** (#489) — auto-segments long content
- 🐛 **Agent chat cancel & switch** (#495) — cancel no longer misreports as failure; fast switch no longer overwrites stream state
- 🐛 **MiniMax search status in `/status` command** (#587)
- 🐛 **config_registry duplicate BOCHA_API_KEYS** — removed duplicate dict entry that silently overwrote config

### Changed
- 🔎 **Fetcher failure observability** — logs record start/success/failure with elapsed time, failover transitions; Efinance/Akshare include upstream endpoint and classified failure categories
- ♻️ **Data source resilience & cleanup** (#602) — fallback chain optimization
- ♻️ **Image extract API response extension** — new `items` field (code/name/confidence); `codes` preserved for backward compatibility
- ♻️ **Import parse error messages** — specific failure reasons for Excel/CSV; improved logging with file type and size

### Docs
- 📖 LLM config guide refactored for clarity (#583)
- 📖 `image-extract-prompt.md` with full prompt documentation
- 📖 AkShare fallback cache TTL documentation
## [3.4.10] - 2026-03-07

### Fixed
- 🐛 **EfinanceFetcher ETF OHLCV data** (#541, #527) — switch `_fetch_etf_data` from `ef.fund.get_quote_history` (NAV-only, no OHLCV, no `beg`/`end` params) to `ef.stock.get_quote_history`; ETFs now return proper open/high/low/close/volume/amount instead of zeros; remove obsolete NAV column mappings from `_normalize_data`
- 🐛 **tiktoken 0.12.0 `Unknown encoding cl100k_base`** (#537) — pin `tiktoken>=0.8.0,<0.12.0` in requirements.txt to avoid plugin-registration regression introduced in 0.12.0
- 🐛 **Web UI API error classification** (#540) — frontend no longer treats every HTTP 400 as the same "server/network" failure; now distinguishes Agent disabled / missing params / model-tool incompatibility / upstream LLM errors / local connection failures
- 🐛 **北交所代碼识别失败** (#491, #533) — 8/4/92 开头的 6 位代碼现正确识别为北交所；Tushare/Akshare/Yfinance 等數據源支援 .BJ 或 bj 前綴；Baostock/Pytdx 对北交所代碼显式切換數據源；避免误判上海 B 股 900xxx
- 🐛 **狙击点位解析錯誤** (#488, #532) — 理想買入/二次買入等欄位在无「元」字时误提取括号内技术指標数字；现先截去第一个括号后内容再提取

### Added
- **Markdown-to-image for dashboard report** (#455, #535) — 個股日报汇总支援 markdown 转图片推送（Telegram、WeChat、Custom、Email），与大盤复盘行为一致
- **markdown-to-file engine** (#455) — `MD2IMG_ENGINE=markdown-to-file` 可選，对 emoji 支援更好，需 `npm i -g markdown-to-file`
- **PREFETCH_REALTIME_QUOTES** (#455) — 设为 `false` 可禁用实时行情预取，避免 efinance/akshare_em 全市场拉取
- **Stock name prefetch** (#455) — 分析前预取股票名称，减少报告中「股票xxxxx」占位符
- 📊 **分析报告模型标记** (#528, #534) — 在分析报告 meta、报告末尾、推送内容中展示 `model_used`（完整 LLM 模型名）；Agent 多轮呼叫时记录并展示每轮實際使用的模型（支援 fallback 切換）

### Changed
- **Enhanced markdown-to-image failure warning** (#455) — 转图失败时提示具体依賴（wkhtmltopdf 或 m2f）
- **WeChat-only image routing optimization** (#455) — 仅配置企业微信图片时，不再对完整报告做冗餘转图，避免误导性失败日誌
- **Stock name prefetch lightweight mode** (#455) — 名称预取阶段略過 realtime quote 查詢，减少额外網路开销

## [3.4.9] - 2026-03-06

### Added
- 🧠 **Structured config validation** — `ConfigIssue` dataclass and `validate_structured()` with severity-aware logging; `CONFIG_VALIDATE_MODE=strict` aborts startup on errors
- 🖼️ **Vision model config** — `VISION_MODEL` and `VISION_PROVIDER_PRIORITY` for image stock extraction; provider fallback (Gemini → Anthropic → OpenAI → DeepSeek) when primary fails
- 🚀 **CLI init wizard** — `python -m dsa init` 3-step interactive bootstrap (model → data source → notification), 9 provider presets, incremental merge by default
- 🔧 **Multi-channel LLM support** with visual channel editor (#494)

### Changed
- ♻️ **Vision extraction** — migrated from gemini-3 hardcode to `litellm.completion()` with configurable model and provider fallback; `OPENAI_VISION_MODEL` deprecated in favor of `VISION_MODEL`
- ♻️ **Market analyzer** — uses `Analyzer.generate_text()` for LLM calls; fixes bypass and Anthropic `AttributeError` when using non-Router path
- ♻️ **Config validation refinements** — test_env output format syncs with `validate_structured` (severity-aware ✓/✗/⚠/·); Vision key warning when `VISION_MODEL` set but no provider API key; market_analyzer test covers `generate_market_review` fallback when `generate_text` returns None
- ⚙️ **Auto-tag workflow defaults to NO tag** — only tags when commit message explicitly contains `#patch`, `#minor`, or `#major`
- ♻️ **Formatter and notification refactor** (#516)

### Fixed
- 🐛 **STOCK_LIST not refreshed on scheduled runs** — `.env` or WebUI changes to `STOCK_LIST` now hot-reload before each scheduled analysis (#529)
- 🐛 **WebUI fails to load with MIME type error** — SPA fallback route now resolves correct `Content-Type` for JS/CSS files (#520)
- 🐛 **AstrBot sender docstring misplaced** — `import time` placed before docstring in `_send_astrbot`, causing it to become dead code
- 🐛 **Telegram Markdown link escaping** — `_convert_to_telegram_markdown` escaped `[]()` characters, breaking all Markdown links in reports
- 🐛 **Duplicate `discord_bot_status` field** in Config dataclass — second declaration silently shadowed the first
- 🧹 **Unused imports** — removed `shutil`/`subprocess` from `main.py`
- 🔧 **Config validation and Vision key check** (#525)

### Docs
- 📝 Clarified GitHub Actions non-trading-day manual run controls (`TRADING_DAY_CHECK_ENABLED` + `force_run`) for Issue #461 / PR #466

## [3.4.8] - 2026-03-02

### Fixed
- 🐛 **Desktop exe crashes on startup with `FileNotFoundError`** — PyInstaller build was missing litellm's JSON data files (e.g. `model_prices_and_context_window_backup.json`). Added `--collect-data litellm` to both Windows and macOS build scripts so the files are correctly bundled in the executable.

### CI
- 🔧 Cache Electron binaries on macOS CI runners to prevent intermittent EOF download failures when fetching `electron-vX.Y.Z-darwin-*.zip` from GitHub CDN
- 🔧 Fix macOS DMG `hdiutil Resource busy` error during desktop packaging

### Docs
- 📝 Clarify non-trading-day manual run controls for GitHub Actions (`TRADING_DAY_CHECK_ENABLED` + `force_run`) (#474)

## [3.4.7] - 2026-02-28

### Added
- 🧠 **CN/US Market Strategy Blueprint System** (#395) — market review prompt injects region-specific strategy blueprints with position sizing and risk trigger recommendations

### Fixed
- 🐛 **`TRADING_DAY_CHECK_ENABLED` env var and `--force-run` for GitHub Actions** (#466)
- 🐛 **Agent pipeline preserved resolved stock names** (#464) — placeholder names no longer leak into reports
- 🐛 **Code cleanup** (#462, Fixes #422)
- 🐛 **WebUI auto-build on startup** (#460)
- 🐛 **ARCH_ARGS unbound variable** (#458)
- 🐛 **Time zone inconsistency & right panel flash** (#439)

### Docs
- 📝 Clarify potential ambiguities in code (#343)
- 📝 ENABLE_EASTMONEY_PATCH guidance for Issue #453 (#456)

## [3.4.0] - 2026-02-27

### Added
- 📡 **LiteLLM Direct Integration + Multi API Key Support** (#454, Fixes #421 #428)
  - Removed native SDKs (google-generativeai, google-genai, anthropic); unified through `litellm>=1.80.10`
  - New config: `LITELLM_MODEL`, `LITELLM_FALLBACK_MODELS`, `GEMINI_API_KEYS`, `ANTHROPIC_API_KEYS`, `OPENAI_API_KEYS`
  - Multi-key auto-builds LiteLLM Router (simple-shuffle) with 429 cooldown
  - **Breaking**: `.env` `GEMINI_MODEL` (no prefix) only for fallback; explicit config must include provider prefix

### Changed
- ♻️ **Notification Refactoring** (#435) — extracted 10 sender classes into `src/notification_sender/`

### Fixed
- 🐛 LLM NoneType crash, history API 422, sniper points extraction
- 🐛 Auto-build frontend on WebUI startup — `WEBUI_AUTO_BUILD` env var (default `true`)
- 🐛 Docker explicit project name (#448)
- 🐛 Bocha search SSL retry (#445, #446) — transient errors retry up to 3 times
- 🐛 Gemini google-genai SDK migration (Fixes #440, #444)
- 🐛 Mobile home page scrolling (Fixes #419, #433)
- 🐛 History list scroll reset (#431)
- 🐛 Settings save button false positive (fixes #417, #430)

## [3.3.22] - 2026-02-26

### Added
- 💬 **Chat History Persistence** (Fixes #400, #414) — `/chat` page survives refresh, sidebar session list
- 🎨 Project VI Assets — logo icon set, PSD, vector, banner (#425)
- 🚀 Desktop CI Auto-Release (#426) — Windows + macOS parallel builds

### Fixed
- 🐛 Agent Reasoning 400 & LiteLLM Proxy (fixes #409, #427)
- 🐛 Discord chunked sending (#413) — `DISCORD_MAX_WORDS` config
- 🐛 yfinance shared DataFrame (#412)
- 🐛 sniper_points parsing (#408)
- 🐛 Agent framework category missing (#406)
- 🐛 Date inconsistency & query id (fixes #322, #363)

## [3.3.12] - 2026-02-24

### Added
- 📈 **Intraday Realtime Technical Indicators** (Issue #234, #397) — MA calculated from realtime price, config: `ENABLE_REALTIME_TECHNICAL_INDICATORS`
- 🤖 **Agent Strategy Chat** (#367) — full ReAct pipeline, 11 YAML strategies, SSE streaming, multi-turn chat
- 📢 PushPlus Group Push — `PUSHPLUS_TOPIC` (#402)
- 📅 Trading Day Check (Issue #373, #375) — `TRADING_DAY_CHECK_ENABLED`, `--force-run`

### Fixed
- 🐛 DeepSeek reasoning mode (Issue #379, #386)
- 🐛 Agent news intel persistence (Fixes #396, #405)
- 🐛 Bare except clauses replaced with `except Exception` (#398)
- 🐛 UUID fallback for HTTP non-secure context (fixes #377, #381)
- 🐛 Docker DNS resolution (Fixes #372, #374)
- 🐛 Agent session/strategy bugs — multiple follow-up fixes for #367
- 🐛 yfinance parallel download data filtering

### Changed
- Market review strategy consistency — unified cn/us template
- Agent test assertions updated (`6 -> 11`)


## [3.2.11] - 2026-02-23

### 修复（#patch）
- 🐛 **StockTrendAnalyzer 从未執行** (Issue #357)
  - 根因：`get_analysis_context` 仅傳回 2 天數據且无 `raw_data`，pipeline 中 `raw_data in context` 始终为 False
  - 修复：Step 3 直接呼叫 `get_data_range` 獲取 90 日历天（约 60 交易日）历史數據用于趨勢分析
  - 改善：趨勢分析失败时用 `logger.warning(..., exc_info=True)` 记录完整 traceback

## [3.2.10] - 2026-02-22

### 新增
- ⚙️ 支援 `RUN_IMMEDIATELY` 配置项，设为 `true` 时定时工作触发后立即執行一次分析，無需等待首个定时点

### 修复
- 🐛 修复 Web UI 页面居中議題
- 🐛 修复 Settings 傳回 500 錯誤

## [3.2.9] - 2026-02-22

### 修复
- 🐛 **ETF 分析仅关注指數走勢**（Issue #274）
  - 美股/港股 ETF（如 VOO、QQQ）与 A 股 ETF 不再纳入基金公司层面風險（诉讼、声誉等）
  - 搜尋维度：ETF/指數专用 risk_check、earnings、industry 查詢，避免命中基金管理人新闻
  - AI 提示：指數型标的分析約束，`risk_alerts` 不得出现基金管理人公司经营風險

## [3.2.8] - 2026-02-21

### 修复
- 🐛 **BOT 与 WEB UI 股票代碼大小写统一**（Issue #355）
  - BOT `/analyze` 与 WEB UI 触发分析的股票代碼统一为大写（如 `aapl` → `AAPL`）
  - 新增 `canonical_stock_code()`，在 BOT、API、Config、CLI、task_queue 入口处規範化
  - 历史记录与工作去重邏輯可正确识别同一股票（大小写不再影响）

## [3.2.7] - 2026-02-20

### 新增
- 🔐 **Web 页面密碼驗證**（Issue #320, #349）
  - 支援 `ADMIN_AUTH_ENABLED=true` 启用 Web 登录保护
  - 首次訪問在网页设置初始密碼；支援「系統设置 > 修改密碼」和 CLI `python -m src.auth reset_password` 重置

## [3.2.6] - 2026-02-20
### ⚠️ 破坏性变更（Breaking Changes）

- **历史记录 API 变更 (Issue #322)**
  - 路由变更：`GET /api/v1/history/{query_id}` → `GET /api/v1/history/{record_id}`
  - 參數变更：`query_id` (字符串) → `record_id` (整数)
  - 新闻介面变更：`GET /api/v1/history/{query_id}/news` → `GET /api/v1/history/{record_id}/news`
  - 原因：`query_id` 在批量分析时可能重复，無法唯一标识单条历史记录。改用資料庫主键 `id` 確保唯一性
  - 影响範圍：使用旧版历史详情 API 的所有客户端需同步更新

### 修复
- 修复美股（如 ADBE）技术指標矛盾：akshare 美股复权數據例外，统一美股历史數據源为 YFinance（Issue #311）
- 🐛 **历史记录查詢和顯示議題 (Issue #322)**
  - 修复历史记录列表查詢中日期不一致議題：使用明天作为 endDate，確保包含今天全天的數據
  - 修复服務器 UI 报告选择議題：原因是多条记录共享同一 `query_id`，导致总是顯示第一条。现改用 `analysis_history.id` 作为唯一标识
  - 历史详情、新闻介面及前端組件已全面適配 `record_id`
  - 新增后台轮询（每 30s）与页面可见性变更时静默刷新历史列表，確保 CLI 发起的分析完成后前端能及时同步，使用 `silent` 模式避免触发 loading 狀態
- 🐛 **美股指數实时行情与日线數據** (Issue #273)
  - 修复 SPX、DJI、IXIC、NDX、VIX、RUT 等美股指數無法獲取实时行情的議題
  - 新增 `us_index_mapping` 模組，将使用者輸入（如 SPX）映射为 Yahoo Finance 符号（如 ^GSPC）
  - 美股指數与美股股票日线數據直接路由至 YfinanceFetcher，避免遍歷不支援的數據源
  - 消除重复的美股识别邏輯，统一使用 `is_us_stock_code()` 函數

### 最佳化
- 🎨 **首页輸入栏与 Market Sentiment 布局对齐最佳化**
  - 股票代碼輸入框左缘与历史记录 glass-card 框左对齐
  - 分析按钮右缘与 Market Sentiment 外框右对齐
  - Market Sentiment 卡片向下拉伸填满格子，消除与 STRATEGY POINTS 之间的空隙
  - 窄屏时輸入栏填满宽度，回應式对齐保持一致

## [3.2.5] - 2026-02-19

### 新增
- 🌍 **大盤复盘可選区域**（Issue #299）
  - 支援 `MARKET_REVIEW_REGION` 環境變數：`cn`（A股）、`us`（美股）、`both`（两者）
  - us 模式使用 SPX/纳斯达克/道指/VIX 等指數；both 模式可同时复盘 A 股与美股
  - 預設 `cn`，保持向后相容

## [3.2.4] - 2026-02-18

### 修复
- 🐛 **统一美股數據源为 YFinance**（Issue #311）
  - akshare 美股复权數據例外，统一美股历史數據源为 YFinance
  - 修复 ADBE 等美股股票技术指標矛盾議題

## [3.2.3] - 2026-02-18

### 修复
- 🐛 **标普500实时數據缺失**（Issue #273）
  - 修复 SPX、DJI、IXIC、NDX、VIX、RUT 等美股指數無法獲取实时行情的議題
  - 新增 `us_index_mapping` 模組，将使用者輸入（如 SPX）映射为 Yahoo Finance 符号（如 `^GSPC`）
  - 美股指數与美股股票日线數據直接路由至 YfinanceFetcher，避免遍歷不支援的數據源

## [3.2.2] - 2026-02-16

### 新增
- 📊 **PE 指標支援**（Issue #296）
  - AI System Prompt 增加 PE 估值关注
- 📰 **新闻时效性筛查**（Issue #296）
  - `NEWS_MAX_AGE_DAYS`：新闻最大时效（天），預設 3，避免使用过时資訊
- 📈 **强势趨勢股乖离率放宽**（Issue #296）
  - `BIAS_THRESHOLD`：乖离率閾值（%），預設 5.0，可配置
  - 强势趨勢股（多头排列且趨勢强度 ≥70）自动放宽乖离率到 1.5 倍

## [3.2.1] - 2026-02-16

### 新增
- 🔧 **东财介面补丁可配置开关**
  - 支援 `EFINANCE_PATCH_ENABLED` 環境變數开关东财介面补丁（預設 `true`）
  - 补丁不可用时可降級關閉，避免影响主流程

## [3.2.0] - 2026-02-15

### 新增
- 🔒 **CI 门禁统一（P0）**
  - 新增 `scripts/ci_gate.sh` 作为后端门禁单一入口
  - 主 CI 改为 `backend-gate`、`docker-build`、`web-gate` 三段式
  - CI 触发改为所有 PR，避免 Required Checks 因路徑过滤缺失而卡住合併
  - `web-gate` 支援前端路徑变更按需触发
  - 新增 `network-smoke` 工作流承载非阻断網路場景迴歸
- 📦 **發佈鏈路收斂（P0）**
  - `docker-publish` 調整为 tag 主触发，并增加發佈前门禁校验
  - 手动發佈增加 `release_tag` 輸入与 semver/changelog 强校验
  - 發佈前新增 Docker smoke（關鍵模組匯入）
- 📝 **PR 模板升級（P0）**
  - 增加背景、範圍、驗證命令与结果、回滚方案、Issue 關聯等必填项
- 🤖 **AI 审查覆盖增强（P0）**
  - `pr-review` 纳入 `.github/workflows/**` 範圍
  - 新增 `AI_REVIEW_STRICT` 开关，可選将 AI 审查失败升級为阻断

## [3.1.13] - 2026-02-15

### 新增
- 📊 **仅分析结果摘要**（Issue #262）
  - 支援 `REPORT_SUMMARY_ONLY` 環境變數，设为 `true` 时只推送汇总，不含個股详情
  - 預設 `false`，多股时适合快速浏览

## [3.1.12] - 2026-02-15

### 新增
- 📧 **個股与大盤复盘合併推送**（Issue #190）
  - 支援 `MERGE_EMAIL_NOTIFICATION` 環境變數，设为 `true` 时将個股分析与大盤复盘合併为一次推送
  - 預設 `false`，减少電郵数量、降低被识别为垃圾電郵的風險

## [3.1.11] - 2026-02-15

### 新增
- 🤖 **Anthropic Claude API 支援**（Issue #257）
  - 支援 `ANTHROPIC_API_KEY`、`ANTHROPIC_MODEL`、`ANTHROPIC_TEMPERATURE`、`ANTHROPIC_MAX_TOKENS`
  - AI 分析優先级：Gemini > Anthropic > OpenAI
- 📷 **从图片识别股票代碼**（Issue #257）
  - 上傳自选股截图，通过 Vision LLM 自动提取股票代碼
  - API: `POST /api/v1/stocks/extract-from-image`；支援 JPEG/PNG/WebP/GIF，最大 5MB
  - 支援 `OPENAI_VISION_MODEL` 单独配置图片识别模型
- ⚙️ **通达信數據源手动配置**（Issue #257）
  - 支援 `PYTDX_HOST`、`PYTDX_PORT` 或 `PYTDX_SERVERS` 配置自建通达信服務器

## [3.1.10] - 2026-02-15

### 新增
- ⚙️ **立即執行配置**（Issue #332）
  - 支援 `RUN_IMMEDIATELY` 環境變數，`true` 时定时工作啟動后立即執行一次
- 🐛 修复 Docker 构建議題

## [3.1.9] - 2026-02-14

### 新增
- 🔌 **东财介面补丁機制**
  - 新增 `patch/eastmoney_patch.py` 修复 efinance 上游介面变更
  - 不影响其他數據源的正常執行

## [3.1.8] - 2026-02-14

### 新增
- 🔐 **Webhook 证书校验开关**（Issue #265）
  - 支援 `WEBHOOK_VERIFY_SSL` 環境變數，可關閉 HTTPS 证书校验以支援自簽名证书
  - 預設保持校验，關閉存在 MITM 風險，仅建议在可信内网使用

## [3.1.7] - 2026-02-14

### 修复
- 🐛 修复包匯入錯誤（package import error）

## [3.1.6] - 2026-02-13

### 修复
- 🐛 修复 `news_intel` 中 `query_id` 不一致議題

## [3.1.5] - 2026-02-13

### 新增
- 📷 **Markdown 转图片通知**（Issue #289）
  - 支援 `MARKDOWN_TO_IMAGE_CHANNELS` 配置，对 Telegram、企业微信、自定义 Webhook（Discord）、電郵发送图片格式报告
  - 電郵为内联附件，增强对不支援 HTML 客户端的相容性
  - 需安裝 `wkhtmltopdf` 和 `imgkit`

## [3.1.4] - 2026-02-12

### 新增
- 📧 **股票分組发往不同邮箱**（Issue #268）
  - 支援 `STOCK_GROUP_N` + `EMAIL_GROUP_N` 配置，不同股票组报告发送到对应邮箱
  - 大盤复盘发往所有配置的邮箱

## [3.1.3] - 2026-02-12

### 修复
- 🐛 修复 Docker 内執行时通过页面修改配置报错 `[Errno 16] Device or resource busy` 的議題

## [3.1.2] - 2026-02-11

### 修复
- 🐛 修复 Docker 一致性議題，解決關鍵批次處理与通知 Bug

## [3.1.1] - 2026-02-11

### 变更
- ♻️ `API_HOST` → `WEBUI_HOST`：Docker Compose 配置项统一

## [3.1.0] - 2026-02-11

### 新增
- 📊 **ETF 支援增强与代碼規範化**
  - 统一各數據源 ETF 代碼處理邏輯
  - 新增 `canonical_stock_code()` 统一代碼格式，確保數據源路由正确

## [3.0.5] - 2026-02-08

### 修复
- 🐛 修复信号 emoji 与建议不一致的議題（复合建议如"賣出/观望"未正确映射）
- 🐛 修复 `*ST` 股票名在微信/Dashboard 中 markdown 转义議題
- 🐛 修复 `idx.amount` 为 None 时大盤复盘 TypeError
- 🐛 修复分析 API 傳回 `report=None` 及 ReportStrategy 类型不一致議題
- 🐛 修复 Tushare 傳回类型錯誤（dict → UnifiedRealtimeQuote）及 API 端点指向

### 新增
- 📊 大盤复盘报告注入结构化數據（漲跌統計、指數表格、板塊排名）
- 🔍 搜尋结果 TTL 快取（500 条上限，FIFO 淘汰）
- 🔧 Tushare Token 存在时自动注入实时行情優先级
- 📰 新闻摘要截斷长度 50→200 字

### 最佳化
- ⚡ 补充行情欄位請求限制为最多 1 次，减少无效請求

## [3.0.4] - 2026-02-07

### 新增
- 📈 **回测引擎** (PR #269)
  - 新增基于历史分析记录的回测系統，支援收益率、胜率、最大回撤等指標評估
  - WebUI 集成回测结果展示

## [3.0.3] - 2026-02-07

### 修复
- 🐛 修复狙击点位數據解析錯誤議題 (PR #271)

## [3.0.2] - 2026-02-06

### 新增
- ✉️ 可配置電郵发送者名称 (PR #272)
- 🌐 外国股票支援英文關鍵词搜尋

## [3.0.1] - 2026-02-06

### 修复
- 🐛 修复 ETF 实时行情獲取、市场數據回退、企业微信訊息分块議題
- 🔧 CI 流程简化

## [3.0.0] - 2026-02-06

### 移除
- 🗑️ **移除旧版 WebUI**
  - 刪除基于 `http.server.ThreadingHTTPServer` 的旧版 WebUI（`web/` 包）
  - 旧版 WebUI 的功能已完全被 FastAPI（`api/`）+ React 前端替代
  - `--webui` / `--webui-only` 命令行參數标记为弃用，自动重定向到 `--serve` / `--serve-only`
  - `WEBUI_ENABLED` / `WEBUI_HOST` / `WEBUI_PORT` 環境變數保持相容，自动轉發到 FastAPI 服務
  - `webui.py` 保留为相容入口，啟動时直接呼叫 FastAPI 后端
  - Docker Compose 中移除 `webui` 服務定义，统一使用 `server` 服務

### 变更
- ♻️ **服務层重构**
  - 将 `web/services.py` 中的非同步工作服務迁移至 `src/services/task_service.py`
  - Bot 分析命令（`bot/commands/analyze.py`）改为使用 `src.services.task_service`
  - Docker 環境變數 `WEBUI_HOST`/`WEBUI_PORT` 更名为 `API_HOST`/`API_PORT`（旧名仍相容）

## [2.3.0] - 2026-02-01

### 新增
- 🇺🇸 **增强美股支援** (Issue #153)
  - 實現基于 Akshare 的美股历史數據獲取 (`ak.stock_us_daily()`)
  - 實現基于 Yfinance 的美股实时行情獲取（優先策略）
  - 增加对不支援數據源（Tushare/Baostock/Pytdx/Efinance）的美股代碼过滤和快速降級

### 修复
- 🐛 修复 AMD 等美股代碼被误识别为 A 股的議題 (Issue #153)

## [2.2.5] - 2026-02-01

### 新增
- 🤖 **AstrBot 訊息推送** (PR #217)
  - 新增 AstrBot 通知渠道，支援推送到 QQ 和微信
  - 支援 HMAC SHA256 簽名驗證，確保通信安全
  - 通过 `ASTRBOT_URL` 和 `ASTRBOT_TOKEN` 配置

## [2.2.4] - 2026-02-01

### 新增
- ⚙️ **可配置數據源優先级** (PR #215)
  - 支援通过環境變數（如 `YFINANCE_PRIORITY=0`）动态調整數據源優先级
  - 無需修改代碼即可優先使用特定數據源（如 Yahoo Finance）

## [2.2.3] - 2026-01-31

### 修复
- 📦 更新 requirements.txt，增加 `lxml_html_clean` 依賴以解決相容性議題

## [2.2.2] - 2026-01-31

### 修复
- 🐛 修复代理配置区分大小写議題 (fixes #211)

## [2.2.1] - 2026-01-31

### 修复
- 🐛 **YFinance 相容性修复** (PR #210, fixes #209)
  - 修复新版 yfinance 傳回 MultiIndex 列名导致的數據解析錯誤

## [2.2.0] - 2026-01-31

### 新增
- 🔄 **多源回退策略增强**
  - 實現了更健壮的數據獲取回退機制 (feat: multi-source fallback strategy)
  - 最佳化了數據源故障时的自动切換邏輯

### 修复
- 🐛 修复 analyzer 執行后無法通过改 .env 文件的 stock_list 内容調整跟踪的股票

## [2.1.14] - 2026-01-31

### 文档
- 📝 更新 README 和最佳化 auto-tag 規則

## [2.1.13] - 2026-01-31

### 修复
- 🐛 **Tushare 優先级与实时行情** (Fixed #185)
  - 修复 Tushare 數據源優先级设置議題
  - 修复 Tushare 实时行情獲取功能

## [2.1.12] - 2026-01-30

### 修复
- 🌐 修复代理配置在某些情况下的区分大小写議題
- 🌐 修复本機環境禁用代理的邏輯

## [2.1.11] - 2026-01-30

### 最佳化
- 🚀 **飞书訊息流最佳化** (PR #192)
  - 最佳化飞书 Stream 模式的訊息类型處理
  - 修改 Stream 訊息模式預設为關閉，防止配置錯誤執行时报错

## [2.1.10] - 2026-01-30

### 合併
- 📦 合併 PR #154 贡献

## [2.1.9] - 2026-01-30

### 新增
- 💬 **微信文本訊息支援** (PR #137)
  - 新增微信推送的纯文本訊息类型支援
  - 添加 `WECHAT_MSG_TYPE` 配置项

## [2.1.8] - 2026-01-30

### 修复
- 🐛 修正日誌中 API 提供商顯示錯誤 (PR #197)

## [2.1.7] - 2026-01-30

### 修复
- 🌐 禁用本機環境的代理设置，避免網路連線議題

## [2.1.6] - 2026-01-29

### 新增
- 📡 **Pytdx 數據源 (Priority 2)**
  - 新增通达信數據源，免费無需注册
  - 多服務器自动切換
  - 支援实时行情和历史數據
- 🏷️ **多源股票名称解析**
  - DataFetcherManager 新增 `get_stock_name()` 方法
  - 新增 `batch_get_stock_names()` 批量查詢
  - 自动在多數據源间回退
  - Tushare 和 Baostock 新增股票名称/列表方法
- 🔍 **增强搜尋回退**
  - 新增 `search_stock_price_fallback()` 用于數據源全部失败时
  - 新增搜尋维度：市场分析、行业分析
  - 最大搜尋次数从 3 增加到 5
  - 改进搜尋结果格式（每维度 4 条结果）

### 改进
- 更新搜尋查詢模板以提高相關性
- 增强 `format_intel_report()` 輸出结构

## [2.1.5] - 2026-01-29

### 新增
- 📡 新增 Pytdx 數據源和多源股票名称解析功能

## [2.1.4] - 2026-01-29

### 文档
- 📝 更新赞助商資訊

## [2.1.3] - 2026-01-28

### 文档
- 📝 重构 README 布局
- 🌐 新增繁体中文翻译 (README_CHT.md)

### 修复
- 🐛 修复 WebUI 無法輸入美股代碼議題
  - 輸入框邏輯改成所有字母都轉換成大写
  - 支援 `.` 的輸入（如 `BRK.B`）

## [2.1.2] - 2026-01-27

### 修复
- 🐛 修复個股分析推送失败和报告路徑議題 (fixes #166)
- 🐛 修改 CR 錯誤，確保微信訊息最大字节配置生效

## [2.1.1] - 2026-01-26

### 新增
- 🔧 添加 GitHub Actions auto-tag 工作流
- 📡 添加 yfinance 兜底數據源及數據缺失警告

### 修复
- 🐳 修复 docker-compose 路徑和文档命令
- 🐳 Dockerfile 补充 copy src 文件夹 (fixes #145)

## [2.1.0] - 2026-01-25

### 新增
- 🇺🇸 **美股分析支援**
  - 支援美股代碼直接輸入（如 `AAPL`, `TSLA`）
  - 使用 YFinance 作为美股數據源
- 📈 **MACD 和 RSI 技术指標**
  - MACD：趨勢确认、金叉死叉信号（零轴上金叉⭐、金叉✅、死叉❌）
  - RSI：超买超卖判斷（超卖⭐、强势✅、超买⚠️）
  - 指標信号纳入综合評分系統
- 🎮 **Discord 推送支援** (PR #124, #125, #144)
  - 支援 Discord Webhook 和 Bot API 两种方式
  - 通过 `DISCORD_WEBHOOK_URL` 或 `DISCORD_BOT_TOKEN` + `DISCORD_MAIN_CHANNEL_ID` 配置
- 🤖 **机器人命令交互**
  - 钉钉机器人支援 `/分析 股票代碼` 命令触发分析
  - 支援 Stream 长連線模式
- 🌡️ **AI 温度參數可配置** (PR #142)
  - 支援自定义 AI 模型温度參數
- 🐳 **Zeabur 部署支援**
  - 添加 Zeabur 镜像部署工作流
  - 支援 commit hash 和 latest 双標籤

### 重构
- 🏗️ **项目结构最佳化**
  - 核心代碼移至 `src/` 目錄，根目錄更清爽
  - 文档移至 `docs/` 目錄
  - Docker 配置移至 `docker/` 目錄
  - 修复所有 import 路徑，保持向后相容
- 🔄 **數據源架構升級**
  - 新增數據源熔斷機制，单數據源连续失败自动切換
  - 实时行情快取最佳化，批量预取减少 API 呼叫
  - 網路代理智能分流，国内介面自动直连
- 🤖 Discord 机器人重构为平台適配器架構

### 修复
- 🌐 **網路稳定性增强**
  - 自动检测代理配置，对国内行情介面強制直连
  - 修复 EfinanceFetcher 偶发的 `ProtocolError`
  - 增加对底层網路錯誤的捕獲和重試機制
- 📧 **電郵渲染最佳化**
  - 修复電郵中表格不渲染議題 (#134)
  - 最佳化電郵排版，更紧凑美观
- 📢 **企业微信推送修复**
  - 修复大盤复盘推送不完整議題
  - 增强訊息分割邏輯，支援更多标题格式
  - 增加分批发送间隔，避免限流丢失
- 👷 **CI/CD 修复**
  - 修复 GitHub Actions 中路徑引用的錯誤

## [2.0.0] - 2026-01-24

### 新增
- 🇺🇸 **美股分析支援**
  - 支援美股代碼直接輸入（如 `AAPL`, `TSLA`）
  - 使用 YFinance 作为美股數據源
- 🤖 **机器人命令交互** (PR #113)
  - 钉钉机器人支援 `/分析 股票代碼` 命令触发分析
  - 支援 Stream 长連線模式
  - 支援选择精简报告或完整报告
- 🎮 **Discord 推送支援** (PR #124)
  - 支援 Discord Webhook 推送
  - 添加 Discord 環境變數到工作流

### 修复
- 🐳 修复 WebUI 在 Docker 中綁定 0.0.0.0 (fixed #118)
- 🔔 修复飞书长連線通知議題
- 🐛 修复 `analysis_delay` 未定义錯誤
- 🔧 啟動时 config.py 检测通知渠道，修复已配置自定义渠道情况下仍然提示未配置議題

### 改进
- 🔧 最佳化 Tushare 優先级判斷邏輯，提升封装性
- 🔧 修复 Tushare 優先级提升后仍排在 Efinance 之后的議題
- ⚙️ 配置 TUSHARE_TOKEN 时自动提升 Tushare 數據源優先级
- ⚙️ 實現 4 个使用者反馈 issue (#112, #128, #38, #119)

## [1.6.0] - 2026-01-19

### 新增
- 🖥️ WebUI 管理界面及 API 支援（PR #72）
  - 全新 Web 架構：分層設計（Server/Router/Handler/Service）
  - 核心 API：支援 `/analysis` (触发分析), `/tasks` (查詢进度), `/health` (健康檢查)
  - 交互界面：支援页面直接輸入代碼并触发分析，实时展示进度
  - 執行模式：新增 `--webui-only` 模式，仅啟動 Web 服務
  - 解決了 [#70](https://github.com/ZhuLinsen/daily_stock_analysis/issues/70) 的核心需求（提供触发分析的介面）
- ⚙️ GitHub Actions 配置灵活性增强（[#79](https://github.com/ZhuLinsen/daily_stock_analysis/issues/79)）
  - 支援从 Repository Variables 讀取非敏感配置（如 STOCK_LIST, GEMINI_MODEL）
  - 保持对 Secrets 的向下相容

### 修复
- 🐛 修复企业微信/飞书报告截斷議題（[#73](https://github.com/ZhuLinsen/daily_stock_analysis/issues/73)）
  - 移除 notification.py 中不必要的长度硬截斷邏輯
  - 依賴底层自动分片機制處理长訊息
- 🐛 修复 GitHub Workflow 環境變數缺失（[#80](https://github.com/ZhuLinsen/daily_stock_analysis/issues/80)）
  - 修复 `CUSTOM_WEBHOOK_BEARER_TOKEN` 未正确传递到 Runner 的議題

## [1.5.0] - 2026-01-17

### 新增
- 📲 单股推送模式（[#55](https://github.com/ZhuLinsen/daily_stock_analysis/issues/55)）
  - 每分析完一只股票立即推送，不用等全部分析完
  - 命令行參數：`--single-notify`
  - 環境變數：`SINGLE_STOCK_NOTIFY=true`
- 🔐 自定义 Webhook Bearer Token 認證（[#51](https://github.com/ZhuLinsen/daily_stock_analysis/issues/51)）
  - 支援需要 Token 認證的 Webhook 端点
  - 環境變數：`CUSTOM_WEBHOOK_BEARER_TOKEN`

## [1.4.0] - 2026-01-17

### 新增
- 📱 Pushover 推送支援（PR #26）
  - 支援 iOS/Android 跨平台推送
  - 通过 `PUSHOVER_USER_KEY` 和 `PUSHOVER_API_TOKEN` 配置
- 🔍 博查搜尋 API 集成（PR #27）
  - 中文搜尋最佳化，支援 AI 摘要
  - 通过 `BOCHA_API_KEYS` 配置
- 📊 Efinance 數據源支援（PR #59）
  - 新增 efinance 作为數據源选项
- 🇭🇰 港股支援（PR #17）
  - 支援 5 位代碼或 HK 前綴（如 `hk00700`、`hk1810`）

### 修复
- 🔧 飞书 Markdown 渲染最佳化（PR #34）
  - 使用交互卡片和格式化器修复渲染議題
- ♻️ 股票列表热重載（PR #42 修复）
  - 分析前自动重載 `STOCK_LIST` 配置
- 🐛 钉钉 Webhook 20KB 限制處理
  - 长訊息自动分块发送，避免被截斷
- 🔄 AkShare API 重試機制增强
  - 添加失败快取，避免重复請求失败介面

### 改进
- 📝 README 精简最佳化
  - 進階配置移至 `docs/full-guide.md`


## [1.3.0] - 2026-01-12

### 新增
- 🔗 自定义 Webhook 支援
  - 支援任意 POST JSON 的 Webhook 端点
  - 自动识别钉钉、Discord、Slack、Bark 等常见服務格式
  - 支援配置多个 Webhook（逗号分隔）
  - 通过 `CUSTOM_WEBHOOK_URLS` 環境變數配置

### 修复
- 📝 企业微信长訊息分批发送
  - 解決自选股过多时内容超过 4096 字符限制导致推送失败的議題
  - 智能按股票分析块分割，每批添加分页标记（如 1/3, 2/3）
  - 批次间隔 1 秒，避免触发频率限制

## [1.2.0] - 2026-01-11

### 新增
- 📢 多渠道推送支援
  - 企业微信 Webhook
  - 飞书 Webhook（新增）
  - 電郵 SMTP（新增）
  - 自动识别渠道类型，配置更簡單

### 改进
- 统一使用 `NOTIFICATION_URL` 配置，相容旧的 `WECHAT_WEBHOOK_URL`
- 電郵支援 Markdown 转 HTML 渲染

## [1.1.0] - 2026-01-11

### 新增
- 🤖 OpenAI 相容 API 支援
  - 支援 DeepSeek、通义千问、Moonshot、智谱 GLM 等
  - Gemini 和 OpenAI 格式二选一
  - 自动降級重試機制

## [1.0.0] - 2026-01-10

### 新增
- 🎯 AI 决策仪表盘分析
  - 一句话核心结论
  - 精確買入/止损/目标点位
  - 檢查清单（✅⚠️❌）
  - 分持倉建议（空仓者 vs 持倉者）
- 📊 大盤复盘功能
  - 主要指數行情
  - 漲跌統計
  - 板塊漲跌榜
  - AI 生成复盘报告
- 🔍 多數據源支援
  - AkShare（主數據源，免费）
  - Tushare Pro
  - Baostock
  - YFinance
- 📰 新闻搜尋服務
  - Tavily API
  - SerpAPI
- 💬 企业微信机器人推送
- ⏰ 定时工作调度
- 🐳 Docker 部署支援
- 🚀 GitHub Actions 零成本部署

### 技术特性
- Gemini AI 模型（gemini-3-flash-preview）
- 429 限流自动重試 + 模型切換
- 請求间延时防封禁
- 多 API Key 负载均衡
- SQLite 本機數據存储

---

[Unreleased]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.17.1...HEAD
[3.17.1]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.17.0...v3.17.1
[3.17.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.16.0...v3.17.0
[3.16.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.15.0...v3.16.0
[3.15.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.14.2...v3.15.0
[3.14.2]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.14.1...v3.14.2
[3.14.1]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.14.0...v3.14.1
[3.14.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.13.0...v3.14.0
[3.13.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.12.0...v3.13.0
[3.12.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.11.0...v3.12.0
[3.11.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.10.1...v3.11.0
[3.10.1]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.10.0...v3.10.1
[3.10.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.9.0...v3.10.0
[3.9.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.8.0...v3.9.0
[3.8.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.7.0...v3.8.0
[3.7.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.6.0...v3.7.0
[3.6.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.5.0...v3.6.0
[3.5.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.4.10...v3.5.0
[3.4.10]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.4.9...v3.4.10
[3.4.9]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.4.8...v3.4.9
[3.4.8]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.4.7...v3.4.8
[3.4.7]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.4.0...v3.4.7
[3.4.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.3.22...v3.4.0
[3.3.22]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.3.12...v3.3.22
[3.3.12]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.2.11...v3.3.12
[3.2.11]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v3.2.10...v3.2.11
[2.3.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.2.5...v2.3.0
[2.2.5]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.2.4...v2.2.5
[2.2.4]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.2.3...v2.2.4
[2.2.3]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.2.2...v2.2.3
[2.2.2]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.2.1...v2.2.2
[2.2.1]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.2.0...v2.2.1
[2.2.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.14...v2.2.0
[2.1.14]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.13...v2.1.14
[2.1.13]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.12...v2.1.13
[2.1.12]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.11...v2.1.12
[2.1.11]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.10...v2.1.11
[2.1.10]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.9...v2.1.10
[2.1.9]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.8...v2.1.9
[2.1.8]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.7...v2.1.8
[2.1.7]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.6...v2.1.7
[2.1.6]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.5...v2.1.6
[2.1.5]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.4...v2.1.5
[2.1.4]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.3...v2.1.4
[2.1.3]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.2...v2.1.3
[2.1.2]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.1...v2.1.2
[2.1.1]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.1.0...v2.1.1
[2.1.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v1.6.0...v2.0.0
[1.6.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/ZhuLinsen/daily_stock_analysis/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ZhuLinsen/daily_stock_analysis/releases/tag/v1.0.0
