# -*- coding: utf-8 -*-
"""
大盤复盘市场区域配置

定义各市场区域的指數、新闻搜尋词、Prompt 提示等元數據，
供 MarketAnalyzer 按 region 切換 A 股/美股复盘行为。
"""

from dataclasses import dataclass
from typing import List


@dataclass
class MarketProfile:
    """大盤复盘市场区域配置"""

    region: str  # "cn" | "us"
    # 用于判斷整体走勢的指數代碼，cn 用上证 000001，us 用标普 SPX
    mood_index_code: str
    # 新闻搜尋關鍵词
    news_queries: List[str]
    # 指數点评 Prompt 提示语
    prompt_index_hint: str
    # 市场概况是否包含漲跌家数、漲停跌停（A 股有，美股无）
    has_market_stats: bool
    # 市场概况是否包含板塊漲跌（A 股有，美股暂无）
    has_sector_rankings: bool


CN_PROFILE = MarketProfile(
    region="cn",
    mood_index_code="000001",
    news_queries=[
        "A股 大盤 复盘",
        "股市 行情 分析",
        "A股 市场 热点 板塊",
    ],
    prompt_index_hint="分析上证、深证、创业板等各指數走勢特点",
    has_market_stats=True,
    has_sector_rankings=True,
)

US_PROFILE = MarketProfile(
    region="us",
    mood_index_code="SPX",
    news_queries=[
        "美股 大盤",
        "US stock market",
        "S&P 500 NASDAQ",
    ],
    prompt_index_hint="分析标普500、纳斯达克、道指等各指數走勢特点",
    has_market_stats=False,
    has_sector_rankings=False,
)

HK_PROFILE = MarketProfile(
    region="hk",
    mood_index_code="HSI",
    news_queries=[
        "港股 大盤 复盘",
        "Hong Kong stock market",
        "恒生指數 行情",
    ],
    prompt_index_hint="分析恒生指數、恒生科技指數、国企指數等各指數走勢特点",
    has_market_stats=False,
    has_sector_rankings=False,
)


def get_profile(region: str) -> MarketProfile:
    """根据 region 傳回对应的 MarketProfile"""
    if region == "us":
        return US_PROFILE
    if region == "hk":
        return HK_PROFILE
    return CN_PROFILE
