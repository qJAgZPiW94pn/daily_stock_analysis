# 🚀 部署指南

本文档介绍如何将 A股自选股智能分析系統部署到服務器。

## 📋 部署方案对比

| 方案 | 优点 | 缺点 | 推荐场景 |
|------|------|------|----------|
| **Docker Compose** ⭐ | 一键部署、环境隔离、易迁移、易升級 | 需要安裝 Docker | **推荐**：大多数场景 |
| **直接部署** | 简单直接、无额外依賴 | 环境依賴、迁移麻烦 | 临时測試 |
| **Systemd 服務** | 系統级管理、开机自启 | 配置繁琐 | 长期稳定執行 |
| **Supervisor** | 程式管理、自动重啟 | 需要额外安裝 | 多程式管理 |

**结论：推荐使用 Docker Compose，迁移最快最方便！**

---

## 🐳 方案一：Docker Compose 部署（推荐）

### 1. 安裝 Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# CentOS
sudo yum install -y docker docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

### 2. 准备配置文件

```bash
# 克隆代碼（或上傳代碼到服務器）
git clone <your-repo-url> /opt/stock-analyzer
cd /opt/stock-analyzer

# 复制并编辑配置文件
cp .env.example .env
vim .env  # 填入真实的 API Key 等配置
```

### 3. 一键啟動

```bash
# 构建并啟動（同时包含定时分析和 Web 界面服務）
docker-compose -f ./docker/docker-compose.yml up -d

# 查看日誌
docker-compose -f ./docker/docker-compose.yml logs -f

# 查看執行狀態
docker-compose -f ./docker/docker-compose.yml ps
```

啟動成功后，在浏览器输入 `http://服務器公网IP:8000` 即可打开 Web 管理界面。如果打不开，记得先在云服務器控制台的「安全组」里放行 8000 端口。

> 不知道怎么访问？→ [云服務器 Web 界面访问指南](deploy-webui-cloud.md)

### 4. 常用管理命令

```bash
# 停止服務
docker-compose -f ./docker/docker-compose.yml down

# 重啟服務
docker-compose -f ./docker/docker-compose.yml restart

# 更新代碼后重新部署
git pull
docker-compose -f ./docker/docker-compose.yml build --no-cache
docker-compose -f ./docker/docker-compose.yml up -d

# 进入容器调试
docker-compose -f ./docker/docker-compose.yml exec -u dsa stock-analyzer bash

# 手动执行一次分析
docker-compose -f ./docker/docker-compose.yml exec -u dsa stock-analyzer python main.py --no-notify
```

### 5. 數據持久化

數據自动保存在宿主机目錄：
- `./data/` - 資料庫文件
- `./logs/` - 日誌文件
- `./reports/` - 分析报告

### 6. 權限说明

Docker 镜像啟動入口会自动建立并修复 `./data`、`./logs`、`./reports` 对应挂载目錄的權限，然后降权为非 root 使用者 (`dsa`, UID 1000) 執行应用。普通部署不需要手动 `chown` / `chmod`。

如果你显式指定了 `--user` / Compose `user:`，或使用只读挂载、rootless Docker、NFS 等不允许容器修复属主的环境，请确保实际執行使用者对这些目錄具备写入權限。

---

## 🖥️ 方案二：直接部署

### 1. 安裝 Python 环境

```bash
# 安裝 Python 3.10+
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3-pip

# 建立虚拟环境
python3.10 -m venv /opt/stock-analyzer/venv
source /opt/stock-analyzer/venv/bin/activate
```

### 2. 安裝依賴

```bash
cd /opt/stock-analyzer
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 配置环境變數

```bash
cp .env.example .env
vim .env  # 填入配置
```

### 4. 執行

```bash
# 单次執行
python main.py

# 定时工作模式（前台執行）
python main.py --schedule

# 后台執行（使用 nohup）
nohup python main.py --schedule > /dev/null 2>&1 &

# 啟動 Web 管理界面（云服務器需先在 .env 中设置 WEBUI_HOST=0.0.0.0）
python main.py --webui-only

# 啟動 Web 界面（啟動时执行一次分析；需每日定时请加 --schedule 或设 SCHEDULE_ENABLED=true）
python main.py --webui
```

> 不知道怎么访问？→ [云服務器 Web 界面访问指南](deploy-webui-cloud.md)

---

## 🔧 方案三：Systemd 服務

建立 systemd 服務文件实现开机自启和自动重啟：

### 1. 建立服務文件

```bash
sudo vim /etc/systemd/system/stock-analyzer.service
```

内容：
```ini
[Unit]
Description=A股自选股智能分析系統
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/stock-analyzer
Environment="PATH=/opt/stock-analyzer/venv/bin"
ExecStart=/opt/stock-analyzer/venv/bin/python main.py --schedule
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

### 2. 啟動服務

```bash
# 重载配置
sudo systemctl daemon-reload

# 啟動服務
sudo systemctl start stock-analyzer

# 开机自启
sudo systemctl enable stock-analyzer

# 查看狀態
sudo systemctl status stock-analyzer

# 查看日誌
journalctl -u stock-analyzer -f
```

---

## ⚙️ 配置说明

### 必须配置项

| 配置项 | 说明 | 获取方式 |
|--------|------|----------|
| `ANSPIRE_API_KEYS` / `AIHUBMIX_KEY` / `GEMINI_API_KEY` / `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` | AI 模型至少配置一个；推荐优先 Anspire 或 AIHubMix | 对应服務商控制台 |
| `STOCK_LIST` | 自选股列表 | 逗号分隔的股票代碼 |
| 通知渠道 | 至少配置一个，如企业微信、飞书、Telegram 或電郵 | 对应通知平台 |

### 可選配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `SCHEDULE_ENABLED` | `false` | 是否启用定时工作 |
| `SCHEDULE_TIME` | `18:00` | 每日执行时间 |
| `MARKET_REVIEW_ENABLED` | `true` | 是否启用大盤复盘 |
| `ANSPIRE_API_KEYS` | - | Anspire 大模型与新闻搜索（推荐） |
| `AIHUBMIX_KEY` | - | AIHubMix 一 Key 多模型（推荐） |
| `SERPAPI_API_KEYS` | - | SerpAPI 实时金融新闻搜索（推荐） |
| `TAVILY_API_KEYS` | - | Tavily 新闻搜索（可選） |
| `MINIMAX_API_KEYS` | - | MiniMax 搜索（可選） |

---

## 🌐 代理配置

如果服務器在国内，访问 Gemini API 需要代理：

### Docker 方式

编辑 `docker-compose.yml`：
```yaml
environment:
  - http_proxy=http://your-proxy:port
  - https_proxy=http://your-proxy:port
```

### 直接部署方式

编辑 `main.py` 顶部：
```python
os.environ["http_proxy"] = "http://your-proxy:port"
os.environ["https_proxy"] = "http://your-proxy:port"
```

---

## 📊 監控与维护

### 日誌查看

```bash
# Docker 方式
docker-compose -f ./docker/docker-compose.yml logs -f --tail=100

# 直接部署
tail -f /opt/stock-analyzer/logs/stock_analysis_*.log
```

### 健康检查

```bash
# 检查程式
ps aux | grep main.py

# 检查最近的报告
ls -la /opt/stock-analyzer/reports/
```

### 定期维护

```bash
# 清理旧日誌（保留7天）
find /opt/stock-analyzer/logs -mtime +7 -delete

# 清理旧报告（保留30天）
find /opt/stock-analyzer/reports -mtime +30 -delete
```

---

## ❓ 常见議題

### 1. Docker 构建失败

```bash
# 清理快取重新构建
docker-compose -f ./docker/docker-compose.yml build --no-cache
```

### 2. API 访问逾時

检查代理配置，确保服務器能访问 Gemini API。

### 3. 資料庫锁定

```bash
# 停止服務后刪除 lock 文件
rm /opt/stock-analyzer/data/*.lock
```

### 4. 記憶體不足

调整 `docker-compose.yml` 中的記憶體限制：
```yaml
deploy:
  resources:
    limits:
      memory: 1G
```

### 5. WebUI 打开后 UI 元素异常变大 / 布局错乱

**症状**：能访问 8000 端口，但页面上的文字、按钮、卡片异常放大，没有正常布局。

**根因**：`static/index.html` 存在，但 CSS/JS 资源文件缺失（`static/assets/` 为空或不存在），浏览器无法加载样式与脚本，导致裸 HTML 渲染。

**解决方法**：

- **Docker 部署**：执行以下命令重新构建镜像（确保前端已正确打包进镜像）：
  ```bash
  docker-compose -f ./docker/docker-compose.yml down
  docker-compose -f ./docker/docker-compose.yml build --no-cache
  docker-compose -f ./docker/docker-compose.yml up -d
  ```
  构建完成后刷新浏览器快取（`Ctrl+Shift+R`）再访问。

- **直接部署（pip + python）**：先构建前端，再啟動服務：
  ```bash
  # 安裝 Node.js 18+（推荐 20+，如尚未安裝）
  # 构建前端
  cd apps/dsa-web
  npm ci
  npm run build
  cd ../..
  # 啟動服務
  python main.py --webui-only
  ```

**验证**：用浏览器开发者工具（F12 → Network）检查是否有 `/assets/index-*.js` 和 `/assets/index-*.css` 的 404 錯誤；如有，说明资源缺失，按上述步骤重新构建即可。

---

## 🔄 快速迁移

从一台服務器迁移到另一台：

```bash
# 源服務器：打包
cd /opt/stock-analyzer
tar -czvf stock-analyzer-backup.tar.gz .env data/ logs/ reports/

# 目标服務器：部署
mkdir -p /opt/stock-analyzer
cd /opt/stock-analyzer
git clone <your-repo-url> .
tar -xzvf stock-analyzer-backup.tar.gz
docker-compose -f ./docker/docker-compose.yml up -d
```

---

## ☁️ 方案四：GitHub Actions 部署（免服務器）

**最简单的方案！** 無需服務器，利用 GitHub 免费计算资源。

### 优势
- ✅ **完全免费**（每月 2000 分钟）
- ✅ **無需服務器**
- ✅ **自动定时执行**
- ✅ **零维护成本**

### 限制
- ⚠️ 无狀態（每次執行是新环境）
- ⚠️ 定时可能有几分钟延遲
- ⚠️ 无法提供 HTTP API

### 部署步骤

#### 1. 建立 GitHub 倉庫

```bash
# 初始化 git（如果还没有）
cd /path/to/daily_stock_analysis
git init
git add .
git commit -m "Initial commit"

# 建立 GitHub 倉庫并推送
# 在 GitHub 网页上建立新倉庫后：
git remote add origin https://github.com/你的使用者名/daily_stock_analysis.git
git branch -M main
git push -u origin main
```

#### 2. 配置 Secrets（重要！）

打开倉庫页面 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

添加以下 Secrets：

| Secret 名称 | 说明 | 必填 |
|------------|------|------|
| `ANSPIRE_API_KEYS` | Anspire Open API Key（一 Key 启用大模型与搜索） | 推荐 |
| `AIHUBMIX_KEY` | AIHubMix API Key（一 Key 多模型） | 推荐 |
| `ANTHROPIC_API_KEY` | Anthropic API Key | 可選 |
| `GEMINI_API_KEY` | Gemini AI API Key | 可選 |
| `OPENAI_API_KEY` | OpenAI 兼容 API Key | 可選 |
| `WECHAT_WEBHOOK_URL` | 企业微信机器人 Webhook | 可選* |
| `FEISHU_WEBHOOK_URL` | 飞书机器人 Webhook | 可選* |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | 可選* |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | 可選* |
| `TELEGRAM_MESSAGE_THREAD_ID` | Telegram Topic ID | 可選* |
| `EMAIL_SENDER` | 发件人邮箱 | 可選* |
| `EMAIL_PASSWORD` | 邮箱授權码 | 可選* |
| `SERVERCHAN3_SENDKEY` | Server酱³ Sendkey | 可選* |
| `CUSTOM_WEBHOOK_URLS` | 自定义 Webhook（多个逗号分隔） | 可選* |
| `STOCK_LIST` | 自选股列表，如 `600519,300750` | ✅ |
| `SERPAPI_API_KEYS` | SerpAPI Key | 推荐 |
| `TAVILY_API_KEYS` | Tavily 搜索 API Key | 可選 |
| `BOCHA_API_KEYS` | 博查搜索 API Key | 可選 |
| `BRAVE_API_KEYS` | Brave Search API Key | 可選 |
| `MINIMAX_API_KEYS` | MiniMax Coding Plan Web Search | 可選 |
| `SEARXNG_BASE_URLS` | SearXNG 自建实例（无配额兜底，需在 settings.yml 启用 format: json）；留空时默认自动发现公共实例 | 可選 |
| `SEARXNG_PUBLIC_INSTANCES_ENABLED` | 是否在 `SEARXNG_BASE_URLS` 为空时自动从 `searx.space` 获取公共实例（默认 `true`） | 可選 |
| `TUSHARE_TOKEN` | Tushare Token | 可選 |
| `GEMINI_MODEL` | 模型名称（默认 gemini-2.0-flash） | 可選 |

> *注：通知渠道至少配置一个，支援多渠道同时推送

#### 3. 验证 Workflow 文件

确保 `.github/workflows/daily_analysis.yml` 文件存在且已提交：

```bash
git add .github/workflows/daily_analysis.yml
git commit -m "Add GitHub Actions workflow"
git push
```

#### 4. 手动測試執行

1. 打开倉庫页面 → **Actions** 標籤
2. 选择 **"每日股票分析"** workflow
3. 点击 **"Run workflow"** 按钮
4. 选择執行模式：
   - `full` - 完整分析（股票+大盤）
   - `market-only` - 仅大盤复盘
   - `stocks-only` - 仅股票分析
5. 点击绿色 **"Run workflow"** 按钮

#### 5. 查看执行日誌

- Actions 页面可以看到執行历史
- 点击具体的執行记录查看详细日誌
- 分析报告会作为 Artifact 保存 30 天

### 定时说明

默认配置：**週一到週五，北京时间 18:00** 自动执行

修改时间：编辑 `.github/workflows/daily_analysis.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 10 * * 1-5'  # UTC 时间，+8 = 北京时间
```

常用 cron 示例：
| 表达式 | 说明 |
|--------|------|
| `'0 10 * * 1-5'` | 週一到週五 18:00（北京时间） |
| `'30 7 * * 1-5'` | 週一到週五 15:30（北京时间） |
| `'0 10 * * *'` | 每天 18:00（北京时间） |
| `'0 2 * * 1-5'` | 週一到週五 10:00（北京时间） |

### 修改自选股

方法一：修改倉庫 Secret `STOCK_LIST`

方法二：直接修改代碼后推送：
```bash
# 修改 .env.example 或在代碼中设置默认值
git commit -am "Update stock list"
git push
```

### 常见議題

**Q: 为什么定时工作没有执行？**
A: GitHub Actions 定时工作可能有 5-15 分钟延遲，且仅在倉庫有活动时才触发。长时间无 commit 可能导致 workflow 被禁用。

**Q: 如何查看历史报告？**
A: Actions → 选择執行记录 → Artifacts → 下載 `analysis-reports-xxx`

**Q: 免费额度够用吗？**
A: 每次執行约 2-5 分钟，一个月 22 个工作日 = 44-110 分钟，远低于 2000 分钟限制。

---

## 🌐 云服務器上部署了，但不知道怎么用浏览器访问？

详见 → [云服務器 Web 界面访问指南](deploy-webui-cloud.md)

涵盖：直接部署和 Docker 两种方式的啟動与访问、安全组/防火墙配置、常见議題排查、Nginx 反向代理（可選）。

---

**祝部署顺利！🎉**
