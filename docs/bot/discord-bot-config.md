# Discord机器人配置

## Discord机器人
Discord机器人接收訊息需要使用Discord Developer Portal建立机器人应用
https://discord.com/developers/applications

Discord机器人支援两种訊息发送方式：
1. **Webhook模式**：配置簡單，權限低，适合只需要发送訊息的場景
2. **Bot API模式**：權限高，支援接收命令，需要配置Bot Token和频道ID

## 建立Discord机器人

### 1. 登录Discord Developer Portal
訪問 https://discord.com/developers/applications 并使用你的Discord账号登录

### 2. 建立应用
点击"New Application"按钮，輸入应用名称（例如：A股智能分析机器人），然后点击"Create"

### 3. 配置机器人
在左侧导航栏中点击"Bot"，然后点击"Add Bot"按钮，确认添加

### 4. 獲取Bot Token
在Bot页面，点击"Reset Token"按钮，然后复制生成的Token（这是你的`DISCORD_BOT_TOKEN`）

### 5. 配置權限
在Bot页面的"Privileged Gateway Intents"部分，开启以下选项：
- Presence Intent
- Server Members Intent
- Message Content Intent

### 6. 添加到服務器
1. 在左侧导航栏中点击"OAuth2" > "URL Generator"
2. 在"Scopes"中选择：
   - `bot`
   - `applications.commands`
3. 在"Bot Permissions"中选择：
   - Send Messages
   - Embed Links
   - Attach Files
   - Read Message History
   - Use Slash Commands
4. 复制生成的URL，在浏览器中打开，选择要添加机器人的服務器

### 7. 獲取频道ID
1. 在Discord客户端中，开启开发者模式：设置 > 進階 > 开发者模式
2. 右键点击你想要机器人发送訊息的频道，选择"Copy ID"（这是你的`DISCORD_MAIN_CHANNEL_ID`）

## 配置環境變數

将以下配置添加到你的`.env`文件中：

```env
# Discord 机器人配置
DISCORD_BOT_TOKEN=your-discord-bot-token
DISCORD_MAIN_CHANNEL_ID=your-channel-id
DISCORD_WEBHOOK_URL=your-webhook-url (可選)
DISCORD_INTERACTIONS_PUBLIC_KEY=your-public-key (仅接收入站 Interaction/Webhook 回调时需要)
DISCORD_BOT_STATUS=A股智能分析 | /help
```

如果你配置了 Discord Interaction / Webhook 入站回调，务必在 Discord Developer Portal 的 `General Information -> Public Key` 复制公钥并填入 `DISCORD_INTERACTIONS_PUBLIC_KEY`；系統会使用该公钥校验每个入站請求的 Ed25519 簽名，验签失败会直接拒絕請求。

## Webhook模式配置（可選）

如果你只想使用Webhook模式发送訊息，不需要Bot Token，可以按照以下步骤配置：

1. 右键点击频道，选择"编辑频道"
2. 点击"集成" > "Webhooks" > "新建Webhook"
3. 配置Webhook名称和头像
4. 复制Webhook URL（这是你的`DISCORD_WEBHOOK_URL`）

## 支援的命令

Discord机器人支援以下Slash命令：

1. `/analyze <stock_code> [full_report]` - 分析指定股票代碼
   - `stock_code`: 股票代碼，如 600519
   - `full_report`: 可選，是否生成完整报告（包含大盤）

2. `/market_review` - 獲取大盤复盘报告

3. `/help` - 查看帮助資訊

## 測試机器人

1. 確保机器人已成功添加到你的服務器
2. 在频道中輸入`/help`，机器人会傳回帮助資訊
3. 輸入`/analyze 600519`測試股票分析功能
4. 輸入`/market_review`測試大盤复盘功能

## 注意事项

1. 確保你的机器人有足够的權限在频道中发送訊息和使用Slash命令
2. 定期更新你的Bot Token，確保安全性
3. 不要将你的Bot Token分享给任何人
4. 如果机器人没有回應，檢查：
   - Bot Token是否正确
   - 频道ID是否正确
   - 机器人是否在线
   - 机器人是否有訊息发送權限

## 故障排除

- **机器人不回應命令**：檢查Bot Token和频道ID是否正确，確保机器人已添加到服務器
- **Slash命令不顯示**：等待一段时间（Discord需要同步命令），或重新添加机器人
- **訊息发送失败**：檢查频道權限，確保机器人有发送訊息的權限

## 相關链接

- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord Bot Documentation](https://discordpy.readthedocs.io/en/stable/)
- [Discord Slash Commands](https://discord.com/developers/docs/interactions/application-commands)
