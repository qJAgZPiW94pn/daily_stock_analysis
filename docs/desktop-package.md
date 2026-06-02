# 桌面端打包说明 (Electron + React UI)

本项目可打包为桌面应用，使用 Electron 作为桌面壳，`apps/dsa-web` 的 React UI 作为界面。

## 架构说明

- React UI（Vite 构建）由本機 FastAPI 服務托管
- Electron 啟動时自动拉起后端服務，等待 `/api/health` 就绪后加载 UI
- 使用者配置文件 `.env` 和資料庫放在 exe 同级目錄（便携模式）

## 本機开发

一键啟動（开发模式）：

```bash
powershell -ExecutionPolicy Bypass -File scripts\run-desktop.ps1
```

或手动执行：

1) 构建 React UI（输出到 `static/`）

```bash
cd apps/dsa-web
npm install
npm run build
```

2) 啟動 Electron 应用（自动拉起后端）

```bash
cd apps/dsa-desktop
npm install
npm run dev
```

首次執行时会自动从 `.env.example` 复制生成 `.env`。

## 打包 (Windows)

### 前置条件

- Node.js 18+
- Python 3.10+
- 开启 Windows 开发者模式（electron-builder 需要建立符号链接）
  - 设置 -> 隐私和安全性 -> 开发者选项 -> 开发者模式

### 一键打包

```bash
powershell -ExecutionPolicy Bypass -File scripts\build-all.ps1
```

该脚本会依次执行：
1. 构建 React UI
2. 安裝 Python 依賴
3. PyInstaller 打包后端
4. electron-builder 打包桌面应用

当前 Windows 安裝包使用 NSIS 向导式安裝流程，仅支援当前使用者安裝且已禁用管理员提权，安裝时可手动选择目标目錄（例如非 C 盘）。安裝器通过 NSIS `.onVerifyInstDir` 回调在安裝器层面阻止选择 `Program Files`、`Windows` 等系統保护目錄——选择这些路徑时"下一步"按钮会被自动禁用。安裝完成后，桌面端仍会按现有逻辑在安裝目錄旁生成/读取 `.env`、`data/stock_analysis.db`（含 `data/stock_analysis.db-wal` / `data/stock_analysis.db-shm`）和 `logs/desktop.log`。推荐使用默认的 per-user 安裝目錄。如果不想安裝，仍可繼續分发 `win-unpacked` 免安裝包。

## GitHub CI 自动打包並行布 Release

倉庫已支援通过 GitHub Actions 自动构建桌面端并上傳到 GitHub Releases：

- 工作流：`.github/workflows/desktop-release.yml`
- 触发方式：
  - 推送语义化 tag（如 `v3.2.12`）后自动触发
  - 在 Actions 页面手动触发并指定 `release_tag`
- 产物：
  - Windows 安裝包：Release 附件和本機 `apps/dsa-desktop/dist/` 中统一为 `daily-stock-analysis-windows-installer-<tag>.exe`
  - Windows 自动更新元數據：Release 附件会额外保留 `latest.yml` 和 `*.blockmap`，供安裝版桌面端后台下載与校验更新；普通使用者無需手动下載这些元數據
  - Windows 免安裝包：`daily-stock-analysis-windows-noinstall-<tag>.zip`
  - macOS Intel：`daily-stock-analysis-macos-x64-<tag>.dmg`
  - macOS Apple Silicon：`daily-stock-analysis-macos-arm64-<tag>.dmg`

建议發佈流程：

1. 合併代碼到 `main`
2. 由自动打 tag 工作流生成版本（或手动建立 tag）
3. `desktop-release` 工作流自动构建并把两个平台安裝包附加到对应 GitHub Release

## 发版前可复现验证（桌面更新链路）

桌面端自动更新链路依賴 Windows NSIS 安裝产物、`latest.yml` 与 `*.blockmap` 元數據。当前桌面 CI 不覆盖 `desktop-release` 打包产物可發佈链路，提交前建议补充如下本機验证：

说明：该清单专注于 Windows NSIS 安裝版与 `electron-updater` 發佈元數據。当前 Linux 环境无法直接产出 Windows 安裝包和 updater 元數據（`latest.yml` / `*.blockmap`），此类链路需在 Windows 發佈执行器或 Windows 本机环境复核。

若在非 Windows 环境无法完成上述验证，请在 PR 验收说明中明确补齐 Windows 發佈链路复核人、复核时间窗及 `desktop-release` 产物检查结果（release/tag 与 `daily-stock-analysis-windows-installer-<tag>.exe`、`latest.yml`、`*.blockmap` 版本一致性与可下載性）。

1. 先构建 Web 静态产物（桌面端主窗口与设置页入口依賴）

```bash
cd apps/dsa-web
npm ci
npm run lint
npm run build
```

2. 回到桌面端，补齐依賴、執行 preload 单测、再执行 Electron 打包

```bash
cd ../dsa-desktop
npm ci
npm test
npm run build
```

在 Windows 發佈复核环境，还可额外执行：

```powershell
./scripts/verify-desktop-updater-artifacts.ps1 -ReleaseTag v$(node -p "require('./apps/dsa-desktop/package.json').version")
```

> 预期当前执行环境不支援生成 Windows NSIS 安裝器时，请在交付说明中明确注明平台限制，并要求指定的 Windows 發佈链路复核人补齐该项验证。

3. 检查更新元數據是否产出

```bash
ls -1 dist | sort
ls -1 dist/*.yml dist/*.blockmap 2>/dev/null || true
```

4. 强制对齐版本与發佈附件（可在 Windows 环境或能产出 NSIS 产物的执行器上复核）

```bash
RELEASE_TAG="v$(node -p \"require('./package.json').version\")"
REPO="ZhuLinsen/daily_stock_analysis"

for f in dist/*latest.yml dist/*.blockmap dist/daily-stock-analysis-windows-installer-*.exe; do
  [ -f \"$f\" ] && echo \"[FOUND] $f\"
done

if [ -f dist/latest.yml ]; then
  echo \"---- latest.yml 版本片段 ----\"
  grep -E \"^version:|^files:|^sha512:\" dist/latest.yml
fi

echo \"---- Release 清单（人工核对）----\"
echo \"Release Tag: $RELEASE_TAG\"
echo \"Release 地址: https://github.com/$REPO/releases/tag/$RELEASE_TAG\"
echo \"应核对附件是否包含:\"
echo \"- daily-stock-analysis-windows-installer-*.exe\"
echo \"- latest.yml\"
echo \"- *.blockmap\"
echo \"并确保 latest.yml 中 version 与 tag 的语义化版本一致，path/url 与安裝包附件名一致\"
```

5a. 建议在 PR 描述里记录的“可复核输出”（Windows）：

```bash
echo "release-tag=${RELEASE_TAG}"
echo "latest.yml version:"
grep -E "^version:" dist/latest.yml
echo "latest.yml files:"
sed -n '1,80p' dist/latest.yml
echo "packaging artifacts:"
ls -1 dist/*.yml dist/*.blockmap dist/*installer*.exe 2>/dev/null | sort
```

Windows 發佈链路复核清单（在 PR 后由發佈团队/维护者执行）：

- release/tag 与 `daily-stock-analysis-windows-installer-<tag>.exe` 的版本号一致；
- `latest.yml`、`daily-stock-analysis-windows-installer-<tag>.exe`、`*.blockmap` 同 tag 同步出现且可下載；
- `latest.yml` 中 `version` 与 Release tag 语义一致（去掉 `v` 前缀后比对），且 `path` / `files.url` 与安裝包附件名一致；
- 如缺少上述文件或 `release-tag` 不匹配，需标注阻断并补齐 `desktop-release` 打包流程。

5. Windows/NSIS 产物与發佈附件一致性请在 Windows 环境手动验证（可人工触发發佈流程），并在升級后核对執行时文件留存：

   1. 安裝前后分别记录安裝目錄中的 `.env`、`data/stock_analysis.db`、`data/stock_analysis.db-wal`、`data/stock_analysis.db-shm`、`logs/desktop.log` 的 SHA256；
   2. 确认桌面端下一次啟動后，上述文件仍存在且与安裝前记录一致；
   3. 如不一致，可在应用退出后检查使用者數據目錄中的 `.dsa-desktop-update-backup` 是否清理完整，并结合最新日誌串联排查。

Windows 平台建议使用 PowerShell 执行：

```bash
Get-FileHash .env,data\\stock_analysis.db,data\\stock_analysis.db-wal,data\\stock_analysis.db-shm,logs\\desktop.log -Algorithm SHA256
```

说明：应用已在 Windows NSIS 安裝版的“重啟安裝”前備份安裝目錄旁上述執行时文件并尝试恢復，目的是降低更新过程中文件丢失風險；若恢復失败，桌面端会显示更新安裝錯誤并保留手动下載路徑供回退處理。

### 分步打包

1) 构建 React UI

```bash
cd apps/dsa-web
npm install
npm run build
```

2) 打包 Python 后端

```bash
pip install pyinstaller
pip install -r requirements.txt
python -m PyInstaller --name stock_analysis --onefile --noconsole --add-data "static;static" --hidden-import=multipart --hidden-import=multipart.multipart main.py
```

将生成的 exe 复制到 `dist/backend/`：

```bash
mkdir dist\backend
copy dist\stock_analysis.exe dist\backend\stock_analysis.exe
```

3) 打包 Electron 桌面应用

```bash
cd apps/dsa-desktop
npm install
npm run build
```

打包产物位于 `apps/dsa-desktop/dist/`。Windows 安裝器会生成 `daily-stock-analysis-windows-installer-<tag>.exe`，安裝向导中可選择安裝目錄。

## 目錄结构

Windows 安裝包模式下，安裝器仅支援当前使用者安裝且已禁用管理员提权，使用者可在安裝向导中选择安裝目錄；安裝器会在安裝器层面阻止选择 `Program Files`、`Windows` 等系統保护目錄（选择时"下一步"按钮自动禁用），安裝完成后，应用会在安裝目錄旁生成/读取 `.env`、`data/stock_analysis.db`（含 `data/stock_analysis.db-wal` / `data/stock_analysis.db-shm`）和 `logs/desktop.log`。请保留默认的 per-user 安裝位置或选择其他使用者可写目錄。

`win-unpacked` 免安裝模式下，目錄结构如下：

```
win-unpacked/
  Daily Stock Analysis.exe    <- 双击啟動
  .env                        <- 使用者配置文件（首次啟動自动生成）
  data/
    stock_analysis.db         <- 資料庫主文件
    stock_analysis.db-wal     <- WAL 日誌文件（更新備份/恢復）
    stock_analysis.db-shm     <- WAL 共享元文件（更新備份/恢復）
  logs/
    desktop.log               <- 執行日誌
  resources/
    .env.example              <- 配置模板
    backend/
      stock_analysis.exe      <- 后端服務
```

## 配置文件说明

- `.env` 放在 exe 同目錄下
- 首次啟動时自动从 `.env.example` 复制生成
- macOS 打包态下，`exe` 实际位于 `.app` 包内部，因此 `.env`、`data/`、`logs/` 也会跟着落在应用包内容器里；替换新的 DMG / `.app` 时，旧配置会随旧应用包一起被覆盖
- 使用者需要编辑 `.env` 配置以下内容：
  - `GEMINI_API_KEY` 或 `OPENAI_API_KEY`：AI 分析必需
  - `STOCK_LIST`：自选股列表（逗号分隔）
  - 其他可選配置参考 `.env.example`

### 配置備份 / 恢復 `.env`

- WebUI 与桌面端都可以从 `系統设置 -> 配置備份` 看到 `匯出 .env` 和 `匯入 .env` 按钮
- WebUI 非桌面執行时需要先开启管理员認證并完成登录；未开启認證时按钮会禁用，API 傳回 `403`
- `匯出 .env` 会匯出当前**已保存**的 `.env` 備份文件；页面上尚未点击“保存配置”的本機草稿不会被匯出
- `匯入 .env` 会读取備份文件中的键值并合併到当前配置中，匯入后会立即触发配置重载
- 匯入是“键级覆盖”而不是整文件替换：備份文件中出现的键会覆盖当前值，未出现的键保持不变
- 如果当前页面还有未保存草稿，匯入前会先提示确认，避免把本機草稿和已保存配置混在一起
- Web 端默认 `ADMIN_AUTH_ENABLED=false` 时，设置页会展示按钮为禁用态并提示先启用管理员鉴权；桌面端不受该配置影响，仍可直接使用配置備份/恢復能力。

> 建议：macOS 使用者在升級 DMG 前先执行一次 `匯出 .env`，这样即使旧 `.app` 被整体替换，也能在新版本里直接恢復配置

### 设置页版本資訊

- `系統设置 -> 版本資訊` 中的“桌面端版本”由 Electron 主程式的 `app.getVersion()` 提供，并通过 preload bridge 暴露给前端
- 开发态 `npm run dev` 与打包态 `npm run build` / 安裝包都会复用同一条版本注入链路，不再在 `preload.js` 里维护独立硬编码版本号
- `README.md` 繼續保留安裝和執行入口说明；这类桌面端執行时细节统一落在本专题文档维护，避免入门文档膨胀

### 桌面端更新提醒

- 应用在主界面加载完成后会后台检查 GitHub Releases 的最新正式版，并与当前 `app.getVersion()` 做语义化版本比较
- Windows NSIS 安裝版会通过内置 GitHub 更新源自动下載新版本；下載完成后弹出一次性提醒，使用者确认后重啟并安裝
- `系統设置 -> 版本資訊` 中的“桌面端更新”区域可手动检查更新；若更新已下載，会展示“重啟安裝”操作
- Windows 免安裝包、开发态和 macOS DMG 仍保持“提醒 + 跳转下載页”的兼容路徑，不会因为網路失败而阻断桌面端啟動
- 版本检查失败、GitHub API 逾時、更新元數據缺失或下載安裝异常时，会记录到 `logs/desktop.log`，设置页手动检查时会展示錯誤狀態

## 常见議題

### 啟動后一直显示 "Preparing backend..."

1. 检查 `logs/desktop.log` 查看錯誤資訊
2. 确认 `.env` 文件存在且配置正确
3. 确认端口 8000-8100 未被占用

### 后端啟動报 ModuleNotFoundError

PyInstaller 打包时缺少模块，需要在 `scripts/build-backend.ps1` 中增加 `--hidden-import`。

### UI 加载空白

确认 `static/index.html` 存在，如不存在需重新构建 React UI。

### macOS 升級后配置看起来“被清空”

这是当前桌面端便携模式的已知行为：`.env` 放在打包后的应用目錄旁，而 macOS 中这个目錄通常位于 `.app` 包内部。升級或替换新的 DMG / `.app` 后，旧 `.env` 不会自动迁移，所以看起来像“配置丢了”。

處理方式：

1. 升級前在桌面端设置页执行一次 `匯出 .env`
2. 安裝新版本后，在同一位置点击 `匯入 .env`
3. 匯入完成后等待设置页重新加载即可

## 分发给使用者

Windows 分发现在有两种方式：

1. 安裝包：分发 `apps/dsa-desktop/dist/` 下的 `daily-stock-analysis-windows-installer-<tag>.exe`，使用者安裝时可自行选择目标目錄
2. 免安裝包：将 `apps/dsa-desktop/dist/win-unpacked/` 整个文件夹打包发给使用者

使用 `win-unpacked` 免安裝包时，使用者只需：

1. 解压文件夹
2. 编辑 `.env` 配置 API Key 和股票列表
3. 双击 `Daily Stock Analysis.exe` 啟動
