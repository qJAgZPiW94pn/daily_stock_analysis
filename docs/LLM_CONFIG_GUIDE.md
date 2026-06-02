# LLM (大模型) 配置指南

欢迎！无论你是刚接触 AI 的新手小白，还是精通各种 API 的高玩老手，这份指南都能帮你快速把大模型（LLM）跑起来。

本项目对外提供统一的 AI 模型接入体验，支援主流官方 API、OpenAI 相容平台以及本機模型。底层由 [LiteLLM](https://docs.litellm.ai/) 驱动，但大多数使用者只需要理解“选服務商、填 API Key、选主模型/渠道”这条預設路徑。为了照顾不同阶段的使用者，我们設計了“三层優先级”配置，按需选择最适合你的方式即可。

如果你正在选择具体服務商、配置 GitHub Actions Secrets / Variables、排查 `details.reason` 錯誤或准备回滚配置，请優先查看 [LLM 服務商配置指南](./llm-providers.md)。该文档集中维护 provider 预设、Actions 變數对照、執行时能力检测邊界和常见錯誤處理建议。

> 本页的 provider/model/Base URL 说明本次未新增外部相容语义，仅用于同步现网约定；實際相容判斷仍按当前倉庫锁定依賴与執行时實現執行：
> - 依賴邊界：`litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`（与 `requirements.txt` 一致）。
> - 相容驗證入口：`tests/test_system_config_service.py`、`tests/test_system_config_api.py` 以及现有前端模型配置页迴歸用例。
> - 回退路徑：優先使用 `.env` 配置備份 + `POST /api/v1/system/config/import` 恢復；也可在重啟前手动回填旧 `LITELLM_MODEL` / `LLM_*` / `AGENT_LITELLM_MODEL` / `VISION_MODEL` / `LLM_TEMPERATURE`。

> **说明**：本页对 provider/model/base URL 的说明同步沿用当前依賴約束与历史约定，仅做文档补充，不引入新的執行时 provider、模型或 Base URL 行为变更。

---

## 快速导航：你应该看哪一节？

1. **【新手小白】** "我只想赶紧把系統跑起来，越簡單越好！" -> [指路【方式一：极簡單模型配置】](#方式一极簡單模型配置适合新手)
2. **【进阶使用者】** "我有好几个 Key，想配置备用模型，还要改自定义网址(Base URL)。" -> [指路【方式二：渠道(Channels)模式配置】](#方式二渠道channels模式配置适合进阶多模型)
3. **【高玩老手】** "我要做複雜的负载均衡、請求路由、甚至多异构平台高可用！" -> [指路【方式三：YAML 進階配置】](#方式三yaml進階配置适合老手自定义)
4. **【本機模型】** "我想用 Ollama 本機模型！" -> [指路【示例 4：使用 Ollama 本機模型】](#示例-4使用-ollama-本機模型)
5. **【视觉模型】** "我想用图片识别股票代碼！" -> [指路【扩展功能：看图模型(Vision)配置】](#扩展功能看图模型vision配置)

---

## 方式一：极簡單模型配置（适合新手）

**目标：** 只要记得填入 API Key 和对应的模型名就能立刻用。不需要折腾複雜概念。

如果你只打算用一种模型，这是最快捷的办法。打开项目根目錄下的 `.env` 文件（如果没有，复制一份 `.env.example` 并重命名为 `.env`）。

### Anspire Open 示例：

> 💡 **推荐 [Anspire Open](https://open.anspire.cn/?share_code=QFBC0FYC)**：支援中文最佳化的联网搜尋与 OpenAI-compatible 路徑一体化体验，适合只准备一个 Key 的使用者。
> - 以下为配置示例，模型与网关可用性以账号權限和 Anspire 控制台为准；文档示例不替代實際連通性驗證。
> - 建议在 Web 设置页点击“測試連線”進行實際鉴权与模型可用性檢查，避免以文档預設值直接当作可用性承诺。

```env
# Anspire Open API Keys（支援多个，逗号分隔）
# 獲取: https://open.anspire.cn/?share_code=QFBC0FYC
# 满足預設優先级條件时，系統会复用该 Key 處理搜尋与 LLM（仅限示例兜底路徑）。
# 示例模型：Doubao-Seed-2.0-lite；示例网关：https://open-gateway.anspire.cn/v6
ANSPIRE_API_KEYS=sk-xxxxxxxxxxxxxxxx
# 可選：按控制台可用性切換模型或网关
# ANSPIRE_LLM_MODEL=Doubao-Seed-2.0-pro
# ANSPIRE_LLM_BASE_URL=https://open-gateway.anspire.ai/v6
```

### 示例 1：使用通用第三方平台（相容 OpenAI 格式，推荐）

现在市面上绝大多数第三方聚合平台（例如硅基流动、AIHubmix、阿里百炼、智谱等）都相容 OpenAI 的介面格式。只要平台提供了 API Key 和 Base URL，你都可以按照以下格式无脑配置：

```env
# 填入平台提供给你的 API Key
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
# 填入平台的介面地址 (非常重要：结尾通常必须带有 /v1)
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
# 填入该平台上具体的模型名称（非常重要：注意前面必须加上 openai/ 前綴帮系統识别）
LITELLM_MODEL=openai/deepseek-ai/DeepSeek-V3 
```

### 示例 2：使用 DeepSeek 官方介面
```env
# 填入你在 DeepSeek 官方平台申请的 API Key
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
```
*相容提示：仅填这一行时，系統仍会預設使用 `deepseek/deepseek-chat` 并在日誌提示迁移。*
`deepseek-chat` / `deepseek-reasoner` 仍可用于相容旧配置，但 DeepSeek 官方已标记为 2026/07/24 后废弃；新配置建议通过 Web 快速渠道或显式 `LITELLM_MODEL=deepseek/deepseek-v4-flash` 迁移到 `deepseek-v4-flash` / `deepseek-v4-pro`。

### 示例 3：使用 Gemini 免费 API
```env
# 填入你獲取的 Google Gemini Key
GEMINI_API_KEY=AIzac...
```

### 示例 4：使用 Ollama 本機模型
```env
# Ollama 無需 API Key，本機執行 ollama serve 后即可使用
OLLAMA_API_BASE=http://localhost:11434
LITELLM_MODEL=ollama/qwen3:8b
```

> **重要**：Ollama 必须使用 `OLLAMA_API_BASE` 配置，**不要**使用 `OPENAI_BASE_URL`，否则系統会錯誤拼接 URL（如 404、`api/generate/api/show`）。遠端 Ollama 时，将 `OLLAMA_API_BASE` 设为實際地址（如 `http://192.168.1.100:11434`）。当前依賴約束为 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`（与 requirements.txt 一致）。

> **恭喜！小白读到这里就可以去執行程式了！**
> 想测测看通没通？在主目錄打开命令行輸入：`python scripts/check_env.py --llm`

---

## 方式二：渠道(Channels)模式配置（适合进阶/多模型）

**目标：** 我有多个不同平台的 Key 想要混着用，如果主模型卡了/網路挂了，我希望它能自动切換到备用模型。

**网页端可以直接配：** 你可以啟動程式后，在 **Web UI 的“系統设置 -> AI 模型 -> AI 模型接入”** 中非常直观地進行可视化配置！

> **新版编辑体验补充**：对于 DeepSeek、阿里百炼（DashScope）以及其他相容 OpenAI `/v1/models` 的渠道，设置页现在支援直接点击“獲取模型”，从 `{base_url}/models` 拉取可用模型并多选；底层仍会保存为原来的 `LLM_{CHANNEL}_MODELS=model1,model2` 逗号格式。若渠道不支援该介面、鉴权失败或暂时不可达，仍可繼續手动填写模型列表，不影响保存。

### 首次啟動配置狀態

后端提供只读狀態介面 `GET /api/v1/system/config/setup/status`，用于判斷首次啟動闭环中最基礎的几类配置是否已經就绪：LLM 主渠道、Agent 渠道、自选股、通知渠道和本機存储。这个介面只讀取已保存的 `.env` 与当前程式環境變數，不会重載執行时配置、写入 `.env`、測試真实模型或建立資料庫文件；前端向导和后续 smoke run 可以基于该介面逐步接入。

### Web 渠道编辑器的相容性 / 迁移 / 回退規則

- 预设里的 provider / Base URL / 示例模型只用于**初始化表单**；真正落盘时仍是你当前輸入的 `LLM_{CHANNEL}_PROTOCOL`、`LLM_{CHANNEL}_BASE_URL`、`LLM_{CHANNEL}_MODELS`、`LLM_{CHANNEL}_API_KEY(S)`，不会在后台偷偷改成别的 provider 名或 URL。
- 设置页的“獲取模型”只对 `OpenAI Compatible` / `DeepSeek` 渠道呼叫 `{base_url}/models`；“測試連線”預設只对模型列表首项发起一次最小聊天請求，并在结果中展示后端規範化后的 `resolved_model`。若傳回 `details.reason=model_access_denied`（例如 Issue #1208 中已观测到的 SiliconFlow / OpenAI Compatible 经 LiteLLM 傳回 `Model disabled`），请把它视为基于 provider 文案的 best-effort 模型可用性診斷，優先确认该模型是否已在当前账号/key 下开通，必要时調整模型顺序或移除不可用模型后重試；未覆盖或语义不同的 provider 文案会繼續走兜底診斷。可選的“執行时能力检测”必须由使用者显式选择后触发，会额外发起 JSON / tools / stream / vision smoke 請求，结果仅代表当前账号、模型和 endpoint 的一次 best-effort 检测。上述检测傳回的 `stage / error_code / details / latency_ms / capability_results` 仅用于结构化診斷提示，**不会写回** `.env`，也不会阻止保存。
- 若傳回 `details.reason=provider_blocked`，表示服務商或中转网关明確拦截了本次請求；它区别于本機網路 / TLS 例外和 `model_access_denied`，应優先檢查账号风控、地域或請求来源限制、模型權限、代理商网关策略和内容安全策略。
- 執行时能力检测会产生真实 LLM 請求，可能带来 token / 图像輸入费用、RPM/TPM 限流、余额不足或逾時。检测失败可能来自账号權限、模型未开通、endpoint 区域、余额、服務商相容层或 LiteLLM 轉換路徑，不等于该 provider 全局不支援对应能力。P3 未对所有真实 provider 做在线 smoke；相容依据来自当前依賴約束 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0` 下的 LiteLLM `completion()` / OpenAI I/O format / streaming / exception mapping，以及 OpenAI Chat Completions 的 JSON mode、tool calling、streaming 和 vision input 形状。
- 相關外部来源：LiteLLM Python SDK / OpenAI I/O format / streaming / exception mapping：<https://docs.litellm.ai/>；LiteLLM OpenAI-compatible 路由：<https://docs.litellm.ai/docs/providers/openai_compatible>；OpenAI Chat Completions：<https://platform.openai.com/docs/api-reference/chat/create>；JSON mode：<https://platform.openai.com/docs/guides/structured-outputs?api-mode=chat>；tool calling：<https://platform.openai.com/docs/guides/function-calling?api-mode=chat>；streaming：<https://platform.openai.com/docs/guides/streaming-responses?api-mode=chat>；vision input：<https://platform.openai.com/docs/guides/images-vision?api-mode=chat>。
- 保存渠道时，只会更新这次提交的 key；不会因为切換渠道模式而静默迁移整个旧配置。唯一会被**同步清理**的是執行时模型引用：如果 `LITELLM_MODEL`、`AGENT_LITELLM_MODEL`、`VISION_MODEL` 或 `LITELLM_FALLBACK_MODELS` 指向了当前已啟用渠道里已經不存在的模型，设置页会在保存前把这些失效引用清空/移除，避免執行时繼續指向无效模型；即使当前启用渠道没有任何可選模型，也会清理缺少 legacy Key 支撑的托管 provider 旧值。`cohere/*`、`google/*`、`xai/*` 这类直连模型仅用于说明历史 `direct-env` 相容保留语义，不等于可用性承诺，是否可用请按各厂商官方模型/API 文档再做實際驗證。
- 后端一致性依据：配置校验鏈路在 `SystemConfigService._validate_llm_runtime_selection`（`src/services/system_config_service.py`）中通过 `_uses_direct_env_provider`（`src/config.py`）判斷執行时来源；当前仅 `gemini`、`vertex_ai`、`anthropic`、`openai`、`deepseek` 属于托管 key provider，`cohere`、`google`、`xai` 不在该白名单中，因此会保留为直连模型。
- 回退方式也保持最小：把对应渠道模型列表改回去后重新选择主模型 / fallback，或直接用桌面端匯出備份 / 手动 `.env` 还原之前的 `LLM_*`、`LITELLM_MODEL`、`AGENT_LITELLM_MODEL`、`VISION_MODEL`、`LLM_TEMPERATURE` 即可，不需要额外跑迁移脚本。Web 端如需恢復配置，也可在启用管理员鉴权（`ADMIN_AUTH_ENABLED=true`）后通过 `POST /api/v1/system/config/import` 回滚。
- 当前倉庫对此鏈路的依賴約束是 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`（见 `requirements.txt`）；迴歸覆盖包括 `tests/test_system_config_service.py`、`tests/test_system_config_api.py` 和 `apps/dsa-web/src/components/settings/__tests__/LLMChannelEditor.test.tsx`。

> **外部 provider 示例模型说明**：`cohere/*`、`google/*`、`xai/*` 等 provider 前綴值仅用于说明当前保存清理语义，**不代表该依賴約束内的逐型号可用性保证**。文档或測試中的具体模型名都是配置保留行为样例，不是生产推荐；實際可用性请以对应官方模型文档为准，并结合倉庫依賴約束 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0` 复核。

### 回退与相容性证据

- 依賴約束与静默清理範圍：在 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0` 下，保存仅清理失效的 runtime 模型引用（`LITELLM_MODEL`、`AGENT_LITELLM_MODEL`、`VISION_MODEL`、`LITELLM_FALLBACK_MODELS`），`cohere/*`、`google/*`、`xai/*` 等非渠道直连模型会被保留。
- 回退方式：可直接用桌面端匯出備份后通过 `POST /api/v1/system/config/import` 恢復；也可手动把 `.env` 中历史 `LITELLM_* / AGENT_LITELLM_MODEL / VISION_MODEL / LLM_TEMPERATURE` 回填后重啟生效。Web 端執行匯入前请先开启管理员鉴权（`ADMIN_AUTH_ENABLED=true`）。
- 回退迴歸证据：`tests/test_system_config_service.py::test_import_desktop_env_restores_runtime_models_after_cleanup` 覆盖“清理后用桌面匯出備份恢復 runtime 引用”。
- 直连 provider 迴歸证据：`tests/test_system_config_service.py::SystemConfigServiceTestCase::test_validate_accepts_minimax_model_as_direct_env_provider`、`test_validate_accepts_cohere_model_as_direct_env_provider`、`test_validate_accepts_google_model_as_direct_env_provider`、`test_validate_accepts_xai_model_as_direct_env_provider` 覆盖直连 provider 保留语义。
- 前端迴歸命令：`cd apps/dsa-web && npm run lint && npm run build && npm run test -- src/components/settings/__tests__/LLMChannelEditor.test.tsx`。
- 建议回退操作鏈路（含设置页刷新）：先匯出桌面備份，`POST /api/v1/system/config/import` 匯入后，再通过 `GET /api/v1/system/config` 刷新页面配置，再确认 `LITELLM_MODEL / AGENT_LITELLM_MODEL / VISION_MODEL / LLM_TEMPERATURE` 与模型列表一致后再繼續使用。

### 常用官方文档来源（用于核对预设 provider / Base URL / 模型命名）

- OpenAI Compatible 規範（LiteLLM）：<https://docs.litellm.ai/docs/providers/openai_compatible>
- OpenAI 官方：<https://platform.openai.com/docs/api-reference/chat>
- DeepSeek 官方：<https://api-docs.deepseek.com/>
- Anspire Open：<https://open.anspire.cn/?share_code=QFBC0FYC>
- 阿里百炼 DashScope 相容模式：<https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope>
- Moonshot / Kimi 官方：<https://platform.moonshot.ai/docs/guide/compatibility>
- Anthropic 官方：<https://docs.anthropic.com/en/api/messages>
- Gemini 官方：<https://ai.google.dev/gemini-api/docs/openai>
- Cohere 官方：<https://docs.cohere.com/>
- Cohere API 參考：<https://docs.cohere.com/reference/>
- Cohere LiteLLM Provider：<https://docs.litellm.ai/docs/providers/cohere>
- Google Gemini API 与模型：<https://ai.google.dev/gemini-api/docs/openai>、<https://ai.google.dev/gemini-api/docs/models>
- Google LiteLLM Provider：<https://docs.litellm.ai/docs/providers/gemini>
- xAI 官方：<https://docs.x.ai/docs>
- xAI LiteLLM Provider：<https://docs.litellm.ai/docs/providers/xai>
- Ollama 官方：<https://github.com/ollama/ollama/blob/main/docs/api.md>

如果不方便用网页版，在 `.env` 文件中配置也非常丝滑，它能让你同时管理多个第三方平台。規則如下：

1. **先声明你有几个渠道**：`LLM_CHANNELS=渠道名称1,渠道名称2`
2. **给每个渠道分别填写配置**（注意全大写）：`LLM_{渠道名}_XXX`

### 示例：同时配置 DeepSeek 和某中转平台，并设置备用切換
```env
# 1. 开启渠道模式，声明这里有两个渠道：deepseek 和 aihubmix
LLM_CHANNELS=deepseek,aihubmix

# 2. 渠道一：配置 DeepSeek 官方
LLM_DEEPSEEK_BASE_URL=https://api.deepseek.com
LLM_DEEPSEEK_API_KEY=sk-1111111111111
LLM_DEEPSEEK_MODELS=deepseek-v4-flash,deepseek-v4-pro

# 3. 渠道二：配置一个常用的聚合中转 API
LLM_AIHUBMIX_BASE_URL=https://api.aihubmix.com/v1
LLM_AIHUBMIX_API_KEY=sk-2222222222222
LLM_AIHUBMIX_MODELS=gpt-5.5,claude-sonnet-4-6

# 4. 【關鍵】指定主模型和备用模型列表
# 平时首选用 deepseek 这款模型：
LITELLM_MODEL=deepseek/deepseek-v4-flash
# 可選：Agent 问股单独指定主模型（留空则继承主模型）
AGENT_LITELLM_MODEL=deepseek/deepseek-v4-pro
# 主模型崩了立刻挨个嘗試下面这俩备用模型：
LITELLM_FALLBACK_MODELS=openai/gpt-5.4-mini,anthropic/claude-sonnet-4-6
```

### 示例：Ollama 渠道模式（本機模型，無需 API Key）
```env
# 1. 开启渠道模式，声明 ollama 渠道
LLM_CHANNELS=ollama

# 2. 配置 Ollama 地址（本機預設 11434 端口）
LLM_OLLAMA_BASE_URL=http://localhost:11434
LLM_OLLAMA_MODELS=qwen3:8b,llama3.2

# 3. 指定主模型
LITELLM_MODEL=ollama/qwen3:8b
```

### MiniMax 渠道模型填写说明

- 如果你通过 OpenAI Compatible 渠道接 MiniMax，请在渠道模型里直接填写 `minimax/<模型名>`，例如 `minimax/MiniMax-M1`。
- Web 设置页里的主模型、Agent 主模型、Fallback、Vision 下拉会保留这个值原样展示，不会再錯誤改写成 `openai/minimax/<模型名>`。

### 问股 Agent / LiteLLM 配置相容说明

- 问股 Agent 執行时沿用与普通分析相同的三层優先级：`LITELLM_CONFIG`（LiteLLM YAML）> `LLM_CHANNELS` > legacy provider keys。只要上层配置有效生效，下层配置就不会再参与本次請求。
- YAML 模式下，Agent 直接复用 LiteLLM `model_list` / `model_name` 路由语义；渠道模式下，優先讀取 `AGENT_LITELLM_MODEL`，留空时继承 `LITELLM_MODEL`，再按 `LITELLM_FALLBACK_MODELS` 繼續 fallback。
- 如果你没有启用 YAML / Channels，且 `AGENT_LITELLM_MODEL` 也留空，但本機仍保留 legacy 環境變數，问股 Agent 依然会继承旧配置：`GEMINI_API_KEY + GEMINI_MODEL` -> `gemini/<model>`，`OPENAI_API_KEY + OPENAI_MODEL` -> `openai/<model>`，`ANTHROPIC_API_KEY + ANTHROPIC_MODEL` -> `anthropic/<model>`。
- 该相容邏輯只增强“失败时保留后端真实錯誤原因”和“未配置 LLM 时给出更具体診斷”，**不会**静默刪除、清空、迁移或改写你现有的 `GEMINI_*` / `OPENAI_*` / `ANTHROPIC_*` / `LITELLM_*` 配置。
- 如果当前環境没有任何有效 Agent 模型鏈路，问股页面会繼續按失败语义傳回，并直接展示后端真实配置診斷；补齐任一有效模型来源后即可恢復，無需额外執行配置迁移脚本。
- 推荐的新配置方式仍然是显式设置 `LITELLM_MODEL` / `AGENT_LITELLM_MODEL` 或使用 `LLM_CHANNELS`；legacy provider keys 目前保留为相容回退路徑，方便旧 `.env`、本機 macOS 开发環境和历史部署平滑繼續執行。

### 严格 temperature 模型相容说明

- Moonshot 官方说明 Kimi API 相容 OpenAI 介面，Base URL 使用 `https://api.moonshot.ai/v1`：<https://platform.kimi.ai/docs/guide/kimi-k2-6-quickstart>
- LiteLLM 官方要求 OpenAI Compatible 渠道模型名使用 `openai/` 前綴：<https://docs.litellm.ai/docs/providers/openai_compatible>
- Moonshot 官方相容性文档区分两种固定值：**thinking 模式固定 `1.0`，non-thinking 模式固定 `0.6`**；传其它值会被介面拒絕：<https://platform.moonshot.ai/docs/guide/compatibility#parameters-differences-in-request-body>
- OpenAI Chat Completions 規範中 `temperature` 是可選參數；对 GPT-5 / o 系列等只接受預設温度的模型，本项目会在請求层省略 `temperature`，让服務端使用預設值，而不是改写你的 `LLM_TEMPERATURE`：<https://platform.openai.com/docs/api-reference/chat/create>
- 当前倉庫的執行时依賴約束是 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`（见 `requirements.txt`）；本次相容邏輯按该約束迴歸驗證了主分析、大盤复盘、Agent 直连 LiteLLM，以及系統设置页的渠道連通性測試。
- 因此本项目会在請求发出前按**實際請求模式**归一化 `kimi-k2.6` 及其 `kimi-k2.6-*` 变体：預設 / thinking 路徑使用 `temperature=1.0`；如果你的 LiteLLM YAML 路由别名里显式写了 `litellm_params.extra_body.thinking.type: disabled`（或等价 non-thinking 配置），则自动切到 `temperature=0.6`。你在 `.env` 或 Web 设置里保存的 `LLM_TEMPERATURE` 不会被改写。
- 如果相容平台对未收录的新模型傳回明確的參數錯誤（例如 `temperature` 不支援、只能使用預設 `1.0`、`top_p` 不支援），執行时会对**当前請求**做一次參數修正并重試；只有重試成功后才把该策略快取在当前程式内。该快取不会写回 `.env`，服務重啟后会重新按配置与適配規則判斷。
- 对已經产生部分内容的流式回應，系統不会在半截輸出后切換參數；仍沿用原有“同模型非流式重試 / fallback 模型”的稳定路徑，避免拼接出不一致的回答。
- `SystemConfigService` 在 Web 设置保存 / 桌面端 `.env` 匯入时只更新你提交的 key，不会因为切到严格 temperature 模型静默清空、迁移或重写已有 `LLM_TEMPERATURE`；渠道測試請求里的暫時參數策略也不会回写到配置文件。
- 非严格主模型、非严格 fallback 以及切回普通模型后的請求，仍繼續使用你配置的温度；也就是说旧配置無需迁移，切換模型即可自动恢復原行为。
- 本倉庫相容性迴歸覆盖见：`tests/test_llm_channel_config.py`、`tests/test_market_analyzer_generate_text.py`、`tests/test_agent_pipeline.py`、`tests/test_system_config_service.py`。
- 最小回滚方式：直接回退本次 LLM 參數適配相關改动，無需单独迁移已有 `LLM_TEMPERATURE` 配置。

### 相容性与回退复核清单（按 PR 审核口径）

- 執行时依賴約束：`litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`（与 `requirements.txt` 一致）。
- 迴歸驗證入口：
  - 渠道模型发现与連線：`tests/test_llm_channel_config.py`
  - 執行时源清理与恢復（含桌面匯出備份鏈路）：`tests/test_system_config_service.py`
  - 介面校验与議題面向欄位：`tests/test_system_config_api.py`
  - 设置页交互与保存后提示：`apps/dsa-web/src/components/settings/__tests__/LLMChannelEditor.test.tsx`
- 旧配置回退路徑：`桌面端匯出備份 -> /api/v1/system/config/import`，或手动恢復 `LLM_* / LITELLM_* / AGENT_LITELLM_MODEL / VISION_MODEL / LLM_TEMPERATURE`；Web 匯入備份前同样要求 `ADMIN_AUTH_ENABLED=true`，否则会傳回 403。

> **致命避坑说明**：如果你启用了 `LLM_CHANNELS`，那么你直接写在外面的 `DEEPSEEK_API_KEY` 或 `OPENAI_API_KEY` 将**全部失效（系統一律无视）**！二者**选其一即可**，千万不要既写了新手模式又写了渠道模式结果产生冲突。
> **Docker 注意**：如果你在 `docker compose environment:` 或 `docker run -e` 中显式传入 `LITELLM_MODEL`、`LLM_CHANNELS`、`LLM_DEEPSEEK_MODELS` 等變數，容器重啟后这些環境變數会覆盖 Web 设置页写入的 `.env`，需要同步修改部署配置。

### 相容依据与回退审计说明（本次 PR 適配说明）

- 官方与執行时相容依据采用两层：第一层为官方介面语义（LiteLLM OpenAI-compatible 路由、OpenAI Chat Completions、Moonshot/Kimi 文档与官方模型说明）；第二层为本倉庫当前執行时语义（`litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`）下的實際錯誤归类。
- 本次相容恢復只使用“本機執行时錯誤归类 + 单請求修正重試 + 程式内快取”策略，不写入 `.env`、不做配置迁移，仅在執行路徑上动态规避不支援參數（`temperature`、`top_p`、`presence_penalty`、`frequency_penalty`、`seed`）。若要回退，不需要额外迁移命令，恢復旧值即可。
- 迴歸与证据：`tests/test_llm_param_recovery.py`、`tests/test_system_config_service.py`、`tests/test_llm_channel_config.py`、`tests/test_system_config_api.py`、`tests/test_market_analyzer_generate_text.py`、`tests/test_agent_pipeline.py`；桌面匯入与執行时清理回退另有 `test_import_desktop_env_restores_runtime_models_after_cleanup` 直接覆盖。

---

## 方式三：YAML 進階配置（适合老手自定义）

**目标：** 我不在乎學習门槛，我要最高控制权，我要用原生規則做企业级高可用！

这一层会直接映射到底层 LiteLLM 路由能力，支援高並行、自动重試、按 RPM/TPM 负载均衡等操作。

### 本機執行 / Docker 部署模式配置说明

1. 在 `.env` 中只保留一行指向声明：
   ```env
   LITELLM_CONFIG=./litellm_config.yaml
   ```
2. 在项目根目錄建立一个 `litellm_config.yaml`（可以參考自带的 `docs/examples/litellm_config.example.yaml`）。

示例 `litellm_config.yaml`：
```yaml
model_list:
  - model_name: my-smart-model
    litellm_params:
      model: deepseek/deepseek-v4-flash
      api_base: https://api.deepseek.com
      api_key: "os.environ/MY_CUSTOM_SECRET_KEY"  # 从環境變數讀取 Key，安全防泄漏

  # Ollama 本機模型（無需 api_key）
  - model_name: ollama/qwen3:8b
    litellm_params:
      model: ollama/qwen3:8b
      api_base: http://localhost:11434
```

### GitHub Actions配置说明

1. `Settings` → `Secrets and variables` → `Actions`。非敏感配置（如模型名、开关、Base URL）可以放在 `Secret` 或 `Variables`；凡是 `*_API_KEY` / `*_API_KEYS` 以及 `LLM_<NAME>_API_KEY` / `LLM_<NAME>_API_KEYS` 这类密钥欄位，请统一放在 `Secret` 標籤页的 `New repository secret`

2. 按下表配置，只有全部必填配置正确配置，YAML 進階配置模式才可以生效，YAML配置文件的写法，可以參考自带的 `docs/examples/litellm_config.example.yaml`

| Secret 名称 | 说明 | 必填 |
|------------|------|:----:|
| `LITELLM_CONFIG` | 進階模型路由配置文件路徑，通常配置 `./litellm_config.yaml` | 必填 |
| `LITELLM_MODEL` | 預設主模型名称或路由别名 | 必填 |
| `LITELLM_CONFIG_YAML` | 存放 YAML 配置文件内容，可不在倉庫中提交实体文件 | 可選 |
| `LITELLM_API_KEY` | 用于存储API Key，可在配置文件中引用（環境變數引用方式）。由于GitHub Actions必须要指定匯入的環境變數，因此你不能像本機執行模式那样自由命名環境變數 | 可選，必须配置到repository secret中 |
| `ANTHROPIC_API_KEY` | 如果要多个API Key，这个變數名称也能拿来用 | 可選，必须配置到repository secret中 |
| `OPENAI_API_KEY` | 同上，可以用来存储API Key | 可選，必须配置到repository secret中 |

渠道模式無需上傳 YAML 文件。倉庫自带 `daily_analysis.yml` 已显式透传以下常用欄位：

- 執行时选择：`LLM_CHANNELS`、`LITELLM_MODEL`、`LITELLM_FALLBACK_MODELS`、`AGENT_LITELLM_MODEL`、`VISION_MODEL`、`VISION_PROVIDER_PRIORITY`、`LLM_TEMPERATURE`
- 多 Key：`GEMINI_API_KEYS`、`ANTHROPIC_API_KEYS`、`OPENAI_API_KEYS`、`DEEPSEEK_API_KEYS`（当前 workflow 仅从 repository secrets 匯入，不会讀取同名 Variables）
- 常用渠道名：`primary`、`secondary`、`aihubmix`、`deepseek`、`dashscope`、`zhipu`、`moonshot`、`minimax`、`volcengine`、`siliconflow`、`openrouter`、`gemini`、`anthropic`、`openai`、`ollama`

例如在 GitHub Actions 中配置 `LLM_CHANNELS=primary,deepseek` 时，需同步配置 `LLM_PRIMARY_*` / `LLM_DEEPSEEK_*`。其中 `LLM_<NAME>_API_KEY` / `LLM_<NAME>_API_KEYS` 当前也仅从 repository secrets 匯入；如果你把这些值放在 Variables，執行时不会生效。若使用自定义渠道名（如 `my_proxy`），GitHub Actions 还必须在 workflow `env:` 中显式新增对应的 `LLM_MY_PROXY_*` 映射；本機 `.env` 和 Docker 不受这个限制。


> **三层配置互斥准则**：YAML 優先级最高！只要配置了 YAML，**渠道模式** 和 **新手极简模式** 统统被忽略。系統優先级为：`YAML配置 > 渠道模式 > 极簡單模型`。

---

## 扩展功能：看图模型 (Vision) 配置

系統中有些特定功能（比如上傳股票软件截图，让 AI 提取出截图里的股票代碼并放入自选股池）必须用到具备“视觉能力”的模型。你需在 `.env` 单独给它指派一个懂图片的模型。

```env
# 指定你看图专用的模型名
VISION_MODEL=openai/gpt-5.5
# 别忘了填写它对应提供商的 API KEY，如果是 OpenAI 相容渠道就提供 OPENAI_API_KEY：
# OPENAI_API_KEY=xxx
```

**备用看图機制：** 为了防止偶尔罢工，系統内置了切換策略。如果主视觉模型呼叫失败，它会按照下方的顺位嘗試寻找是否有其他看图模型的 Key：
```env
# 預設的备用顺序：
VISION_PROVIDER_PRIORITY=gemini,anthropic,openai
```

---

## 检测与排错 (Troubleshooting)

配好了之后心惊胆战不知道对不对？在命令行（Terminal）里敲入下面代碼帮你挂号问诊：

- `python scripts/check_env.py --config` ：纯检测 `.env` 配置文件里的邏輯写得对不对，是不是少写了什么。（秒出结果，不呼叫網路，纯檢查本機文本拼写）
- `python scripts/check_env.py --llm` ：系統会真的发一句问候语给大模型，让你亲眼看到他的回答。这能彻底测出你的**網路通不通、账号有没有欠费**。

### 常见踩坑答疑台

| 遇到了什么诡异报错？ | 罪魁祸首可能是啥？ | 该怎么收拾它？ |
|----------------------|----------------------|------------------|
| **界面提示主模型未配置** | 系統不知道你到底想用哪家的哪个模型 | 在 `.env` 中写上一句明白话：`LITELLM_MODEL=provider/你的模型名`。比如 `openai/gpt-5.5` |
| **我写了好几家的Key，为什么死活只有一个生效？修改还没用？** | 你把 **极简模式** 和 **渠道模式** 混着写了！ | 想好一条路走到黑——只要簡單就删掉 `LLM_CHANNELS` 开头的；想要丰富备用切換就要全部转投到 `LLM_CHANNELS` 下的编制里。 |
| **錯誤码报 400 或 401 或 Invalid API Key** | API Key 填错、少复制了一截、账号充值没到账、或者模型名字敲错（极度常见）。 | 1. 檢查复制的 Key 前后是否有误填空格。<br> 2. 檢查 Base URL 最后是不是少了一个 `/v1`。<br> 3. 檢查模型名是否少写了 `openai/` 之类的前綴！ |
| **Kimi K2.6 报 `invalid temperature`（可能提示只允許 `1.0` 或 `0.6`）** | 该模型按 thinking / non-thinking 模式要求不同固定 temperature；旧配置或呼叫入口可能还在传 `0.7`。 | 升級后系統会对 `kimi-k2.6` 預設 / thinking 請求自动使用 `temperature=1.0`；如果你在 LiteLLM YAML 路由里显式關閉 thinking，则自动改用 `0.6`。模型名建议写成 `openai/kimi-k2.6` 并配合 Moonshot / 聚合平台的 OpenAI 相容 Base URL 与 API Key。非 Kimi fallback 仍会繼續使用你配置的 `LLM_TEMPERATURE`。 |
| **GPT-5 / o 系列报 `temperature` 不支援或只允許預設值** | 这类模型只接受服務端預設採樣參數，但旧呼叫入口会显式传 `0.7`。 | 升級后請求层会省略 `temperature`，让服務端使用預設值；`.env` / Web 设置中的 `LLM_TEMPERATURE` 不会被改写，切回普通模型后仍按原值发送。 |
| **转圈转不停，最后报 Timeout / ConnectionRefused 等** | 1. 在国内使用国外原版（像 Google、OpenAI），没开代理被墙了。<br>2. 你买的云服務器压根不能出境。 | 非常推荐使用**国内官方**（如DeepSeek、阿里）或者各种**相容 OpenAI 的聚合中转介面**。因为中转站把網路議題帮你解決好了。 |
| **Ollama 报 404、`Could not get model info` 或 `api/generate/api/show`** | 误用 `OPENAI_BASE_URL` 配置 Ollama，系統会錯誤拼接 URL | 改用 `OLLAMA_API_BASE=http://localhost:11434` 或渠道模式（`LLM_CHANNELS=ollama` + `LLM_OLLAMA_BASE_URL`） |

*进阶老手的叮嘱：如果你开启了 **Agent (深度思考網路搜尋问股) 模式**，这里有个經驗之谈，推荐选用如 `deepseek-v4-pro` 这种邏輯推導能力更强的大模型。如果为了省钱用小微模型跑 Agent，它邏輯能力大機率跟不上，不仅达不到预期，还会白跑一堆空流程。*
