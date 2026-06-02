# -*- coding: utf-8 -*-
"""
===================================
平台適配器基类
===================================

定义平台適配器的抽象基类，各平台必须继承此类。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple

from bot.models import BotMessage, BotResponse, WebhookResponse


class BotPlatform(ABC):
    """
    平台適配器抽象基类
    
    负责：
    1. 驗證 Webhook 請求簽名
    2. 解析平台訊息为统一格式
    3. 将回應轉換为平台格式
    
    使用示例：
        class MyPlatform(BotPlatform):
            @property
            def platform_name(self) -> str:
                return "myplatform"
            
            def verify_request(self, headers, body) -> bool:
                # 驗證簽名邏輯
                return True
            
            def parse_message(self, data) -> Optional[BotMessage]:
                # 解析訊息邏輯
                return BotMessage(...)
            
            def format_response(self, response, message) -> WebhookResponse:
                # 格式化回應邏輯
                return WebhookResponse.success({"text": response.text})
    """
    
    @property
    @abstractmethod
    def platform_name(self) -> str:
        """
        平台标识名称
        
        用于路由匹配和日誌标识，如 "feishu", "dingtalk"
        """
        pass
    
    @abstractmethod
    def verify_request(self, headers: Dict[str, str], body: bytes) -> bool:
        """
        驗證請求簽名
        
        各平台有不同的簽名驗證機制，需要单独實現。
        
        Args:
            headers: HTTP 請求头
            body: 請求体原始字节
            
        Returns:
            簽名是否有效
        """
        pass
    
    @abstractmethod
    def parse_message(self, data: Dict[str, Any]) -> Optional[BotMessage]:
        """
        解析平台訊息为统一格式
        
        将平台特定的訊息格式轉換为 BotMessage。
        如果不是需要處理的訊息类型（如事件回调），傳回 None。
        
        Args:
            data: 解析后的 JSON 數據
            
        Returns:
            BotMessage 对象，或 None（不需要處理）
        """
        pass
    
    @abstractmethod
    def format_response(
        self, 
        response: BotResponse, 
        message: BotMessage
    ) -> WebhookResponse:
        """
        将统一回應轉換为平台格式
        
        Args:
            response: 统一回應对象
            message: 原始訊息对象（用于獲取回复目标等資訊）
            
        Returns:
            WebhookResponse 对象
        """
        pass
    
    def send_followup(
        self,
        response: 'BotResponse',
        message: 'BotMessage',
    ) -> bool:
        """Send a follow-up message after a deferred webhook response.

        Override in platforms that return a deferred acknowledgement
        (e.g. Discord type 5) so the final command result can be delivered
        asynchronously.  The default implementation is a no-op.

        Returns:
            ``True`` if the follow-up was sent successfully.
        """
        return False

    def handle_challenge(self, data: Dict[str, Any]) -> Optional[WebhookResponse]:
        """
        處理平台驗證請求
        
        部分平台在配置 Webhook 时会发送驗證請求，需要傳回特定回應。
        子类可重写此方法。
        
        Args:
            data: 請求數據
            
        Returns:
            驗證回應，或 None（不是驗證請求）
        """
        return None
    
    def handle_webhook(
        self, 
        headers: Dict[str, str], 
        body: bytes,
        data: Dict[str, Any]
    ) -> Tuple[Optional[BotMessage], Optional[WebhookResponse]]:
        """
        處理 Webhook 請求
        
        这是主入口方法，协调驗證、解析等流程。
        
        Args:
            headers: HTTP 請求头
            body: 請求体原始字节
            data: 解析后的 JSON 數據
            
        Returns:
            (BotMessage, WebhookResponse) 元组
            - 如果是驗證請求：(None, challenge_response)
            - 如果是普通訊息：(message, None) - 回應将在命令處理后生成
            - 如果驗證失败或無需處理：(None, error_response 或 None)
        """
        # 1. 檢查是否是驗證請求
        challenge_response = self.handle_challenge(data)
        if challenge_response:
            return None, challenge_response
        
        # 2. 驗證請求簽名
        if not self.verify_request(headers, body):
            return None, WebhookResponse.error("Invalid signature", 403)
        
        # 3. 解析訊息
        message = self.parse_message(data)
        
        return message, None
