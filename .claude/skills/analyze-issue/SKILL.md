# Analyze Issue

分析 GitHub Issue，判斷其真实性、優先级、倉庫责任邊界与建议动作。

**Repository**: https://github.com/ZhuLinsen/daily_stock_analysis/issues

## Usage

```text
/analyze-issue <issue_number>
```

## Instructions

分析时使用简洁中文，優先遵循倉庫根目錄 `AGENTS.md`。

### Step 1: 拉取 Issue 資訊

```bash
gh issue view <issue_number> --repo ZhuLinsen/daily_stock_analysis
gh issue view <issue_number> --repo ZhuLinsen/daily_stock_analysis --comments
```

如为 bug，優先核对 issue 模板中是否提供了以下資訊：

- 是否已同步到最新版本
- commit hash / 版本基线
- 執行環境与复现步骤
- 日誌或报错資訊

### Step 2: 回答 4 个核心議題

1. 版本是否明確
2. 議題是否真实且可驗證
3. 是否属于倉庫责任邊界
4. 是否值得立即處理

### Step 3: 结合倉庫现状做证据檢查

- 阅读相關代碼、配置、測試、脚本、工作流与文档
- 如果議題涉及 API、數據源 fallback、报告生成、通知发送、認證、桌面端、發佈流程，明確写出影响面
- 判斷是實際 bug、環境配置議題、使用方式議題、还是外部依賴議題
- 如怀疑已被修复，檢查当前代碼而不是只看 issue 描述

### Step 4: 形成结论

至少给出以下欄位：

- `版本基线`：最新 / 非最新 / 未提供
- `是否合理`：是/否 + 理由
- `是否是 issue`：是/否 + 理由
- `是否好解決`：是/否 + 难点
- `结论`：`成立 / 部分成立 / 不成立`
- `分類`：`bug / feature / docs / question / external`
- `優先级`：`P0 / P1 / P2 / P3`
- `难度`：`easy / medium / hard`
- `建议动作`：`立即修复 / 排期修复 / 文档澄清 / 關閉`

### Step 5: 生成分析文档

保存到 `.claude/reviews/issues/issue-<number>.md`

## Output Document Format

```markdown
# Issue #<number> Analysis

**Date**: YYYY-MM-DD
**Status**: Pending Review

## Summary

- 版本基线：
- 是否合理：
- 是否是 issue：
- 是否好解決：
- 结论：
- 分類：
- 優先级：
- 难度：
- 建议动作：

## Evidence

- 關鍵 issue 資訊：
- 關鍵代碼/脚本/工作流证据：

## Impact Scope

- 受影响模組：
- 受影响執行路徑（本機 / Docker / GitHub Actions / API / Web / Desktop）：

## Root Cause / Main Reasoning

<根因或主要判斷依据>

## Proposed Handling

<建议修复、澄清或關閉方式>

若建议后续建立 PR，给出的 PR title 建议符合 `AGENTS.md`：使用 `<类型>: <修改内容>`，不添加 `[codex]`、`codex`、`autocode`、`copilot` 或其他工具/agent 来源前綴；该约定仅用于协作一致性提醒，不应单独作为 review process blocker。

## Risks And Rollback

- 風險点：
- 若修复，回滚方式：

## Draft Reply

<建议回复内容>
```

## Allowed Auto-Actions (No Confirmation Needed)

- 拉取 issue 详情与評論
- 阅读相關代碼、配置、脚本、工作流和文档
- 生成分析文档

## Actions Requiring Confirmation

執行以下动作前，先询问使用者：

1. 添加或修改標籤
2. 在 issue 下評論
3. 關閉 issue
4. 开始修复 issue
