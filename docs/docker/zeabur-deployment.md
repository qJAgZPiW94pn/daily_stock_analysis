# Zeabur 部署指南

本指南詳細介绍如何在 Zeabur 上部署 A股自选股智能分析系統，包括 WebUI 和 Discord 机器人功能。

## 目錄

- [1. 部署前准备](#1-部署前准备)
- [2. 在 Zeabur 上部署](#2-在-zeabur-上部署)
- [3. 配置啟動命令](#3-配置啟動命令)
- [4. Discord 机器人部署](#4-discord-机器人部署)
- [5. 環境變數配置](#5-環境變數配置)
- [6. 挂载配置](#6-挂载配置)
- [7. 健康檢查](#7-健康檢查)
- [8. 常见議題](#8-常见議題)

## 1. 部署前准备

### 1.1 必要條件

- Zeabur 账号
- GitHub 账号（用于連線倉庫）
- Discord 开发者账号（如需部署机器人）
- 相關 API 密钥（如 Gemini API Key、搜尋服務 API Key 等）

### 1.2 倉庫准备

確保你的倉庫包含以下文件：

- `.github/workflows/docker-publish.yml`（已自动建立）
- `docker/Dockerfile`（已存在）
- 完整的项目代碼

## 2. 在 Zeabur 上部署

### 2.1 連線 GitHub 倉庫

1. 登录 Zeabur 控制台
2. 点击「新建项目」
3. 选择「从 GitHub 匯入」
4. 选择你的倉庫和分支（推荐使用 `main` ）
5. 点击「匯入」

### 2.2 配置构建規則

Zeabur 会自动检测 `.github/workflows/docker-publish.yml` 文件，并使用 GitHub Actions 构建镜像。

如果没有自动检测到，可以手动配置：

1. 在项目页面，点击「构建規則」
2. 选择「Dockerfile」
3. Dockerfile 路徑填写：`docker/Dockerfile`
4. 点击「保存」

### 2.3 啟動服務

1. 等待镜像构建完成
2. 点击「啟動服務」
3. 服務啟動后，你可以在「訪問」標籤页獲取訪問地址

### 2.4 前端构建与静态资源

FastAPI 会自动托管 `static/` 目錄下的前端资源。前端打包輸出位置由
`apps/dsa-web/vite.config.ts` 决定，預設輸出到项目根目錄 `static/`。

Dockerfile 已采用多阶段构建，前端会在镜像构建时自动打包。
如需覆盖預設静态资源，可在宿主机手动构建并挂载到容器内 `/app/static`。

## 3. 配置啟動命令

### 3.1 支援的啟動模式

系統支援多种啟動模式，你可以根据需要配置不同的啟動命令：

| 模式 | 啟動命令 | 描述 |
|------|----------|------|
| 定时工作模式（預設） | `python main.py --schedule` | 按计划執行股票分析 |
| FastAPI 模式 | `python main.py --serve` | 啟動 FastAPI 并執行分析 |
| 仅 FastAPI 模式 | `python main.py --serve-only` | 仅啟動 FastAPI，不執行分析 |
| 仅大盤复盘 | `python main.py --market-review` | 仅執行大盤复盘分析 |

### 3.2 配置啟動命令

1. 在 Zeabur 控制台，进入服務页面
2. 点击「设置」
3. 找到「啟動命令」配置项
4. 輸入你需要的啟動命令，例如：
    - 啟動 FastAPI：`python main.py --serve`
    - 仅啟動 FastAPI：`python main.py --serve-only --host 0.0.0.0 --port 8000`
    - 啟動定时工作：`python main.py --schedule`
5. 点击「保存」
6. 重啟服務

## 4. Discord 机器人部署

### 4.1 准备工作

1. 建立 Discord 应用和机器人
   - 訪問 [Discord 开发者平台](https://discord.com/developers/applications)
   - 点击「New Application」建立新应用
   - 在「Bot」標籤页，点击「Add Bot」建立机器人
   - 复制机器人 Token

2. 配置机器人權限
   - 在「Bot」標籤页，向下滚动到「Privileged Gateway Intents」
   - 启用「Server Members Intent」和「Message Content Intent」
   - 在「OAuth2」→「URL Generator」中，选择「bot」範圍
   - 选择所需權限（如「Send Messages」、「Read Messages/View Channels」等）
   - 复制生成的邀请链接，将机器人添加到你的服務器

### 4.2 配置環境變數

在 Zeabur 控制台的「環境變數」配置中，添加以下變數：

| 變數名 | 说明 | 示例值 |
|--------|------|--------|
| `DISCORD_BOT_TOKEN` | Discord 机器人 Token | `MTAxMjM0NTY3ODkwMTEyMzQ1Ng.GhIjKl.MnOpQrStUvWxYz1234567890` |
| `DISCORD_MAIN_CHANNEL_ID` | 主频道 ID | `123456789012345678` |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL（可選） | `https://discord.com/api/webhooks/...` |

### 4.3 啟動机器人

机器人功能預設通过配置启用，無需特殊啟動命令。確保你的配置文件中包含机器人相關配置，或通过環境變數设置。

## 5. 環境變數配置

### 5.1 基本環境變數

| 變數名 | 说明 | 預設值 |
|--------|------|--------|
| `PYTHONUNBUFFERED` | 启用 Python 无缓冲輸出 | `1` |
| `LOG_DIR` | 日誌目錄 | `/app/logs` |
| `DATABASE_PATH` | 資料庫路徑 | `/app/data/stock_analysis.db` |

### 5.2 API 服務配置

| 變數名 | 说明 | 預設值 |
|--------|------|--------|
| `API_HOST` | API 服務监听地址 | `0.0.0.0` |
| `API_PORT` | API 服務端口 | `8000` |

> 旧版 `WEBUI_HOST`/`WEBUI_PORT`/`WEBUI_ENABLED` 環境變數仍相容，会自动轉發到 API 服務。

### 5.3 分析相關配置

| 變數名 | 说明 |
|--------|------|
| `ANSPIRE_API_KEYS` | Anspire Open API 密钥（大模型与搜尋共用，推荐） |
| `AIHUBMIX_KEY` | AIHubMix API 密钥（一 Key 多模型，推荐） |
| `GEMINI_API_KEY` | Gemini API 密钥 |
| `OPENAI_API_KEY` | OpenAI 相容 API 密钥 |
| `SERPAPI_API_KEYS` | SerpAPI 密钥（推荐） |
| `TAVILY_API_KEYS` | Tavily API 密钥（用逗号分隔） |
| `BOCHA_API_KEYS` | Bocha API 密钥（用逗号分隔） |
| `BRAVE_API_KEYS` | Brave Search API 密钥（用逗号分隔） |
| `MINIMAX_API_KEYS` | MiniMax API 密钥（用逗号分隔） |
| `SEARXNG_BASE_URLS` | SearXNG 实例地址（逗号分隔，无配額兜底，需在 settings.yml 启用 format: json）；留空时預設自动发现公共实例 |
| `SEARXNG_PUBLIC_INSTANCES_ENABLED` | 是否在 `SEARXNG_BASE_URLS` 为空时自动从 `searx.space` 獲取公共实例（預設 `true`） |

### 5.4 配置方法

在 Zeabur 控制台：

1. 进入服務页面
2. 点击「環境變數」
3. 点击「添加環境變數」
4. 輸入變數名和值
5. 点击「保存」
6. 重啟服務

## 6. 挂载配置

### 6.1 支援的挂载目錄

| 目錄 | 说明 |
|------|------|
| `/app/data` | 資料庫和數據文件 |
| `/app/logs` | 日誌文件 |
| `/app/reports` | 分析报告 |

### 6.2 配置挂载

1. 在 Zeabur 控制台，进入服務页面
2. 点击「存储」
3. 点击「添加存储卷」
4. 选择「持久化存储」
5. 配置挂载路徑：
   - 存储卷路徑：`/app/data`
   - 容器内路徑：`/app/data`
6. 点击「保存」
7. 对其他需要挂载的目錄重复上述步骤

### 6.3 注意事项

- 挂载后，數據会持久化保存，不会因容器重啟而丢失
- 建议至少挂载 `/app/data` 目錄，以保存資料庫

## 7. 健康檢查

系統内置了健康檢查機制，預設檢查：

- WebUI 模式：檢查 `http://localhost:8000/health` 端点
- FastAPI 模式：檢查 `http://localhost:8000/api/health` 端点
- 非服務模式：始终傳回健康狀態

健康檢查配置如下：

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || curl -f http://localhost:8000/health \
    || python -c "import sys; sys.exit(0)"
```

## 8. 常见議題

### 8.1 API 服務無法訪問

- 檢查啟動命令是否包含 `--serve` 或 `--serve-only` 參數
- 檢查「訪問」標籤页是否已配置域名
- 檢查防火墙设置

### 8.2 机器人不回應

- 檢查 Discord 机器人 Token 是否正确
- 檢查机器人是否已添加到服務器
- 檢查机器人權限是否足够
- 檢查日誌文件，查看是否有錯誤資訊

### 8.3 分析工作不執行

- 檢查定时工作配置是否正确
- 檢查 API 密钥是否有效
- 檢查日誌文件，查看是否有錯誤資訊

### 8.4 數據丢失

- 確保已挂载 `/app/data` 目錄
- 檢查存储卷配置是否正确

## 9. 進階配置

### 9.1 多实例部署

你可以在 Zeabur 上部署多个实例，用于不同的功能：

1. 一个实例用于 API 服務（`python main.py --serve-only`）
2. 一个实例用于定时工作（`python main.py --schedule`）
3. 一个实例用于机器人（`python main.py --discord-bot`）

確保它们共享同一个 `/app/data` 存储卷，以共享資料庫。

### 9.2 自定义域名

在 Zeabur 控制台的「訪問」標籤页，你可以：

1. 使用自动生成的域名
2. 綁定自定义域名
3. 配置 HTTPS

## 10. 更新部署

### 10.1 自动更新

当你向倉庫推送新代碼时：

1. GitHub Actions 会自动构建新镜像
2. Zeabur 会检测到新镜像
3. 你可以选择「自动部署」或手动触发部署

### 10.2 手动更新

1. 在 Zeabur 控制台，进入服務页面
2. 点击「部署历史」
3. 选择「重新部署」
4. 或点击「更新镜像」

## 11. 監控和日誌

### 11.1 查看日誌

在 Zeabur 控制台，进入服務页面，点击「日誌」標籤页，可以查看实时日誌和历史日誌。

### 11.2 監控指標

Zeabur 提供了基礎的監控指標：

- CPU 使用率
- 記憶體使用率
- 網路流量
- 磁盘使用率

在「監控」標籤页查看詳細指標。

## 12. 故障排查

### 12.1 查看詳細日誌

```bash
# 进入容器
zeabur exec <服務名> bash

# 查看日誌文件
cat /app/logs/stock_analysis_20260125.log
```

### 12.2 檢查配置

```bash
# 进入容器
zeabur exec <服務名> bash

# 檢查環境變數
printenv | grep -i discord
printenv | grep -i webui
```

### 12.3 測試連線

```bash
# 測試網路連線
zeabur exec <服務名> curl -I https://api.discord.com

# 測試 API 連線
zeabur exec <服務名> python -c "import requests; print(requests.get('https://api.discord.com').status_code)"
```

## 13. 最佳實踐

1. **使用持久化存储**：始终挂载 `/app/data` 目錄，以保存資料庫
2. **配置合理的健康檢查**：根据實際情况調整健康檢查參數
3. **使用環境變數管理敏感資訊**：不要将 API 密钥硬編碼到代碼中
4. **定期備份數據**：定期下載 `/app/data` 目錄的内容進行備份
5. **使用合适的啟動模式**：根据需求选择合适的啟動命令
6. **監控服務狀態**：定期檢查服務狀態和日誌

## 14. 联系方式

如有議題，欢迎联系项目维护者或在 GitHub Issues 中提问。
