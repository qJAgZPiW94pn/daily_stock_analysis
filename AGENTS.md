# AGENTS.md

本文件用于約束本倉庫的預設开发流程，目标是减少重复沟通、减少返工，并让改动和当前项目结构保持一致。

如果本文件与倉庫中的脚本、工作流、代碼现状不一致，以實際可執行内容为准，并在相關改动中顺手修正文档，避免規則繼續漂移。

## 1. 硬規則

- 遵循现有目錄邊界：
  - 后端邏輯優先放在 `src/`、`data_provider/`、`api/`、`bot/`
  - Web 前端改动在 `apps/dsa-web/`
  - 桌面端改动在 `apps/dsa-desktop/`
  - 部署与流水线改动在 `scripts/`、`.github/workflows/`、`docker/`
- 未经明確确认，不執行 `git commit`、`git tag`、`git push`。
- commit message 使用英文，不添加 `Co-Authored-By`。
- 不写死密钥、账号、路徑、模型名、端口或環境差异邏輯。
- 優先复用现有模組、配置入口、脚本和測試，不新增平行實現。
- 預設稳定性優先于“顺手最佳化”；非当前工作直接需要的重构、抽象和基礎设施迁移一律克制。
- 新增配置项时，必须同步更新 `.env.example` 和相關文档。
- 涉及使用者可见能力、CLI/API 行为、部署方式、通知方式、报告结构变化时，必须同步更新相關文档与 `docs/CHANGELOG.md`。
- `docs/CHANGELOG.md` 的 `[Unreleased]` 段使用**扁平格式**：每条独立一行，格式为 `- [类型] 描述`，类型取值：`新功能`/`改进`/`修复`/`文档`/`測試`/`chore`；**禁止在 `[Unreleased]` 内新增 `### 类目标题`**，以减少並行 PR 的 merge 冲突。发版时由 maintainer 汇总整理成带标题的正式格式。
- `README.md` 只用于项目定位、核心能力总览、快速开始、主要入口、赞助/合作等首页级資訊；非必要不更新 README，避免持续膨胀。
- 更细的模組行为、页面交互、专题配置、排障说明、欄位契约、實現语义和邊界條件，優先更新对应 `docs/*.md` 或专题文档，不写入 README。
- 变更中英双语文档之一时，需評估另一份是否需要同步；若未同步，交付说明里要写明原因。
- 注释、docstring、日誌文案以清晰准确为准，不強制要求英文，但应与文件语境保持一致。

## 1.1 PR 标题規範（非阻断建议）

- 推荐使用 `<类型>: <修改内容>` 作为 PR 标题，例如 `fix: 修复大盤分析历史记录丢失`，優先类型为 `fix`/`feat`/`refactor`/`docs`/`chore`/`test`/`ci`。
- 标题应描述實際变更内容，建议不添加 `[codex]`、`codex`、`autocode`、`copilot` 或其他工具/agent 来源前綴。
- 该規範仅用于协作可读性与一致性提示，不应单独作为 review process blocker。

## 2. AI 协作资产治理

- `AGENTS.md` 是倉庫内 AI 协作規則的唯一真源。
- `CLAUDE.md` 必须是指向 `AGENTS.md` 的软链接，用于相容 Claude 生态。
- `.github/copilot-instructions.md` 与 `.github/instructions/*.instructions.md` 是 GitHub Copilot / Coding Agent 的镜像或分層补充；若与本文件冲突，以 `AGENTS.md` 为准。
- 倉庫协作 skill 存放在 `.claude/skills/`，分析产物存放在 `.claude/reviews/`；前者可以入库，后者預設视为本機产物。
- 根目錄 `SKILL.md` 与 `docs/openclaw-skill-integration.md` 属于产品或外部集成说明，不是倉庫协作規則真源。
- 若未来新增 `.agents/skills/` 或其他 agent 专用目錄，必须先明確单一真源，再通过脚本或镜像同步；禁止手工长期维护多份同义内容。
- 修改 AI 协作治理资产时，執行：

```bash
python scripts/check_ai_assets.py
```

## 3. 倉庫速览

- 项目定位：股票智能分析系統，覆盖 A 股、港股、美股。
- 主流程：抓取數據 -> 技术分析/新闻检索 -> LLM 分析 -> 生成报告 -> 通知推送。
- 關鍵入口：
  - `main.py`：分析工作主入口
  - `server.py`：FastAPI 服務入口
  - `apps/dsa-web/`：Web 前端
  - `apps/dsa-desktop/`：Electron 桌面端
  - `.github/workflows/`：CI、發佈、每日工作
- 核心职责：
  - `src/core/`：主流程编排
  - `src/services/`：业务服務层
  - `src/repositories/`：數據訪問层
  - `src/reports/`：报告生成
  - `src/schemas/`：Schema / 數據结构
  - `data_provider/`：多數據源適配与 fallback
  - `api/`：FastAPI API
  - `bot/`：机器人接入
  - `scripts/`：本機脚本
  - `.github/scripts/`：GitHub 自動化脚本
  - `tests/`：pytest 測試
  - `docs/`：文档与说明

## 4. 常用命令

### 執行应用

```bash
python main.py
python main.py --debug
python main.py --dry-run
python main.py --stocks 600519,hk00700,AAPL
python main.py --market-review
python main.py --schedule
python main.py --serve
python main.py --serve-only
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### 后端驗證

```bash
pip install -r requirements.txt
pip install flake8 pytest
./scripts/ci_gate.sh
python -m pytest -m "not network"
python -m py_compile <changed_python_files>
```

### Web / Desktop

```bash
cd apps/dsa-web
npm ci
npm run lint
npm run build

cd ../dsa-desktop
npm install
npm run build
```

### PR / CI 证据

```bash
gh pr view <pr_number>
gh pr checks <pr_number>
gh run view <run_id> --log-failed
```

## 5. 預設工作流

1. 先判斷工作类型：`fix / feat / refactor / docs / chore / test / review`
2. 先读现有實現、配置、測試、脚本、工作流和文档，再动手修改。
3. 识别改动邊界：后端 / API / Web / Desktop / Workflow / Docs / AI 协作资产。
4. 先判斷是否命中高風險区域：配置语义、API / Schema、數據源 fallback、报告结构、認證、调度、發佈流程、桌面端啟動鏈路。
5. 只做和当前工作直接相關的最小改动，不顺手夹带无关重构。
6. 如果发现文档、脚本、工作流描述不一致，優先信任實際代碼与工作流，再决定是否顺手修正文档。
7. 改完后按下面的驗證矩阵執行檢查。
8. 最終交付預設要说明：
   - 改了什么
   - 为什么这么改
   - 驗證情况
   - 未驗證项
   - 風險点
   - 回滚方式

## 6. 驗證矩阵

### CI 覆盖原则

当前倉庫 CI 主要包含：

| 檢查项 | 来源 | 说明 | 是否阻断 |
| --- | --- | --- | --- |
| `ai-governance` | `.github/workflows/ci.yml` | 校验 `AGENTS.md` / `CLAUDE.md` / `.github` 指令 / `.claude/skills` 关系 | 是 |
| `backend-gate` | `.github/workflows/ci.yml` | 執行 `./scripts/ci_gate.sh` | 是 |
| `docker-build` | `.github/workflows/ci.yml` | Docker 构建与關鍵模組匯入 smoke | 是 |
| `web-gate` | `.github/workflows/ci.yml` | 前端改动时執行 `npm run lint` + `npm run build` | 是（触发时） |
| `network-smoke` | `.github/workflows/network-smoke.yml` | `pytest -m network` + `scripts/test.sh quick` | 否，观测项 |
| `pr-review` | `.github/workflows/pr-review.yml` | PR 静态檢查 + AI 审查 + 自动標籤 | 否，辅助项 |

若 PR 上已有对应 CI 结果，可直接引用 CI 结论；若 CI 未覆盖改动面，或本機与 CI 環境差异较大，需要补充说明本機驗證与缺口。

### 按改动面執行

- Python 后端改动：
  - 适用範圍：`main.py`、`src/`、`data_provider/`、`api/`、`bot/`、`tests/`
  - 優先執行：`./scripts/ci_gate.sh`
  - 最低要求：`python -m py_compile <changed_python_files>`
  - 若影响 API、工作编排、报告生成、通知发送、數據源 fallback、認證、调度，交付说明中要写明是否覆盖了对应路徑。

- Web 前端改动：
  - 适用範圍：`apps/dsa-web/`
  - 預設執行：`cd apps/dsa-web && npm ci && npm run lint && npm run build`
  - 若涉及 API 联调、路由、狀態管理、Markdown/图表渲染或認證狀態，交付说明中要明確说明联动面和未覆盖風險。

- 桌面端改动：
  - 适用範圍：`apps/dsa-desktop/`、`scripts/run-desktop.ps1`、`scripts/build-desktop*.ps1`、`scripts/build-*.sh`、`docs/desktop-package.md`
  - 預設執行：先构建 Web，再构建桌面端
  - 如受平台限制未能完整驗證，需要明確说明是否驗證了 Web 构建产物、Electron 构建以及 Release 工作流影响。

- API / Schema / 認證联动改动：
  - 适用範圍：`api/**`、`src/schemas/**`、`src/services/**`、`apps/dsa-web/**`、`apps/dsa-desktop/**`
  - 至少覆盖对应后端驗證 + 受影响客户端构建驗證。
  - 若涉及登录、Cookie、會話、轮询狀態、欄位增删或枚举变化，必须明確写出相容性影响。

- 文档与治理文件改动：
  - 适用範圍：`README.md`、`docs/**`、`AGENTS.md`、`.github/copilot-instructions.md`、`.github/instructions/**`、`.claude/skills/**`
  - 不強制代碼測試。
  - 需确认命令、配置项、文件名、工作流名称与實際倉庫一致。
  - 改动 AI 协作治理资产时，執行 `python scripts/check_ai_assets.py`。

- 工作流 / 脚本 / Docker 改动：
  - 适用範圍：`.github/**`、`scripts/**`、`docker/**`
  - 執行最接近改动面的本機驗證。
  - 交付时说明影响了哪条流水线、發佈路徑或部署路徑。
  - 若未執行 Docker / GitHub Actions 相關驗證，明確说明原因与潜在風險。

- 網路或三方依賴相關改动：
  - 先跑离线或確定性檢查。
  - 優先确认 timeout、retry、fallback、例外文案、降級路徑是否仍然成立。
  - 若未執行在线驗證，必须明確写出原因。

## 7. 稳定性护栏

- 配置与執行入口：
  - 修改 `.env` 语义、預設值、CLI 參數、服務啟動方式、调度语义时，要同时評估本機執行、Docker、GitHub Actions、API、Web、Desktop 的影响。
  - 新配置優先做到“不配置也可執行，配置后增强能力”，避免叠加开关和互斥模式。

- 數據源与 fallback：
  - 修改 `data_provider/` 时，要关注數據源優先级、失败降級、欄位標準化、快取与逾時策略。
  - 单一數據源失败不应拖垮整个分析流程，除非需求明確要求 fail-fast。

- API / Web / Desktop 相容：
  - 改 API / Schema / 認證 / 报告载荷时，要同时檢查后端、Web、Desktop 的相容性。
  - 預設優先追加欄位、保留旧欄位或提供相容层，避免无提示破坏现有客户端。

- 报告 / Prompt / 通知：
  - 修改报告结构、Prompt、提取器、通知模板、机器人鏈路时，要檢查上游輸入与下游消费方是否仍相容。
  - 单一通知渠道失败不应拖垮整个分析主流程，除非需求明確要求 fail-fast。
  - 修改 `src/services/image_stock_extractor.py` 中 `EXTRACT_PROMPT` 时，要在 PR 描述中附完整最新 prompt。

- 工作流 / 發佈 / 打包：
  - 修改自动 tag、Release、Docker 發佈、日常分析或桌面端打包流程时，要評估触发條件、产物路徑、權限邊界和回滚方式。
  - 自动 tag 預設保持 opt-in：只有 commit title 含 `#patch`、`#minor`、`#major` 才触发版本号更新，除非需求明確要求改变發佈策略。

## 8. Issue / PR / Skill 工作流

- 倉庫内已有以下 skill，可優先复用：
  - `.claude/skills/analyze-issue/SKILL.md`
  - `.claude/skills/analyze-pr/SKILL.md`
  - `.claude/skills/fix-issue/SKILL.md`
- 如果工作明確是 issue 分析、PR 审查、issue 修复，優先按对应 skill 執行，并将产物保存到 `.claude/reviews/`。
- skill 中的命令、模板、驗證顺序和交付结构必须与 `AGENTS.md` 保持一致。
- skill 預設優先讀取 CI / 工作流证据，再决定是否补本機驗證。
- skill 不得預設執行 `git pull`、`git push`、`git tag`、`gh pr create` 等会改变远端或当前分支狀態的操作；这些操作必须要求使用者确认。
- PR 审查預設顺序：
  1. 必要性
  2. 關聯性
  3. 标题建议（`<类型>: <修改内容>`，且不含工具/agent 前綴；不作为硬性阻断项）
  4. 描述完整性（对照 `.github/PULL_REQUEST_TEMPLATE.md`）
  5. 驗證证据
  6. 實現正确性
  7. 合入判定
- 对 `fix` 类 PR，必须说明：原議題、根因、修复点、迴歸風險。
- 合入阻断條件：
  - 正确性或安全性議題
  - 阻断型 CI 未通过
  - PR 描述与實際改动内容实质性矛盾
  - 缺少回滚方案

## 9. 交付与發佈

- 預設交付结构：
  - `改了什么`
  - `为什么这么改`
  - `驗證情况`
  - `未驗證项`
  - `風險点`
  - `回滚方式`
- 如果是 `docs` 工作，可直接写：`Docs only, tests not run`，但仍需说明是否核对了命令和文件名。
- 自动 tag 預設不触发，只有 commit title 包含 `#patch`、`#minor`、`#major` 才会触发版本号更新。
- 手动打 tag 必须使用 annotated tag。
- 使用者可见变更優先通过 PR 合入，并补齐 label 与驗證说明。
