# Repository Claude Skills

本目錄存放倉庫级协作 skills，属于版本库资产。

- 規則真源：倉庫根目錄 `AGENTS.md`
- 相容入口：根目錄 `CLAUDE.md`（应为指向 `AGENTS.md` 的软链接）
- 本目錄中的 skill 需要与 `AGENTS.md` 保持一致
- `.claude/reviews/` 属于本機分析产物，不作为規則真源

如果未来需要相容其他 agent 目錄（如 `.agents/skills/` 或 `.github/skills/`），应先明確单一真源，再通过脚本或镜像同步，而不是手工长期维护多份同义内容。
