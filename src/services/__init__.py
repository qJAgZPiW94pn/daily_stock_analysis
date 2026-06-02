# -*- coding: utf-8 -*-
"""
===================================
服務层模組初始化
===================================

职责：
1. 声明可匯出的服務类（延遲匯入，避免啟動时拉入 LLM 等重依賴）

使用方式：
    直接从子模組匯入，例如:
    from src.services.history_service import HistoryService
"""


def __getattr__(name: str):
    """延遲匯入：仅在通过 src.services.X 訪問时才加载对应子模組。"""
    _lazy_map = {
        "AnalysisService": "src.services.analysis_service",
        "BacktestService": "src.services.backtest_service",
        "HistoryService": "src.services.history_service",
        "StockService": "src.services.stock_service",
        "TaskService": "src.services.task_service",
        "get_task_service": "src.services.task_service",
    }
    if name in _lazy_map:
        import importlib
        module = importlib.import_module(_lazy_map[name])
        return getattr(module, name)
    raise AttributeError(f"module 'src.services' has no attribute {name!r}")


__all__ = [
    "AnalysisService",
    "BacktestService",
    "HistoryService",
    "StockService",
    "TaskService",
    "get_task_service",
]
