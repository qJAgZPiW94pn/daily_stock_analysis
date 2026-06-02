# ❓ 常见議題解答 (FAQ)

本文档整理了使用者在使用过程中遇到的常见議題及解决方案。

---

## 📊 數據相关

### Q1: 美股代碼（如 AMD, AAPL）分析时价格显示不正确？

**现象**：输入美股代碼后，显示的价格明显不对（如 AMD 显示 7.33 元），或被误识别为 A 股。

**原因**：早期版本代碼匹配逻辑优先尝试国内 A 股规则，导致代碼冲突。

**解决方案**：
1. 已在 v2.3.0 修复，系統现在支援美股代碼自动识别
2. 如仍有議題，可在 `.env` 中设置：
   ```bash
   YFINANCE_PRIORITY=0
   ```
   这将优先使用 Yahoo Finance 數據源获取美股數據

> 📌 相关 Issue: [#153](https://github.com/ZhuLinsen/daily_stock_analysis/issues/153)

---

### Q2: 报告中"量比"欄位显示为空或 N/A？

**现象**：分析报告中量比數據缺失，影响 AI 对缩放量的判断。

**原因**：默认的某些实时行情源（如新浪接口）不提供量比欄位。

**解决方案**：
1. 已在 v2.3.0 修复，腾讯接口现已支援量比解析
2. 推荐配置实时行情源优先级：
   ```bash
   REALTIME_SOURCE_PRIORITY=tencent,akshare_sina,efinance,akshare_em
   ```
3. 系統已内置 5 日均量计算作为兜底逻辑

> 📌 相关 Issue: [#155](https://github.com/ZhuLinsen/daily_stock_analysis/issues/155)

---

### Q3: Tushare 获取數據失败，提示 Token 不对？

**现象**：日誌显示 `Tushare 获取數據失败: 您的token不对，請確認`

**解决方案**：
1. **无 Tushare 账号**：無需配置 `TUSHARE_TOKEN`，系統会自动使用免费數據源（AkShare、Efinance）
2. **有 Tushare 账号**：确认 Token 是否正确，可在 [Tushare Pro](https://tushare.pro/weborder/#/login?reg=834638 ) 个人中心查看
3. 本项目所有核心功能均可在无 Tushare 的情况下正常執行

---

### Q4: 數據获取被限流或傳回为空？

**现象**：日誌显示 `熔断器触发` 或數據傳回 `None`，或出现 `RemoteDisconnected`、`push2his.eastmoney.com` 連線被關閉等

**原因**：免费數據源（东方财富、新浪等）有反爬机制，短时间大量請求会被限流。

**解决方案**：
1. 系統已内置多數據源自动切换和熔断保护
2. 减少自选股数量，或增加請求间隔
3. 避免频繁手动触发分析
4. 若东财接口频繁失败，可设置 `ENABLE_EASTMONEY_PATCH=true` 启用东财补丁（注入 NID 令牌与随机 User-Agent，降低被限流概率）
5. 将 `MAX_WORKERS=1` 改为串行获取，减少对东财的並行压力

---

## ⚙️ 配置相关

### Q5: GitHub Actions 執行失败，提示找不到环境變數？

**现象**：Actions 日誌显示 `GEMINI_API_KEY` 或 `STOCK_LIST` 未定义

**原因**：GitHub 区分 `Secrets`（加密）和 `Variables`（普通變數），配置位置不对会导致读取失败。

**解决方案**：
1. 进入倉庫 `Settings` → `Secrets and variables` → `Actions`
2. **Secrets**（点击 `New repository secret`）：存放敏感資訊
   - `GEMINI_API_KEY`
   - `OPENAI_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - 各类 Webhook URL
3. **Variables**（点击 `Variables` 標籤）：存放非敏感配置
   - `STOCK_LIST`
   - `GEMINI_MODEL`
   - `REPORT_TYPE`

---

### Q6: 修改 .env 文件后配置没有生效？

**解决方案**：
1. 确保 `.env` 文件位于项目根目錄
2. **Docker 部署 / WebUI 系統设置**：
   - WebUI 保存后的 `STOCK_LIST`、`SCHEDULE_ENABLED`、`SCHEDULE_TIME`、`SCHEDULE_RUN_IMMEDIATELY`、`RUN_IMMEDIATELY` 会写回容器内的 `.env`
   - WebUI 保存后会触发当前程式的配置重载；執行中的读取路徑会同步使用最新写回的 `.env`，例如定时工作会繼續热读取保存后的 `STOCK_LIST`
   - 如果容器啟動命令里显式传入了这些同名环境變數（如 `docker run -e ...` 或 Compose `environment:`），后续重啟时仍以显式程式环境變數为准；要让 WebUI 保存值接管，请同步更新或移除这些显式 override
   - 其中 `SCHEDULE_*` 与 `RUN_IMMEDIATELY` 属于**啟動期调度配置**，保存后不会立即触发一次分析，也不会热重建当前程式里的 scheduler
   - 如需让调度开关立刻接管当前容器，请重啟容器，并确保以 schedule 模式啟動
3. **Docker 手工改 `.env` 后**：修改后仍建议重啟容器
   ```bash
   docker-compose down && docker-compose up -d
   ```
4. **GitHub Actions**：`.env` 文件不生效，必须在 Secrets/Variables 中配置
5. 检查是否有多个 `.env` 文件（如 `.env.local`）导致覆盖

---

### Q7: 如何配置代理访问 Gemini/OpenAI API？

**解决方案**：

在 `.env` 中配置：
```bash
USE_PROXY=true
PROXY_HOST=127.0.0.1
PROXY_PORT=10809
```

> ⚠️ 注意：代理配置仅对本機執行生效，GitHub Actions 环境無需配置代理。

---

### LLM 配置常见議題

> 完整说明见 [LLM 配置指南](LLM_CONFIG_GUIDE.md)。

**Q: 配置了 GEMINI_API_KEY 和 LLM_CHANNELS，为什么只用渠道？**

系統按优先级只取一种：高级模型路由 YAML（`LITELLM_CONFIG`）> `LLM_CHANNELS` > legacy keys。但 YAML 仅在文件可正常解析且产出了有效 `model_list` 时才生效；如果 YAML 路徑无效或内容为空，系統会自动回退到 `LLM_CHANNELS` 或 legacy keys。一旦某一层级实际生效，更低优先级的配置不参与解析。

**Q: check_env 输出“未配置可用 AI 模型”怎么办？**

默认先选一种服務商并填写对应 API Key；如果需要固定主模型，再补 `LITELLM_MODEL=provider/model`；如果要多模型切换，再配置 `LLM_CHANNELS` 或高级模型路由 YAML。執行 `python scripts/check_env.py --config` 校验配置，`python scripts/check_env.py --llm` 实际调用 API 測試。

**Q: 如何同时使用多个模型（如 AIHubmix + DeepSeek + Gemini）？**

使用渠道模式：设置 `LLM_CHANNELS=aihubmix,deepseek,gemini`，并配置各渠道的 `LLM_{NAME}_BASE_URL`、`LLM_{NAME}_API_KEY`、`LLM_{NAME}_MODELS`。也可在 Web 设置页 → AI 模型 → AI 模型接入 中可视化配置。

**Q: 问股/Agent 提示未配置可用 LLM，但我只有旧的 `GEMINI_*` / `OPENAI_*` / `ANTHROPIC_*` 配置，怎么办？**

先确认当前是否启用了 `LITELLM_CONFIG` 或 `LLM_CHANNELS`；如果启用了，上层配置会覆盖 legacy keys。若你没有启用这两层，且 `AGENT_LITELLM_MODEL` 为空，问股 Agent 仍会自动继承 legacy provider 模型：`GEMINI_MODEL`、`OPENAI_MODEL`、`ANTHROPIC_MODEL` 分别映射到对应 provider 前缀的 LiteLLM 模型名。此次修复不会静默迁移或清空旧配置，只是把“真实缺失原因”直接傳回到前端，便于你判断到底是缺 key、缺模型名，还是被上层配置覆盖。完整兼容语义见 [LLM 配置指南](LLM_CONFIG_GUIDE.md) 中“问股 Agent / LiteLLM 配置兼容说明”。

---

## 📱 推送相关

### Q8: 机器人推送失败，提示訊息过长？

**现象**：分析成功但未收到推送，日誌显示 400 錯誤或 `Message too long`

**原因**：不同平台訊息长度限制不同：
- 企业微信：4KB
- 飞书：20KB
- 钉钉：20KB

**解决方案**：
1. **自动分块**：最新版本已实现长訊息自动切割
2. **单股推送模式**：设置 `SINGLE_STOCK_NOTIFY=true`，每分析完一只股票立即推送
3. **精简报告**：设置 `REPORT_TYPE=simple` 使用精简格式

---

### Q9: Telegram 推送收不到訊息？

**解决方案**：
1. 确认 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID` 都已配置
2. 获取 Chat ID 方法：
   - 给 Bot 发送任意訊息
   - 访问 `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - 在傳回的 JSON 中找到 `chat.id`
3. 确保 Bot 已被添加到目标群組（如果是群聊）
4. 本機執行时需要能访问 Telegram API（可能需要代理）

---

### Q10: 企业微信 Markdown 格式显示不正常？

**解决方案**：
1. 企业微信对 Markdown 支援有限，可尝试设置：
   ```bash
   WECHAT_MSG_TYPE=text
   ```
2. 这将发送纯文本格式的訊息

---

## 🤖 AI 模型相关

### Q11: Gemini API 傳回 429 錯誤（請求过多）？

**现象**：日誌显示 `Resource has been exhausted` 或 `429 Too Many Requests`

**解决方案**：
1. Gemini 免费版有速率限制（约 15 RPM）
2. 减少同时分析的股票数量
3. 增加請求延遲：
   ```bash
   GEMINI_REQUEST_DELAY=5
   ANALYSIS_DELAY=10
   ```
4. 或切换到 OpenAI 兼容 API 作为备选

---

### Q12: 如何使用 DeepSeek 等国产模型？

**配置方法**：

```bash
# 不需要配置 GEMINI_API_KEY
OPENAI_API_KEY=sk-xxxxxxxx
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-v4-flash
# deepseek-chat / deepseek-reasoner 仍兼容，但官方已标记为 2026/07/24 后废弃
```

支援的模型服務：
- DeepSeek: `https://api.deepseek.com`
- 通义千问: `https://dashscope.aliyuncs.com/compatible-mode/v1`
- Moonshot: `https://api.moonshot.cn/v1`

---

### Q12b: 如何使用 Ollama 本機模型？

**配置方法**：使用 `OLLAMA_API_BASE` + `LITELLM_MODEL`，或渠道模式（`LLM_CHANNELS=ollama` + `LLM_OLLAMA_BASE_URL` + `LLM_OLLAMA_MODELS`）。

**避坑**：不要使用 `OPENAI_BASE_URL` 配置 Ollama，否则系統会錯誤拼接 URL（如 404、`api/generate/api/show`）。详见 [LLM 配置指南](LLM_CONFIG_GUIDE.md) 示例 4 与渠道示例。

---

### Q12c: 執行时报 `OllamaException / APIConnectionError`（All LLM models failed）怎么办？

**症状**：日誌出现 `litellm.APIConnectionError: OllamaException` 或 `Analysis failed: All LLM models failed (tried 1 model(s))`。

逐项排查以下 5 个检查点：

1. **Ollama 服務是否已啟動**
   ```bash
   # 查看程式
   pgrep -a ollama
   # 若无输出则先啟動
   ollama serve
   ```
   确认服務正在监听：`curl http://localhost:11434`，应傳回 `Ollama is running`。

2. **`OLLAMA_API_BASE` 是否配置正确**
   - ✅ 正确：`OLLAMA_API_BASE=http://localhost:11434`
   - ❌ 錯誤：把 Ollama 地址填到 `OPENAI_BASE_URL`，会导致 URL 路徑拼错（如 `…/api/generate/api/show`）。

3. **模型名称是否加了 `ollama/` 前缀**
   - ✅ 正确：`LITELLM_MODEL=ollama/qwen3:8b`
   - ❌ 錯誤：`LITELLM_MODEL=qwen3:8b`（缺少前缀，litellm 无法路由到 Ollama）

4. **模型是否已下載到本機**
   ```bash
   ollama list          # 查看已有模型
   ollama pull qwen3:8b # 如无则先拉取
   ```

5. **遠端部署 / Docker 时的網路与防火墙**
   - 若 Ollama 和程式不在同一主机，需将 `OLLAMA_API_BASE` 改为实际 IP，如 `http://192.168.1.100:11434`。
   - 确认防火墙已放行 11434 端口，且 Ollama 啟動时绑定了正确地址（`OLLAMA_HOST=0.0.0.0:11434`）。

> 完整配置示例见 [LLM 配置指南 → 示例 4（Ollama）](LLM_CONFIG_GUIDE.md#example-4-ollama)。

---

## 🐳 Docker 相关

### Q13: Docker 容器啟動后立即退出？

**解决方案**：
1. 查看容器日誌：
   ```bash
   docker logs <container_id>
   ```
2. 常见原因：
   - 环境變數未正确配置
   - `.env` 文件格式錯誤（如有多余空格）
   - 依賴包版本冲突

---

### Q14: Docker 中 API 服務无法访问？

**解决方案**：
1. 确保啟動命令包含 `--host 0.0.0.0`（不能是 127.0.0.1）
2. 检查端口映射是否正确：
   ```yaml
   ports:
     - "8000:8000"
   ```

---

### Q14.1: Docker 中網路/DNS 解析失败（如 api.tushare.pro、searchapi.eastmoney.com 无法解析）？

**现象**：日誌显示 `Temporary failure in name resolution` 或 `NameResolutionError`，股票數據 API 和大模型 API 均无法访问。

**原因**：自定义 bridge 網路下，容器使用 Docker 内置 DNS，在旁路由、特定網路环境时可能解析失败。

**解决方案**（按优先级尝试）：

1. **显式配置 DNS**：在 `docker/docker-compose.yml` 的 `x-common` 下添加：
   ```yaml
   dns:
     - 223.5.5.5
     - 119.29.29.29
     - 8.8.8.8
   ```
   然后执行 `docker-compose down` 和 `docker-compose up -d --force-recreate` 重新建立容器。

2. **改用 host 網路模式**：若上述仍无效，可在 `server` 服務下添加 `network_mode: host`，并移除 `ports` 映射。使用 host 模式时，`ports` 无效，**端口由 `command` 中的 `--port` 指定**。若宿主机默认端口已占用，可修改为其他端口（如 `.env` 中设置 `API_PORT=8080`），访问对应 `http://localhost:8080`。

> 📌 相关 Issue: [#372](https://github.com/ZhuLinsen/daily_stock_analysis/issues/372)

---

### Q14.2: Docker 安裝时，软件版本号写在哪个文件里？

**结论**：对 Docker 使用者来说，**最权威的版本不是某个 Python 源文件常量，而是你实际使用的镜像 tag**。

**为什么**：
1. 倉庫的 Docker 發佈由 `.github/workflows/docker-publish.yml` 触发，只有推送 `v*.*.*` 形式的 Git tag（例如 `v3.12.0`）时才会生成对应發佈镜像。
2. 这意味着 Docker 镜像版本本质上跟随 **GitHub Release / Git tag**，而不是写死在 `main.py`、`server.py` 或其他后端源码里。
3. `apps/dsa-web/package.json` 里的 `version` 当前是占位值 `0.0.0`，WebUI “版本資訊”卡片更适合用来确认静态资源是否已重建，不应当作 Docker 發佈版本。
4. 桌面端版本是单独维护的，写在 `apps/dsa-desktop/package.json` 的 `version` 欄位；它只代表 Electron 桌面端，不代表 Docker 镜像版本。

**怎么查当前 Docker 版本**：
1. **先看部署命令或 Compose 文件里的镜像 tag**：例如 `ghcr.io/zhulinsen/daily_stock_analysis:v3.12.0`，其中 `v3.12.0` 就是当前部署版本。
2. **如果你拉的是 `latest`**：请回看当时的 `docker pull` / `docker-compose.yml` / 部署脚本，或对照 [GitHub Releases](https://github.com/ZhuLinsen/daily_stock_analysis/releases) 确认对应發佈记录。
3. **如果只是想确认前端是否更新到新构建**：可以打开 WebUI 的“系統设置”页查看 `构建标识` / `构建时间`；这能帮助确认静态资源是否刷新，但不等同于 Docker 镜像發佈版本。

**建议**：如果你想避免重复更新，部署时尽量固定使用明确的版本 tag（如 `v3.12.0`），不要长期依賴 `latest`。

---

## 🔧 其他議題

### Q15: 如何只執行大盤复盘，不分析個股？

**方法**：
```bash
# 本機執行
python main.py --market-only

# GitHub Actions
# 手动触发时选择 mode: market-only
```

---

### Q16: 分析结果中買入/观望/賣出数量统计不对？

**原因**：早期版本使用正则匹配统计，可能与实际建议不一致。

**解决方案**：已在最新版本中修复，AI 模型现在会直接输出 `decision_type` 欄位用于准确统计。

---

### Q17: 为什么週末在 GitHub Actions 手动触发仍显示“非交易日略過”？

**现象**：已经配置了 `TRADING_DAY_CHECK_ENABLED` 或希望手动執行，但日誌仍提示“今日所有相关市场均为非交易日，略過执行”。

**解决方案**：
1. 打开 `Actions → 每日股票分析 → Run workflow`
2. 手动触发时将 `force_run` 设为 `true`（单次强制執行）
3. 如果希望长期關閉交易日检查，在 `Settings → Secrets and variables → Actions` 中设置：
   ```bash
   TRADING_DAY_CHECK_ENABLED=false
   ```

**规则说明**：
- `TRADING_DAY_CHECK_ENABLED=true` 且 `force_run=false`：非交易日略過（默认）
- `force_run=true`：本次即使非交易日也执行
- `TRADING_DAY_CHECK_ENABLED=false`：定时和手动都不做交易日检查

---

## 💬 还有議題？

如果以上内容没有解决你的議題，欢迎：
1. 查看 [完整配置指南](full-guide.md)
2. 搜索或提交 [GitHub Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues)
3. 查看 [更新日誌](CHANGELOG.md) 了解最新修复

---

*最后更新：2026-04-20*
