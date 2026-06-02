# openclaw Skill 集成指南

本文档说明如何通过 [openclaw](https://github.com/openclaw/openclaw) Skill 呼叫 daily_stock_analysis 的 REST API，實現在 openclaw 对话中触发股票分析的能力。

## 概述

- **集成方式**：openclaw Skill 通过 HTTP 呼叫 daily_stock_analysis（DSA）REST API
- **适用場景**：已部署 DSA API 服務，希望在 openclaw 对话中触发分析（如「帮我分析茅台」「analyze AAPL」）

## 前置條件

1. **daily_stock_analysis 必须已執行**：執行 `python main.py --serve-only` 或通过 Docker 部署，使 API 长期可用
2. **openclaw 需具备 HTTP 呼叫能力**：如 `system.run` 執行 curl，或内置 HTTP 工具（如 api-tester 等）
3. **说明**：GitHub Actions 仅做定时工作，不长期暴露 API，需本機或 Docker 執行 DSA

## 核心 API 參考

| 介面 | 方法 | 用途 |
|------|------|------|
| `/api/v1/analysis/analyze` | POST | 触发分析（主入口） |
| `/api/v1/analysis/status/{task_id}` | GET | 非同步工作狀態 |
| `/api/v1/agent/chat` | POST | Agent 策略问股（需 `AGENT_MODE=true`） |
| `/api/health` | GET | 健康檢查 |

### 触发分析請求体

```json
{
  "stock_code": "600519",
  "report_type": "detailed",
  "force_refresh": true,
  "async_mode": false
}
```

- `stock_code`：股票代碼（必填）
- `report_type`：`simple` | `detailed` | `brief`
- `force_refresh`：布尔值，是否強制刷新（忽略快取）
- `async_mode`：布尔值，`false` 时同步傳回，`true` 时傳回 202 + `task_id` 需轮询

**注意**：`force_refresh`、`async_mode` 为布尔类型，非字符串。

### 回應示例（同步模式）

```json
{
  "query_id": "abc123def456",
  "stock_code": "600519",
  "stock_name": "贵州茅台",
  "report": {
    "summary": {
      "analysis_summary": "...",
      "operation_advice": "持有",
      "trend_prediction": "看多",
      "sentiment_score": 75
    },
    "strategy": {
      "ideal_buy": "1850",
      "stop_loss": "1780",
      "take_profit": "1950"
    }
  },
  "created_at": "2026-03-13T10:00:00"
}
```

## 重要限制与说明

- **仅支援股票代碼**：API 不接受中文名称（如「茅台」），需在 Skill 侧解析或提示使用者提供代碼（如 600519、AAPL）
- **同步模式耗时**：`async_mode: false` 时，单次分析约 2–5 分钟，需確保 openclaw 或 HTTP 客户端逾時足够
- **非同步模式**：`async_mode: true` 傳回 202 + `task_id`，需轮询 `GET /api/v1/analysis/status/{task_id}` 直至 `status: completed`

## 股票代碼格式

| 类型 | 格式 | 示例 |
|------|------|------|
| A股 | 6位数字 | `600519`、`000001`、`300750` |
| 北交所 | 8/4/92 开头 6 位，支援 `BJ` 前綴或 `.BJ` 后缀 | `920748`、`BJ920493`、`920493.BJ` |
| 港股 | hk + 5位数字 | `hk00700`、`hk09988` |
| 美股 | 1-5 字母（可選 .X 后缀） | `AAPL`、`TSLA`、`BRK.B` |
| 美股指數 | SPX/DJI/IXIC 等 | `SPX`、`DJI`、`NASDAQ`、`VIX` |

## 配置方式

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "entries": {
      "daily-stock-analysis": {
        "enabled": true,
        "env": {
          "DSA_BASE_URL": "http://localhost:8000"
        }
      }
    }
  }
}
```

- 本機部署：`http://localhost:8000` 或 `http://127.0.0.1:8000`
- 遠端部署：替換为實際 URL
- **建议**：`DSA_BASE_URL` 勿以 `/` 结尾

## 錯誤回應格式

| 狀態码 | error 欄位 | 说明 |
|--------|-------------|------|
| 400 | `validation_error` | 參數錯誤（如缺少 stock_code） |
| 409 | `duplicate_task` | 该股票正在分析中，拒絕重复提交 |
| 500 | `internal_error` / `analysis_failed` | 分析过程发生錯誤 |

## 完整 SKILL.md 示例

将以下内容保存到 `~/.openclaw/skills/daily-stock-analysis/SKILL.md`：

```markdown
---
name: daily-stock-analysis
description: 呼叫 daily_stock_analysis API 進行股票智能分析。当使用者询问「分析茅台」「analyze AAPL」「帮我看看 600519」等时使用。仅支援股票代碼，不支援中文名称。
metadata:
  {"openclaw": {"requires": {"env": ["DSA_BASE_URL"]}, "primaryEnv": "DSA_BASE_URL"}}
---

## 触发條件

当使用者請求分析某只股票时（如「分析茅台」「analyze AAPL」「帮我看看 600519」），使用本 Skill。

## 工作流程

1. **提取股票代碼**：从使用者訊息中识别股票代碼（如 600519、AAPL、hk00700）。若使用者仅提供中文名称（如「茅台」），需提示使用者提供股票代碼，或使用常见映射（茅台→600519）。
2. **呼叫 API**：向 `{DSA_BASE_URL}/api/v1/analysis/analyze` 发送 POST 請求，請求体：
   ```json
   {"stock_code": "<提取的代碼>", "report_type": "detailed", "force_refresh": true, "async_mode": false, "skills": ["bull_trend"]}
   ```
   > `skills` 为可選策略 ID 数组；历史欄位 `strategies` 仍保留相容，建议優先使用 `skills`。
3. **等待回應**：同步模式下分析约需 2–5 分钟，请確保 HTTP 客户端逾時足够（建议 ≥300 秒）。
4. **解析结果**：从回應的 `report.summary` 中提取 `operation_advice`、`trend_prediction`、`analysis_summary`，从 `report.strategy` 中提取 `ideal_buy`、`stop_loss`、`take_profit`，以简洁格式呈现给使用者。
5. **錯誤處理**：
   - 連線失败：提示檢查 DSA 是否執行、DSA_BASE_URL 是否正确
   - 400：檢查 stock_code 格式
   - 409：该股票正在分析中，可稍后重試或查詢工作狀態
   - 500：提示查看 DSA 日誌排查

## 股票代碼格式

- A股：6位数字（600519、000001）
- 北交所：8/4/92 开头 6 位，支援 BJ 前綴或 .BJ 后缀（920748、BJ920493、920493.BJ）
- 港股：hk + 5位数字（hk00700）
- 美股：1–5 字母（AAPL、TSLA、BRK.B）
- 美股指數：SPX、DJI、IXIC 等
```

## Agent 策略问股（可選）

若 daily_stock_analysis 已啟用 `AGENT_MODE=true`，可呼叫 Agent 策略问股介面，支援多轮对话与多种策略（缠论、均线金叉等）：

```bash
# 将 {DSA_BASE_URL} 替換为實際配置的 API 地址（如 http://localhost:8000）
curl -X POST {DSA_BASE_URL}/api/v1/agent/chat \
  -H 'Content-Type: application/json' \
  -d '{"message": "用缠论分析 600519", "session_id": "optional-session-id"}'
```

回應包含 `content`（分析结论）和 `session_id`（用于多轮对话）。

## 故障排查

| 現象 | 可能原因 | 處理建议 |
|------|----------|----------|
| 連線失败 | DSA 未執行、端口錯誤、防火墙 | 确认 `python main.py --serve-only` 已啟動，檢查 `DSA_BASE_URL` |
| 400 錯誤 | stock_code 格式錯誤或缺失 | 檢查代碼格式（见上文表格），確保請求体包含 `stock_code` |
| 500 錯誤 | AI 配置、數據源、網路議題 | 查看 DSA 日誌，确认 GEMINI_API_KEY 等已配置 |
| Agent 400 | Agent 模式未启用 | 在 DSA 的 `.env` 中设置 `AGENT_MODE=true` |
| 分析逾時 | 同步模式等待时间过长 | 增加 HTTP 客户端逾時，或改用 `async_mode: true` 轮询狀態 |

## 認證说明

預設情况下 DSA API 無需認證。若在 `.env` 中启用了 `ADMIN_AUTH_ENABLED=true`，则需在 Skill 呼叫时携带登录后获得的 Cookie，具体方式取决于 openclaw 的 HTTP 工具能力（当前 API 仅支援 Cookie 認證，不支援 Bearer Token）。
