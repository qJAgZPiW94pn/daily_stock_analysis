# 云服務器 Web 界面訪問指南

如果你已經把项目部署到云服務器，但不知道在浏览器里輸入什么地址才能打开 Web 管理界面，这篇教程就是为你准备的。

> 其实就两步：让服務监听外网，再在浏览器里輸入地址。

---

## 目錄

- [方式一：直接部署（pip + python）](#方式一直接部署pip--python)
- [方式二：Docker Compose](#方式二docker-compose)
- [如何在浏览器里打开界面](#如何在浏览器里打开界面)
- [如何确认 Docker 重建已生效](#如何确认-docker-重建已生效)
- [訪問不了？先檢查这几项](#訪問不了先檢查这几项)
- [可選：Nginx 反向代理（綁定域名 / 80 端口）](#可選nginx-反向代理綁定域名--80-端口)
- [安全建议](#安全建议)

---

## 方式一：直接部署（pip + python）

### 第一步：修改 .env 中的监听地址

用编辑器打开 `.env`（在项目根目錄，即包含 `main.py` 的目錄），找到这一行：

```env
WEBUI_HOST=127.0.0.1
```

把 `127.0.0.1` 改成 `0.0.0.0`：

```env
WEBUI_HOST=0.0.0.0
```

> `127.0.0.1` 表示只有本机能訪問，`0.0.0.0` 表示允許任何来源訪問。云服務器必须改成 `0.0.0.0` 才能从外网打开界面。

> **注意**：当前 `python main.py` 啟動邏輯会在 host 为預設 `0.0.0.0` 时讀取 `.env` 里的 `WEBUI_HOST`；即使显式传入 `--host 0.0.0.0`，如果 `.env` 里仍是 `WEBUI_HOST=127.0.0.1`，最終也可能只监听本机。云服務器请务必先把 `.env` 改成 `WEBUI_HOST=0.0.0.0`。

### 第二步：啟動服務

在项目根目錄執行：

```bash
# 只啟動 Web 界面（不自动執行分析）
python main.py --webui-only

# 或者：啟動 Web 界面（啟動时執行一次分析；需每日定时分析请加 --schedule 或设 SCHEDULE_ENABLED=true）
python main.py --webui
```

啟動成功后，终端会輸出类似：

```
FastAPI 服務已啟動: http://0.0.0.0:8000
```

如果你想让服務在退出终端后繼續執行，可以用 `nohup`：

```bash
nohup python main.py --webui-only > /dev/null 2>&1 &
```

> 日誌文件会由程式自动写入 `logs/` 目錄，用 `tail -f logs/stock_analysis_*.log` 查看。

### 修改端口（可選）

預設端口是 8000。如果想改用其他端口，在 `.env` 里设置：

```env
WEBUI_PORT=8888
```

然后重啟服務。

---

## 方式二：Docker Compose

### 第一步：确认已有 .env 配置

项目的 `docker/docker-compose.yml` 在容器内部已經自动设置了 `WEBUI_HOST=0.0.0.0`，你不需要在 `.env` 里再改监听地址，Docker 会自动處理。

### 第二步：啟動服務

在项目根目錄執行：

```bash
# 同时啟動定时分析 + Web 界面（推荐）
docker-compose -f ./docker/docker-compose.yml up -d

# 或者只啟動 Web 界面服務
docker-compose -f ./docker/docker-compose.yml up -d server
```

啟動后查看狀態：

```bash
docker-compose -f ./docker/docker-compose.yml ps
```

看到 `server` 服務狀態为 `running` 就说明 Web 界面已經在執行了。

### 修改端口（可選）

預設端口是 8000。如果想改用其他端口，在 `.env` 里设置：

```env
API_PORT=8888
```

然后重新啟動容器：

```bash
docker-compose -f ./docker/docker-compose.yml down
docker-compose -f ./docker/docker-compose.yml up -d
```

---

## 如何在浏览器里打开界面

服務啟動后，在浏览器地址栏輸入：

```
http://你的服務器公网IP:8000
```

例如，如果你的服務器 IP 是 `1.2.3.4`，就輸入：

```
http://1.2.3.4:8000
```

如果你的域名已經解析到这台服務器，也可以直接用域名訪問：

```
http://your-domain.com:8000
```

> **在哪里查公网 IP？** 登录你的云服務器控制台（阿里云/腾讯云/AWS 等），在实例列表里可以看到「公网 IP」或「弹性 IP」。

---

## 如何确认 Docker 重建已生效

先区分两件事：

1. **Docker 镜像發佈版本**：看你部署时使用的镜像 tag，例如 `ghcr.io/zhulinsen/daily_stock_analysis:v3.12.0`。倉庫的 Docker 發佈由 `.github/workflows/docker-publish.yml` 按 `v*.*.*` Git tag 触发，所以 Docker 版本应以镜像 tag / GitHub Releases 为准。
2. **当前页面加载的前端构建**：看 WebUI “系統设置”页里的版本資訊卡片，用来确认浏览器拿到的静态资源是否已經更新。

也就是说，**“系統设置”里的版本資訊更适合判斷前端是否重建成功，不等同于 Docker 镜像發佈版本**。

WebUI 现在会在“系統设置”页展示只读的“版本資訊”卡片，包含：

- `WebUI 版本`
- `构建标识`
- `构建时间`

如果 `apps/dsa-web/package.json` 里的版本号仍是占位值 `0.0.0`，页面会自动回退展示本次前端构建生成的 `构建标识`，避免你误把占位版本当成真实發佈版本。

当你重新執行 `docker-compose -f ./docker/docker-compose.yml up -d --build`，或者单独重新執行前端 `npm run build` 后，可以刷新浏览器并进入“系統设置”，優先确认“构建时间”是否已經变化；若变化，通常就说明当前加载的静态资源已經切換到最新构建。

如果你想确认“我现在到底部署的是哪个正式版本”，優先用下面这些方式：

```yaml
# 方式 1：看 docker-compose / 部署脚本里的 image tag
image: ghcr.io/zhulinsen/daily_stock_analysis:v3.12.0
```

```bash
# 方式 2：回看你的拉取命令
docker pull ghcr.io/zhulinsen/daily_stock_analysis:v3.12.0
```

如果你一直使用 `latest`，建议改成显式版本 tag；否则很难仅凭容器内页面資訊判斷自己是否已經重复更新到同一版本。

在确认本機前端打包鏈路时，建议執行以下命令作为最小驗證闭环：

```bash
cd apps/dsa-web
npm ci
npm run lint
npm run build
```

其中 `build` 成功后，`static` 下生成的 `index.html`/JS/CSS 资源会包含本次构建时间与构建版本資訊；刷新后在“版本資訊”卡片中应能见到变化。

---

## 訪問不了？先檢查这几项

### 1. 安全组 / 防火墙没有放行端口

这是最常见的原因。云服務器預設只开放 22（SSH）端口，需要手动放行 8000（或你改的端口）。

**操作方法**（以阿里云为例）：
1. 登录阿里云控制台 → 云服務器 ECS → 找到你的实例
2. 点击「安全组」→「配置規則」→「添加安全组規則」
3. 方向选「入方向」，端口範圍填 `8000/8000`，授權对象填 `0.0.0.0/0`，点击「確定」

腾讯云、AWS 等云厂商操作类似，找到「安全组」或「防火墙規則」，新增一条允許 TCP 8000 端口的入站規則即可。

### 2. 服務器系統防火墙拦截了

如果你的系統开启了 `ufw` 或 `firewalld`，也需要放行端口：

```bash
# Ubuntu / Debian（ufw）
sudo ufw allow 8000

# CentOS / RHEL（firewalld）
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### 3. 直接部署时 .env 里的 WEBUI_HOST 没改

这是第二常见原因。`.env` 里預設是 `WEBUI_HOST=127.0.0.1`，这样服務只监听本机，外网根本连不上。

改法：打开 `.env`，把 `WEBUI_HOST=127.0.0.1` 改成 `WEBUI_HOST=0.0.0.0`，然后重啟服務。

> Docker 方式不需要改这个，可以略過。

### 4. 端口号对不上

檢查訪問地址里的端口是否和 `.env` / 啟動命令里设置的端口一致。

- 直接部署：預設 8000，可通过 `WEBUI_PORT=xxxx` 修改
- Docker：預設 8000，可通过 `API_PORT=xxxx` 修改

### 5. 页面能打开，但 UI 元素例外变大 / 布局错乱

**症状**：浏览器能訪問到 8000 端口，页面有内容，但文字、按钮、卡片尺寸例外大，没有正常布局与配色。

**根因**：`static/index.html` 存在但 CSS/JS 资源缺失（`static/assets/` 为空或不存在），浏览器加载了 HTML 框架但無法拿到样式与脚本，退化为裸 HTML 渲染。

可先用浏览器开发者工具（F12 → Network 標籤页）檢查是否有 `/assets/index-*.js`、`/assets/index-*.css` 的 **404** 錯誤。若有，按以下方式修复：

**Docker 使用者**：

```bash
docker-compose -f ./docker/docker-compose.yml down
docker-compose -f ./docker/docker-compose.yml build --no-cache
docker-compose -f ./docker/docker-compose.yml up -d
```

重建完成后，用 `Ctrl+Shift+R` 強制刷新浏览器快取，再訪問页面。

**直接部署使用者**：先確保已安裝 Node.js 18+（推荐 20+），然后手动构建前端：

```bash
cd apps/dsa-web
npm ci
npm run build
cd ../..
python main.py --webui-only
```

---

## 可選：Nginx 反向代理（綁定域名 / 80 端口）

如果你有域名，或者不想在地址里带 `:8000`，可以用 Nginx 做反向代理，把 80/443 端口流量轉發给后端服務。

### 安裝 Nginx

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y nginx

# CentOS
sudo yum install -y nginx
```

### 配置文件示例

新建文件 `/etc/nginx/conf.d/stock-analyzer.conf`，内容如下（把 `your-domain.com` 改成你的域名或 IP）：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 支援 WebSocket（Agent 对话页面需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 启用配置并重啟 Nginx

```bash
sudo nginx -t            # 檢查配置有没有语法錯誤
sudo systemctl reload nginx
```

配置成功后，直接用 `http://your-domain.com` 訪問即可，不需要带端口号。

> **使用 Nginx 后的注意事项**：
> - 如果你开启了 Web 登录認證（`ADMIN_AUTH_ENABLED=true`），建议在 `.env` 中把 `TRUST_X_FORWARDED_FOR=true` 一并打开，否则系統可能無法正确识别真实 IP。该选项适用于**单层可信反向代理**（Nginx → App）部署；如果使用多级代理或 CDN（CDN → Nginx → App），登录限流的 key 可能退化为边缘代理 IP 而非真实客户端 IP，需根据實際拓撲評估。
> - 如需 HTTPS，可以用 [Certbot](https://certbot.eff.org/) 自动申请免费的 Let's Encrypt 证书。

---

## 安全建议

把 Web 界面暴露到公网之前，强烈建议开启登录密碼保护：

在 `.env` 中设置：

```env
ADMIN_AUTH_ENABLED=true
```

重啟服務后，第一次訪問网页时会要求设置初始密碼。设置完成后，每次打开设置页面都需要輸入密碼，可以防止 API Key 等敏感配置被他人看到。

> 如果忘了密碼，可以在服務器上執行：`python -m src.auth reset_password`

---

遇到其他議題？欢迎 [提交 Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues)。
