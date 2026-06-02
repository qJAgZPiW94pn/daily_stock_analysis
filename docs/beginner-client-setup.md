# 小白客户端安裝与配置指南

这份文档写给不会代碼、只想下載客户端直接用的使用者。目标很简单：下載客户端，填一个模型服務密钥（Key），填股票代碼，然后生成第一份分析报告。

> 本项目生成的是辅助分析报告，不构成投资建议。真实交易请自行判断風險。

## 先准备

1. Windows 或 macOS 电脑。
2. 一个模型服務密钥（Key），推荐从下面任选一个：
   - [Anspire Open](https://open.anspire.cn/?share_code=QFBC0FYC)：支援全球主流模型，一个 Key 可同时用于模型和新闻搜索，第一次配置最省事。
   - [AIHubMix](https://aihubmix.com/?aff=CfMq)：支援全球主流模型，适合想在一个平台切换多种模型的使用者。
3. 想分析的股票代碼，例如 `600519,hk00700,AAPL`。

## 1. 下載客户端

打开發佈页：

<https://github.com/ZhuLinsen/daily_stock_analysis/releases/latest>

在页面下方 `Assets`（附件）里下載：

| 电脑 | 下載哪个 |
| --- | --- |
| Windows | `daily-stock-analysis-windows-installer-<版本号>.exe` |
| Windows 不想安裝 | `daily-stock-analysis-windows-noinstall-<版本号>.zip` |
| macOS Apple 芯片 | `daily-stock-analysis-macos-arm64-<版本号>.dmg` |
| macOS Intel 芯片 | `daily-stock-analysis-macos-x64-<版本号>.dmg` |

不用下載 `latest.yml`、`*.blockmap`，它们不是客户端安裝包。

不知道 Mac 是哪种芯片：点击左上角苹果图标 -> 关于本机，看到 M1/M2/M3/M4 就选 `arm64`，看到 Intel 就选 `x64`。

## 2. 安裝并打开

- Windows 安裝包：双击 `.exe`，按提示安裝，安裝目錄用默认位置即可。
- Windows 免安裝包：解压 `.zip`，双击 `Daily Stock Analysis.exe`。
- macOS：双击 `.dmg`，把应用拖到 `Applications`。如果提示来自未验证开发者，在系統设置的隐私与安全性里允许打开。

macOS 使用者升級前建议先在客户端设置里匯出一次配置備份。

## 3. 配置 AI 模型

打开客户端，进入：

`系統设置 -> AI 模型`

只选下面一个方案即可。

> 重要：每次改完设置后，都要点击页面上的保存按钮；看到保存成功提示后，再切换页面或回到首页。

### 方案 A：Anspire Open

1. 打开 [Anspire Open](https://open.anspire.cn/?share_code=QFBC0FYC)，注册 / 登录后建立 API Key。
2. 回到客户端，在快速添加渠道里选择 `Anspire Open`。
3. 粘贴 API Key。
4. 模型名选择控制台里已开通的模型；不確定就先选控制台推荐或轻量模型。
5. 点击保存；看到保存成功后，再点击測試連線。

### 方案 B：AIHubMix

1. 打开 [AIHubMix](https://aihubmix.com/?aff=CfMq)，注册 / 登录后建立 API Key。
2. 回到客户端，在快速添加渠道里选择 `AIHubmix（聚合平台）`。
3. 粘贴 API Key。
4. 模型名选择控制台里已开通的模型；不確定就先选控制台推荐模型。
5. 点击保存；看到保存成功后，再点击測試連線。

看到測試成功，就繼續下一步。

## 4. 填写自选股

进入：

`系統设置 -> 基础设置`

找到 `自选股列表`，填写：

`600519,hk00700,AAPL`

多個股票用英文逗号隔开。常见写法：

- A 股：`600519`、`300750`、`000001`
- 港股：`hk00700`、`hk09988`
- 美股：`AAPL`、`TSLA`、`NVDA`

填完点击保存，看到保存成功后再回首页。

## 5. 建议配置新闻源

新闻源不是必填，但建议配置。它会影响近期新闻、公告、事件驱动、热点题材和風險提示。

进入：

`系統设置 -> 數據源`

按你的模型服務选择：

1. 用 Anspire Open：找到 `Anspire API Keys`，填入同一个 Anspire Key，保存成功后即可。
2. 用 AIHubMix：建议再申请 [SerpAPI](https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis) 或 [Tavily](https://tavily.com/) 的 Key，填到 `SerpAPI API Keys` 或 `Tavily API Keys`，保存成功后即可。

想先试用也可以略過新闻源，客户端仍然能生成基础分析。

## 6. 开始分析

回到首页：

1. 输入股票代碼，例如 `600519`。
2. 点击分析。
3. 等工作从排队、分析中变成分析完成。
4. 在历史记录里查看报告。

## 常见議題

### 下載页面里文件很多，该下哪个？

普通 Windows 使用者下載 `.exe` 安裝包。不要下載 `latest.yml` 或 `*.blockmap`。

### API Key 填了还是不能用？

检查这几项：

1. Key 是否复制完整，没有多余空格。
2. 平台账号是否有余额或额度。
3. 当前模型是否已开通。
4. 測試連線里是否提示模型不存在、權限不足或余额不足。

### 配置乱了怎么办？

在客户端设置里匯出配置備份。出議題时可以匯入之前的備份，或者只保留这三项重新配置：AI 模型、自选股、新闻源。
