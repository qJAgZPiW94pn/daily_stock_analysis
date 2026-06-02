# -*- coding: utf-8 -*-
"""
===================================
A股自选股智能分析系統 - 分析服務层
===================================

职责：
1. 封装核心分析逻辑，支援多调用方（CLI、WebUI、Bot）
2. 提供清晰的API接口，不依賴于命令行參數
3. 支援依賴注入，便于測試和扩展
4. 统一管理分析流程和配置
"""

import uuid
from typing import List, Optional

from src.analyzer import AnalysisResult
from src.core.market_review import run_market_review
from src.core.pipeline import StockAnalysisPipeline
from src.config import Config, get_config
from src.enums import ReportType
from src.notification import NotificationService


def analyze_stock(
    stock_code: str,
    config: Config = None,
    full_report: bool = False,
    notifier: Optional[NotificationService] = None,
) -> Optional[AnalysisResult]:
    """
    分析单只股票

    Args:
        stock_code: 股票代碼
        config: 配置对象（可選，默认使用单例）
        full_report: 是否生成完整报告
        notifier: 通知服務（可選）

    Returns:
        分析结果对象
    """
    if config is None:
        config = get_config()

    # 建立分析流水线
    pipeline = StockAnalysisPipeline(
        config=config,
        query_id=uuid.uuid4().hex,
        query_source="cli"
    )

    # 使用通知服務（如果提供）
    if notifier:
        pipeline.notifier = notifier

    # 根据full_report參數设置报告类型
    report_type = ReportType.FULL if full_report else ReportType.SIMPLE

    # 執行单只股票分析
    result = pipeline.process_single_stock(
        code=stock_code,
        skip_analysis=False,
        single_stock_notify=notifier is not None,
        report_type=report_type,
    )

    return result


def analyze_stocks(
    stock_codes: List[str],
    config: Config = None,
    full_report: bool = False,
    notifier: Optional[NotificationService] = None,
) -> List[AnalysisResult]:
    """
    分析多只股票

    Args:
        stock_codes: 股票代碼列表
        config: 配置对象（可選，默认使用单例）
        full_report: 是否生成完整报告
        notifier: 通知服務（可選）

    Returns:
        分析结果列表
    """
    if config is None:
        config = get_config()

    results = []
    for stock_code in stock_codes:
        result = analyze_stock(stock_code, config, full_report, notifier)
        if result:
            results.append(result)

    return results


def perform_market_review(
    config: Config = None,
    notifier: Optional[NotificationService] = None,
) -> Optional[str]:
    """
    执行大盤复盘

    Args:
        config: 配置对象（可選，默认使用单例）
        notifier: 通知服務（可選）

    Returns:
        复盘报告内容
    """
    if config is None:
        config = get_config()

    # 建立分析流水线以获取analyzer和search_service
    pipeline = StockAnalysisPipeline(
        config=config,
        query_id=uuid.uuid4().hex,
        query_source="cli",
    )

    # 使用提供的通知服務或建立新的
    review_notifier = notifier or pipeline.notifier

    # 调用大盤复盘函數
    return run_market_review(
        notifier=review_notifier,
        analyzer=pipeline.analyzer,
        search_service=pipeline.search_service,
    )

