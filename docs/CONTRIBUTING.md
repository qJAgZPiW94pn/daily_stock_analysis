# 贡献指南

感谢你对本项目的关注！欢迎任何形式的贡献。

## 🐛 报告 Bug

1. 先搜索 [Issues](https://github.com/ZhuLinsen/daily_stock_analysis/issues) 确认議題未被报告
2. 使用 Bug Report 模板建立新 Issue
3. 提供详细的复现步骤和环境資訊

## 💡 功能建议

1. 先搜索 Issues 确认建议未被提出
2. 使用 Feature Request 模板建立新 Issue
3. 详细描述你的使用场景和期望功能

## 🔧 提交代碼

### 开发环境

```bash
# 克隆倉庫
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git
cd daily_stock_analysis

# 建立虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安裝依賴
pip install -r requirements.txt

# 配置环境變數
cp .env.example .env
```

### 提交流程

1. Fork 本倉庫
2. 建立特性分支：`git checkout -b feature/your-feature`
3. 提交改动：`git commit -m 'feat: add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 建立 Pull Request

### Commit 规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
feat: 新功能
fix: Bug 修复
docs: 文档更新
style: 代碼格式（不影响功能）
refactor: 重构
perf: 效能最佳化
test: 測試相关
chore: 构建/工具相关
```

示例：
```
feat: 添加钉钉机器人支援
fix: 修复 429 限流重试逻辑
docs: 更新 README 部署说明
```

### 代碼规范

- Python 代碼遵循 PEP 8
- 函數和类需要添加 docstring
- 重要逻辑添加注释
- 新功能需要更新相关文档

### CI 自动检查

提交 PR 后，CI 会自动執行以下检查：

| 检查项 | 说明 | 必须通过 |
|--------|------|:--------:|
| backend-gate | `scripts/ci_gate.sh`（py_compile + flake8 严重錯誤 + 本機核心脚本 + offline pytest） | ✅ |
| docker-build | Docker 镜像构建与关键模块匯入 smoke | ✅ |
| web-gate | 前端变更时执行 `npm run lint` + `npm run build` | ✅（触发时） |
| network-smoke | 定时/手动执行 `pytest -m network` + `scripts/test.sh quick`（非阻断） | ❌（观测项） |

**本機執行检查：**

```bash
# backend gate（推荐）
pip install -r requirements.txt
pip install flake8 pytest
./scripts/ci_gate.sh

# 前端 gate（如修改了 apps/dsa-web）
cd apps/dsa-web
npm ci
npm run lint
npm run build
```

## 📋 优先贡献方向

查看 [Roadmap](README.md#-roadmap) 了解当前需要的功能：

- 🔔 新通知渠道（钉钉、飞书、Telegram）
- 🤖 新 AI 模型支援（GPT-4、Claude）
- 📊 新數據源接入
- 🐛 Bug 修复和效能最佳化
- 📖 文档完善和翻译

## ❓ 議題解答

如有任何議題，欢迎：
- 建立 Issue 討論
- 查看已有 Issue 和 Discussion

再次感谢你的贡献！ 🎉
