# -*- coding: utf-8 -*-
"""
===================================
机器人訊息模型
===================================

定义统一的訊息和回應模型，屏蔽各平台差异。
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List


class ChatType(str, Enum):
    """会话类型"""
    GROUP = "group"      # 群聊
    PRIVATE = "private"  # 私聊
    UNKNOWN = "unknown"  # 未知


class Platform(str, Enum):
    """平台类型"""
    FEISHU = "feishu"        # 飞书
    DINGTALK = "dingtalk"    # 钉钉
    WECOM = "wecom"          # 企业微信
    TELEGRAM = "telegram"    # Telegram
    UNKNOWN = "unknown"      # 未知


@dataclass
class BotMessage:
    """
    统一的机器人訊息模型
    
    将各平台的訊息格式统一为此模型，便于命令處理器處理。
    
    Attributes:
        platform: 平台标识
        message_id: 訊息 ID（平台原始 ID）
        user_id: 发送者 ID
        user_name: 发送者名称
        chat_id: 会话 ID（群聊 ID 或私聊 ID）
        chat_type: 会话类型
        content: 訊息文本内容（已去除 @机器人 部分）
        raw_content: 原始訊息内容
        mentioned: 是否 @了机器人
        mentions: @的使用者列表
        timestamp: 訊息时间戳
        raw_data: 原始請求數據（平台特定，用于调试）
    """
    platform: str
    message_id: str
    user_id: str
    user_name: str
    chat_id: str
    chat_type: ChatType
    content: str
    raw_content: str = ""
    mentioned: bool = False
    mentions: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    def get_command_and_args(self, prefix: str = "/") -> tuple:
        """
        解析命令和參數
        
        Args:
            prefix: 命令前缀，默认 "/"
            
        Returns:
            (command, args) 元组，如 ("analyze", ["600519"])
            如果不是命令，傳回 (None, [])
        """
        text = self.content.strip()
        
        # 检查是否以命令前缀开头
        if not text.startswith(prefix):
            # 尝试匹配中文命令（无前缀）
            chinese_commands = {
                '分析': 'analyze',
                '大盤': 'market',
                '批量': 'batch',
                '帮助': 'help',
                '狀態': 'status',
            }
            for cn_cmd, en_cmd in chinese_commands.items():
                if text.startswith(cn_cmd):
                    args = text[len(cn_cmd):].strip().split()
                    return en_cmd, args
            return None, []
        
        # 去除前缀
        text = text[len(prefix):]
        
        # 分割命令和參數
        parts = text.split()
        if not parts:
            return None, []
        
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        return command, args
    
    def is_command(self, prefix: str = "/") -> bool:
        """检查訊息是否是命令"""
        cmd, _ = self.get_command_and_args(prefix)
        return cmd is not None


@dataclass
class BotResponse:
    """
    统一的机器人回應模型
    
    命令處理器傳回此模型，由平台适配器转换为平台特定格式。
    
    Attributes:
        text: 回复文本
        markdown: 是否为 Markdown 格式
        at_user: 是否 @发送者
        reply_to_message: 是否回复原訊息
        extra: 额外數據（平台特定）
    """
    text: str
    markdown: bool = False
    at_user: bool = True
    reply_to_message: bool = True
    extra: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def text_response(cls, text: str, at_user: bool = True) -> 'BotResponse':
        """建立纯文本回應"""
        return cls(text=text, markdown=False, at_user=at_user)
    
    @classmethod
    def markdown_response(cls, text: str, at_user: bool = True) -> 'BotResponse':
        """建立 Markdown 回應"""
        return cls(text=text, markdown=True, at_user=at_user)
    
    @classmethod
    def error_response(cls, message: str) -> 'BotResponse':
        """建立錯誤回應"""
        return cls(text=f"❌ 錯誤：{message}", markdown=False, at_user=True)


@dataclass
class WebhookResponse:
    """
    Webhook 回應模型
    
    平台适配器傳回此模型，包含 HTTP 回應内容。
    
    Attributes:
        status_code: HTTP 狀態码
        body: 回應体（字典，将被 JSON 序列化）
        headers: 额外的回應头
    """
    status_code: int = 200
    body: Dict[str, Any] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    
    @classmethod
    def success(cls, body: Optional[Dict] = None) -> 'WebhookResponse':
        """建立成功回應"""
        return cls(status_code=200, body=body or {})
    
    @classmethod
    def challenge(cls, challenge: str) -> 'WebhookResponse':
        """建立验证回應（用于平台 URL 验证）"""
        return cls(status_code=200, body={"challenge": challenge})
    
    @classmethod
    def error(cls, message: str, status_code: int = 400) -> 'WebhookResponse':
        """建立錯誤回應"""
        return cls(status_code=status_code, body={"error": message})
