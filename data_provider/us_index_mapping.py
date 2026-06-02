# -*- coding: utf-8 -*-
"""
===================================
美股指數与股票代碼工具
===================================

提供：
1. 美股指數代碼映射（如 SPX -> ^GSPC）
2. 美股股票代碼识别（AAPL、TSLA 等）

美股指數在 Yahoo Finance 中需使用 ^ 前缀，与股票代碼不同。
"""

import re

# 美股代碼正则：1-5 个大写字母，可選 .X 后缀（如 BRK.B）
_US_STOCK_PATTERN = re.compile(r'^[A-Z]{1,5}(\.[A-Z])?$')


# 使用者输入 -> (Yahoo Finance 符号, 中文名称)
US_INDEX_MAPPING = {
    # 标普 500
    'SPX': ('^GSPC', '标普500指數'),
    '^GSPC': ('^GSPC', '标普500指數'),
    'GSPC': ('^GSPC', '标普500指數'),
    # 道琼斯工业平均指數
    'DJI': ('^DJI', '道琼斯工业指數'),
    '^DJI': ('^DJI', '道琼斯工业指數'),
    'DJIA': ('^DJI', '道琼斯工业指數'),
    # 纳斯达克综合指數
    'IXIC': ('^IXIC', '纳斯达克综合指數'),
    '^IXIC': ('^IXIC', '纳斯达克综合指數'),
    'NASDAQ': ('^IXIC', '纳斯达克综合指數'),
    # 纳斯达克 100
    'NDX': ('^NDX', '纳斯达克100指數'),
    '^NDX': ('^NDX', '纳斯达克100指數'),
    # VIX 波动率指數
    'VIX': ('^VIX', 'VIX恐慌指數'),
    '^VIX': ('^VIX', 'VIX恐慌指數'),
    # 罗素 2000
    'RUT': ('^RUT', '罗素2000指數'),
    '^RUT': ('^RUT', '罗素2000指數'),
}


def is_us_index_code(code: str) -> bool:
    """
    判断代碼是否为美股指數符号。

    Args:
        code: 股票/指數代碼，如 'SPX', 'DJI'

    Returns:
        True 表示是已知美股指數符号，否则 False

    Examples:
        >>> is_us_index_code('SPX')
        True
        >>> is_us_index_code('AAPL')
        False
    """
    return (code or '').strip().upper() in US_INDEX_MAPPING


def is_us_stock_code(code: str) -> bool:
    """
    判断代碼是否为美股股票符号（排除美股指數）。

    美股股票代碼为 1-5 个大写字母，可選 .X 后缀如 BRK.B。
    美股指數（SPX、DJI 等）明确排除。

    Args:
        code: 股票代碼，如 'AAPL', 'TSLA', 'BRK.B'

    Returns:
        True 表示是美股股票符号，否则 False

    Examples:
        >>> is_us_stock_code('AAPL')
        True
        >>> is_us_stock_code('TSLA')
        True
        >>> is_us_stock_code('BRK.B')
        True
        >>> is_us_stock_code('SPX')
        False
        >>> is_us_stock_code('600519')
        False
    """
    normalized = (code or '').strip().upper()
    # 美股指數不是股票
    if normalized in US_INDEX_MAPPING:
        return False
    return bool(_US_STOCK_PATTERN.match(normalized))


def get_us_index_yf_symbol(code: str) -> tuple:
    """
    获取美股指數的 Yahoo Finance 符号与中文名称。

    Args:
        code: 使用者输入，如 'SPX', '^GSPC', 'DJI'

    Returns:
        (yf_symbol, chinese_name) 元组，未找到时傳回 (None, None)。

    Examples:
        >>> get_us_index_yf_symbol('SPX')
        ('^GSPC', '标普500指數')
        >>> get_us_index_yf_symbol('AAPL')
        (None, None)
    """
    normalized = (code or '').strip().upper()
    return US_INDEX_MAPPING.get(normalized, (None, None))
