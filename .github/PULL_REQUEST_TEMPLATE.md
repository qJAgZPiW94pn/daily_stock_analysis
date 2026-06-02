<!--
For Chinese contributors: 请直接用中文填写。
For English contributors: please fill in English. All fields marked (EN) accept English.
-->

## PR Type

- [ ] fix
- [ ] feat
- [ ] refactor
- [ ] docs
- [ ] chore
- [ ] test

## Background And Problem

请描述当前議題、影响範圍与触发場景。  
*(EN) Describe the problem, its impact, and what triggers it.*

## Scope Of Change

请列出本 PR 修改的模組和文件範圍。  
*(EN) List the modules and files changed in this PR.*

## Issue Link

必须填写以下之一 / Fill in one of:
- `Fixes #<issue_number>`
- `Refs #<issue_number>`
- 无 Issue 时说明原因与验收標準 / If no issue, explain the motivation and acceptance criteria

## Verification Commands And Results

请填写你實際執行过的命令和關鍵结果（不要只写"已測試"）。  
*(EN) Paste the commands you actually ran and their key output (don't just write "tested"):*

```bash
# example
./scripts/ci_gate.sh
python -m pytest -m "not network"
```

關鍵輸出/结论 / Key output & conclusion:

## Compatibility And Risk

请说明相容性影响、潜在風險（如无请写 `None`）。  
*(EN) Describe compatibility impact and potential risks (write `None` if not applicable).*

- 若本 PR 修改第三方模型 / API 的相容语义、請求參數、路由前綴或 provider fallback，请提供**官方来源链接或公告**，并说明这是长期約束、当前執行时約束还是暫時相容處理。  
  *(EN) If this PR changes third-party model/API compatibility, request parameters, routing prefixes, or provider fallback behavior, include an **official source link or announcement** and clarify whether the rule is permanent, runtime-specific, or a temporary compatibility workaround.)*
- 若本 PR 依賴特定執行时 / 锁定依賴窗口（例如 LiteLLM 版本範圍、OpenAI-compatible 路由、YAML alias 行为），请写明当前驗證过的相容範圍与覆盖路徑。  
  *(EN) If this PR depends on a specific runtime or pinned dependency window (for example a LiteLLM version range, OpenAI-compatible routing, or YAML alias behavior), state the compatibility window you verified and which code paths were covered.)*
- 若本 PR 触及執行时配置保存、清理、迁移或回填邏輯，请明確说明旧配置是否会被自动改写、清空、迁移或保持不变，以及使用者如何恢復原行为。  
  *(EN) If this PR touches runtime config save/cleanup/migration/backfill logic, explicitly describe whether existing config is rewritten, cleared, migrated, or left intact, and how users can restore the previous behavior.)*

## Rollback Plan

请至少写一句可執行的回滚方案（必填）。  
*(EN) Provide at least one actionable rollback step (required).*

- 如果是相容性修复，預設应写出**最小回滚方式**（例如 `revert this PR`），并说明是否需要额外回滚配置或數據迁移。  
  *(EN) For compatibility fixes, include the **minimal rollback path** (for example `revert this PR`) and whether any additional config or data rollback is required.)*

## EXTRACT_PROMPT Change (if applicable)

若本 PR 修改了 `src/services/image_stock_extractor.py` 中的 `EXTRACT_PROMPT`，请在此处粘贴完整变更后的 prompt。  
*If this PR changes `EXTRACT_PROMPT` in `src/services/image_stock_extractor.py`, paste the full updated prompt here:*

<details>
<summary>展开 / Expand: Full EXTRACT_PROMPT</summary>

```
(paste full prompt here)
```

</details>

## Checklist

- [ ] 本 PR 有明確动机和业务价值 / This PR has a clear motivation and value
- [ ] 已提供可复现的驗證命令与结果 / Reproducible verification commands and results are included
- [ ] 已評估相容性与風險 / Compatibility and risk have been assessed
- [ ] 已提供回滚方案 / A rollback plan is provided
- [ ] 若涉及使用者可见变更，已同步更新相關文档与 `docs/CHANGELOG.md`；`README.md` 仅在首页级資訊变化时更新，细节優先写入 `docs/*.md` / If user-visible changes are included, relevant docs and `docs/CHANGELOG.md` are updated; `README.md` is updated only for homepage-level changes, with details kept in `docs/*.md`
