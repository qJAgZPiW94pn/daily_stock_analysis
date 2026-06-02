# -*- coding: utf-8 -*-
"""
===================================
命令基类
===================================

定义命令處理器的抽象基类，所有命令都必须继承此类。
"""

import asyncio
from abc import ABC, abstractmethod
from typing import List, Optional

from bot.models import BotMessage, BotResponse


class BotCommand(ABC):
    """
    命令處理器抽象基类

    所有命令都必须继承此类并實現抽象方法。

    使用示例：
        class MyCommand(BotCommand):
            @property
            def name(self) -> str:
                return "mycommand"

            @property
            def aliases(self) -> List[str]:
                return ["mc", "我的命令"]

            @property
            def description(self) -> str:
                return "这是我的命令"

            @property
            def usage(self) -> str:
                return "/mycommand [參數]"

            def execute(self, message: BotMessage, args: List[str]) -> BotResponse:
                return BotResponse.text_response("命令執行成功")
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        命令名称（不含前綴）

        例如 "analyze"，使用者輸入 "/analyze" 触发
        """
        pass

    @property
    @abstractmethod
    def aliases(self) -> List[str]:
        """
        命令别名列表

        例如 ["a", "分析"]，使用者輸入 "/a" 或 "分析" 也能触发
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """命令描述（用于帮助資訊）"""
        pass

    @property
    @abstractmethod
    def usage(self) -> str:
        """
        使用说明（用于帮助資訊）

        例如 "/analyze <股票代碼>"
        """
        pass

    @property
    def hidden(self) -> bool:
        """
        是否在帮助列表中隱藏

        預設 False，设为 True 则不顯示在 /help 列表中
        """
        return False

    @property
    def admin_only(self) -> bool:
        """
        是否仅管理员可用

        預設 False，设为 True 则需要管理员權限
        """
        return False

    @abstractmethod
    def execute(self, message: BotMessage, args: List[str]) -> BotResponse:
        """
        執行命令

        Args:
            message: 原始訊息对象
            args: 命令參數列表（已分割）

        Returns:
            BotResponse 回應对象
        """
        pass

    async def execute_async(self, message: BotMessage, args: List[str]) -> BotResponse:
        """非同步執行命令。

        預設将同步 `execute()` 下沉到執行緒池，避免在非同步分发鏈路中阻塞事件循环。
        """
        return await asyncio.to_thread(self.execute, message, args)

    def validate_args(self, args: List[str]) -> Optional[str]:
        """
        驗證參數

        子类可重写此方法進行參數校验。

        Args:
            args: 命令參數列表

        Returns:
            如果參數有效傳回 None，否则傳回錯誤資訊
        """
        return None

    def get_help_text(self) -> str:
        """獲取帮助文本"""
        return f"**{self.name}** - {self.description}\n用法: `{self.usage}`"
