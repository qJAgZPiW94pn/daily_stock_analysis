# Fix Issue

基于 issue 分析结果實現修复，并按倉庫規則补齐驗證、風險与回滚说明。

**Repository**: https://github.com/ZhuLinsen/daily_stock_analysis

## Usage

```text
/fix-issue <issue_number>
```

## Prerequisites

優先先完成 `/analyze-issue <issue_number>`，確保議題成立且邊界清晰。

## Instructions

### Step 1: 确认分析基线

檢查 `.claude/reviews/issues/issue-<number>.md` 是否存在；如果不存在，先补做 issue 分析或在本次修复中补齐最小分析结论。

### Step 2: 选择安全的工作方式

- 預設基于当前工作树做最小相關改动
- 不要預設執行 `git pull`
- 不要預設切換分支或改写使用者当前工作狀態
- 如果使用者明確要求建分支，再執行最小必要的分支操作

### Step 3: 实施修复

- 根据 issue 结论定位相關文件
- 優先复用现有模組、配置入口、脚本和測試
- 保持預設行为向后相容，避免破坏 fallback / fail-open
- 如果修复涉及使用者可见行为、配置语义、CLI/API、部署、通知、报告结构，要同步更新相關文档、`docs/CHANGELOG.md`、`.env.example`
- 向 `docs/CHANGELOG.md` 写入条目时，在 `[Unreleased]` 段追加一行，格式为 `- [类型] 描述`，其中 `[类型]` 从 `[新功能]/[改进]/[修复]/[文档]/[測試]/[chore]` 中按本次变更内容选择；只有修复 bug 时才使用 `[修复]`；**不要**在 `[Unreleased]` 内新增 `### 类目标题`
- `README.md` 只承载项目定位、核心能力、快速开始、主要入口、赞助/合作等首页级資訊；非必要不更新 README，避免持续膨胀
- 更细的模組行为、页面交互、专题配置、排障说明、欄位契约、實現语义和邊界條件，優先更新对应 `docs/*.md`

### Step 4: 按改动面驗證

按 `AGENTS.md` 的驗證矩阵執行最接近的檢查：

- 后端優先：`./scripts/ci_gate.sh`
- 最低后端要求：`python -m py_compile <changed_python_files>`
- 前端：`cd apps/dsa-web && npm ci && npm run lint && npm run build`
- 桌面端：先构建 Web，再构建桌面端

如無法完成完整驗證，必须记录缺口、原因与潜在風險。

### Step 5: 更新 issue 分析文档

在 `.claude/reviews/issues/issue-<number>.md` 中补充：

```markdown
## Fix Implementation

**Date**: YYYY-MM-DD

### Changes Made

- 文件与改动点：

### Validation

- 已執行：
- 未執行：

### Risks

- 風險点：

### Rollback

- 回滚方式：
```

### Step 6: 需要确认的后续动作

如使用者要求建立 PR、生成 PR 标题或整理 PR 描述，PR title 建议遵循 `AGENTS.md`：

- 使用 `<类型>: <修改内容>` 格式，例如 `fix: 修复大盤分析历史记录丢失`
- 类型優先使用 `fix`/`feat`/`refactor`/`docs`/`chore`/`test`/`ci`
- 标题只描述實際改动，建议不添加 `[codex]`、`codex`、`autocode`、`copilot` 或其他工具/agent 来源前綴
- 该约定仅用于协作一致性，不应被单独当作 process blocker

只有在使用者明確确认后，才執行：

- 建分支
- `git commit`
- `git push`
- 建立 PR
- 在 issue 下回复或關閉 issue

## Allowed Auto-Actions (No Confirmation Needed)

- 阅读和分析代碼
- 应用与当前工作直接相關的最小修复
- 執行非破坏性的本機驗證
- 更新本機 issue 分析文档

## Actions Requiring Confirmation

1. 切換或建立分支
2. `git commit`
3. `git push`
4. 建立 PR
5. 回复或關閉 issue
