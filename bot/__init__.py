# -*- coding: utf-8 -*-
"""
===================================
机器人命令触发系統
===================================

通过 @机器人 或发送命令触发股票分析等功能。
支援飞书、钉钉、企业微信、Telegram 等多平台。

模組结构：
- models.py: 统一的訊息/回應模型
- dispatcher.py: 命令分发器
- commands/: 命令處理器
- platforms/: 平台適配器
- handler.py: Webhook 處理器

使用方式：
1. 配置環境變數（各平台的 Token 等）
2. 啟動 WebUI 服務
3. 在各平台配置 Webhook URL：
   - 飞书: http://your-server/bot/feishu
   - 钉钉: http://your-server/bot/dingtalk
   - 企业微信: http://your-server/bot/wecom
   - Telegram: http://your-server/bot/telegram

支援的命令：
- /analyze <股票代碼>  - 分析指定股票
- /market             - 大盤复盘
- /batch              - 批量分析自选股
- /help               - 顯示帮助
- /status             - 系統狀態
"""

from bot.models import BotMessage, BotResponse, ChatType, WebhookResponse
from bot.dispatcher import CommandDispatcher, get_dispatcher

__all__ = [
    'BotMessage',
    'BotResponse',
    'ChatType',
    'WebhookResponse',
    'CommandDispatcher',
    'get_dispatcher',
]
