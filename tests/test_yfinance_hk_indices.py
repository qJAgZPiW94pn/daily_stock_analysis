# -*- coding: utf-8 -*-
"""
data_provider/yfinance_fetcher 中港股指數獲取邏輯的单元測試

使用 unittest.mock 模拟 yfinance API 回應，覆盖：
- _get_hk_main_indices 港股指數批量獲取
- 港股指數 Yahoo Finance 符号映射正确性
- 部分/全部失败的降級場景
"""
import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import pandas as pd

# 在匯入 data_provider 前 mock 可能缺失的依賴，避免環境差异导致測試無法執行
if 'fake_useragent' not in sys.modules:
    sys.modules['fake_useragent'] = MagicMock()

# 確保能匯入项目模組
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def _make_mock_hist(close: float, prev_close: float, high: float = None, low: float = None) -> pd.DataFrame:
    """构造模拟的 history DataFrame，包含计算漲跌幅所需欄位"""
    high = high if high is not None else close + 100
    low = low if low is not None else close - 100
    return pd.DataFrame({
        'Close': [prev_close, close],
        'Open': [prev_close - 50, close - 30],
        'High': [prev_close + 100, high],
        'Low': [prev_close - 100, low],
        'Volume': [5000000000.0, 5200000000.0],
    }, index=pd.DatetimeIndex(['2025-02-16', '2025-02-17']))


def _make_mock_yf(hist_df: pd.DataFrame):
    """构造模拟的 yf 模組，Ticker().history() 傳回给定 DataFrame"""
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = hist_df
    mock_yf = MagicMock()
    mock_yf.Ticker.return_value = mock_ticker
    return mock_yf


class TestHkIndexSymbolMapping(unittest.TestCase):
    """驗證港股指數 Yahoo Finance 符号映射的正确性"""

    def setUp(self):
        from data_provider.yfinance_fetcher import YfinanceFetcher
        self.fetcher = YfinanceFetcher()

    def test_hk_indices_mapping_symbols(self):
        """港股指數映射应使用正确的 Yahoo Finance 符号"""
        mock_yf = MagicMock()
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = pd.DataFrame()
        mock_yf.Ticker.return_value = mock_ticker

        self.fetcher._get_hk_main_indices(mock_yf)

        # 收集所有 Ticker() 呼叫的參數
        ticker_calls = [call.args[0] for call in mock_yf.Ticker.call_args_list]

        self.assertIn('^HSI', ticker_calls, '恒生指數应使用 ^HSI')
        self.assertIn('HSTECH.HK', ticker_calls, '恒生科技指數应使用 HSTECH.HK，而非 ^HSTECH')
        self.assertIn('^HSCE', ticker_calls, '国企指數应使用 ^HSCE，而非 ^HSCEI')

    def test_hk_indices_mapping_no_invalid_symbols(self):
        """確保不再使用已知錯誤的旧映射符号"""
        mock_yf = MagicMock()
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = pd.DataFrame()
        mock_yf.Ticker.return_value = mock_ticker

        self.fetcher._get_hk_main_indices(mock_yf)

        ticker_calls = [call.args[0] for call in mock_yf.Ticker.call_args_list]

        self.assertNotIn('^HSTECH', ticker_calls, '^HSTECH 不是有效的 Yahoo Finance 符号')
        self.assertNotIn('^HSCEI', ticker_calls, '^HSCEI 不是有效的 Yahoo Finance 符号')


class TestGetHkMainIndices(unittest.TestCase):
    """_get_hk_main_indices 港股指數批量獲取測試"""

    def setUp(self):
        from data_provider.yfinance_fetcher import YfinanceFetcher
        self.fetcher = YfinanceFetcher()

    def test_returns_list_when_all_succeed(self):
        """全部指數取数成功时傳回包含三个指數的列表"""
        mock_hist = _make_mock_hist(close=20000.0, prev_close=19800.0)
        mock_yf = _make_mock_yf(mock_hist)

        result = self.fetcher._get_hk_main_indices(mock_yf)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)

        codes = {item['code'] for item in result}
        self.assertEqual(codes, {'HSI', 'HSTECH', 'HSCEI'})

        for item in result:
            self.assertIn('code', item)
            self.assertIn('name', item)
            self.assertIn('current', item)
            self.assertIn('change_pct', item)
            self.assertIn('prev_close', item)
            self.assertIn('amplitude', item)

    def test_returns_correct_computed_values(self):
        """驗證漲跌幅和振幅的计算结果"""
        mock_hist = _make_mock_hist(
            close=20000.0, prev_close=19800.0, high=20200.0, low=19700.0
        )
        mock_yf = _make_mock_yf(mock_hist)

        result = self.fetcher._get_hk_main_indices(mock_yf)

        self.assertIsNotNone(result)
        item = result[0]
        self.assertEqual(item['current'], 20000.0)
        self.assertEqual(item['prev_close'], 19800.0)
        self.assertAlmostEqual(item['change'], 200.0)
        expected_pct = (200.0 / 19800.0) * 100
        self.assertAlmostEqual(item['change_pct'], expected_pct)
        expected_amplitude = ((20200.0 - 19700.0) / 19800.0) * 100
        self.assertAlmostEqual(item['amplitude'], expected_amplitude)

    def test_handles_partial_failure(self):
        """部分指數 history 为空时仍傳回能取到數據的指數"""
        call_count = [0]

        def history_side_effect(period):
            call_count[0] += 1
            if call_count[0] == 1:
                return _make_mock_hist(close=20000.0, prev_close=19800.0)
            return pd.DataFrame()

        mock_ticker = MagicMock()
        mock_ticker.history.side_effect = history_side_effect
        mock_yf = MagicMock()
        mock_yf.Ticker.return_value = mock_ticker

        result = self.fetcher._get_hk_main_indices(mock_yf)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_returns_none_when_all_fail(self):
        """全部取数失败时傳回 None"""
        mock_yf = _make_mock_yf(pd.DataFrame())

        result = self.fetcher._get_hk_main_indices(mock_yf)

        self.assertIsNone(result)

    def test_handles_ticker_exception(self):
        """Ticker.history 抛例外时略過该指數，不整体失败"""
        mock_ticker = MagicMock()
        mock_ticker.history.side_effect = Exception("Network error")
        mock_yf = MagicMock()
        mock_yf.Ticker.return_value = mock_ticker

        result = self.fetcher._get_hk_main_indices(mock_yf)

        self.assertIsNone(result)

    def test_return_codes_match_expected_keys(self):
        """傳回的 code 欄位应为 HSI/HSTECH/HSCEI，与 MarketAnalyzer prompt 一致"""
        mock_hist = _make_mock_hist(close=20000.0, prev_close=19800.0)
        mock_yf = _make_mock_yf(mock_hist)

        result = self.fetcher._get_hk_main_indices(mock_yf)

        self.assertIsNotNone(result)
        codes = [item['code'] for item in result]
        self.assertIn('HSI', codes)
        self.assertIn('HSTECH', codes)
        self.assertIn('HSCEI', codes)


class TestGetMainIndicesDispatch(unittest.TestCase):
    """get_main_indices region 分发測試"""

    def setUp(self):
        from data_provider.yfinance_fetcher import YfinanceFetcher
        self.fetcher = YfinanceFetcher()

    def test_region_hk_dispatches_to_hk_method(self):
        """region='hk' 应委托给 _get_hk_main_indices"""
        mock_yf = MagicMock()
        with patch.dict('sys.modules', {'yfinance': mock_yf}):
            with patch.object(self.fetcher, '_get_hk_main_indices', return_value=[{'code': 'HSI'}]) as mock_hk:
                result = self.fetcher.get_main_indices(region='hk')

                mock_hk.assert_called_once()
                self.assertEqual(result, [{'code': 'HSI'}])


if __name__ == '__main__':
    unittest.main()
