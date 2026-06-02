#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test generate_index_from_csv.py
"""

import csv
import json
import pytest
from pathlib import Path
from typing import Dict, List

# Add scripts directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from generate_index_from_csv import (
    extract_symbol_from_ts_code,
    get_stock_name,
    get_us_delist_priority,
    parse_stock_row,
    determine_market,
    generate_aliases,
    normalize_name_for_pinyin,
    generate_pinyin,
    compress_index,
    build_stock_index,
    load_tushare_data,
    load_akshare_data,
)


class TestExtractSymbol:
    """測試 Symbol 提取函數"""

    def test_a_stock_sz(self):
        """測試 A股深圳"""
        result = extract_symbol_from_ts_code("000001.SZ", "CN")
        assert result == "000001"

    def test_a_stock_sh(self):
        """測試 A股上海"""
        result = extract_symbol_from_ts_code("600519.SH", "CN")
        assert result == "600519"

    def test_hk_stock(self):
        """測試港股"""
        result = extract_symbol_from_ts_code("00700.HK", "HK")
        assert result == "00700"

    def test_us_stock(self):
        """測試美股"""
        result = extract_symbol_from_ts_code("AAPL", "US")
        assert result == "AAPL"

    def test_empty_ts_code(self):
        """測試空 ts_code"""
        result = extract_symbol_from_ts_code("", "CN")
        assert result is None

    def test_none_ts_code(self):
        """測試 None ts_code"""
        result = extract_symbol_from_ts_code(None, "CN")
        assert result is None


class TestDetermineMarket:
    """測試市场判断函數"""

    def test_a_stock_sz(self):
        """測試 A股深圳"""
        result = determine_market("000001.SZ")
        assert result == "CN"

    def test_a_stock_sh(self):
        """測試 A股上海"""
        result = determine_market("600519.SH")
        assert result == "CN"

    def test_hk_stock(self):
        """測試港股"""
        result = determine_market("00700.HK")
        assert result == "HK"

    def test_bse_stock(self):
        """測試北交所"""
        result = determine_market("832566.BJ")
        assert result == "BSE"

    def test_us_stock(self):
        """測試美股"""
        result = determine_market("AAPL")
        assert result == "US"

    def test_us_stock_tesla(self):
        """測試美股特斯拉"""
        result = determine_market("TSLA")
        assert result == "US"

    def test_us_stock_with_dot_suffix(self):
        """測試美股带点号后缀（BRK.B）"""
        result = determine_market("BRK.B")
        assert result == "US"

    def test_us_stock_class_a(self):
        """測試美股 A 类股（GOOG.A）"""
        result = determine_market("GOOG.A")
        assert result == "US"

    def test_us_stock_units(self):
        """測試美股 Unit（AAPL.U）"""
        result = determine_market("AAPL.U")
        assert result == "US"


class TestGetStockName:
    """測試股票名称获取函數"""

    def test_cn_stock_name(self):
        """測試 A股使用 name 欄位"""
        row = {'name': '平安银行', 'enname': 'Ping An Bank'}
        result = get_stock_name(row, 'CN')
        assert result == '平安银行'

    def test_hk_stock_name(self):
        """測試港股使用 name 欄位"""
        row = {'name': '腾讯控股', 'enname': 'Tencent'}
        result = get_stock_name(row, 'HK')
        assert result == '腾讯控股'

    def test_us_stock_name(self):
        """測試美股使用 enname 欄位"""
        row = {'name': '苹果', 'enname': 'Apple Inc.'}
        result = get_stock_name(row, 'US')
        assert result == 'Apple Inc.'

    def test_empty_name(self):
        """測試空名称"""
        row = {'name': '', 'enname': ''}
        result = get_stock_name(row, 'CN')
        assert result is None


class TestDataCleaning:
    """測試數據清洗逻辑"""

    def test_valid_cn_stock(self):
        """測試有效的 A股记录"""
        row = {
            'ts_code': '000001.SZ',
            'symbol': '000001',
            'name': '平安银行'
        }
        result = parse_stock_row(row, 'CN')
        assert result is not None
        assert result['ts_code'] == '000001.SZ'
        assert result['symbol'] == '000001'
        assert result['name'] == '平安银行'
        assert result['market'] == 'CN'

    def test_valid_hk_stock(self):
        """測試有效的港股记录"""
        row = {
            'ts_code': '00700.HK',
            'name': '腾讯控股',
            'enname': 'Tencent'
        }
        result = parse_stock_row(row, 'HK')
        assert result is not None
        assert result['ts_code'] == '00700.HK'
        assert result['symbol'] == '00700'
        assert result['name'] == '腾讯控股'
        assert result['market'] == 'HK'

    def test_valid_us_stock(self):
        """測試有效的美股记录"""
        row = {
            'ts_code': 'AAPL',
            'name': '苹果',
            'enname': 'Apple Inc.'
        }
        result = parse_stock_row(row, 'US')
        assert result is not None
        assert result['ts_code'] == 'AAPL'
        assert result['symbol'] == 'AAPL'
        assert result['name'] == 'Apple Inc.'
        assert result['market'] == 'US'

    def test_valid_us_stock_with_dot_suffix(self):
        """測試有效的美股记录（带点号后缀，如 BRK.B）"""
        row = {
            'ts_code': 'BRK.B',
            'name': '',
            'enname': "BERKSHIRE HATHAWAY 'B'"
        }
        result = parse_stock_row(row, None)
        assert result is not None
        assert result['ts_code'] == 'BRK.B'
        assert result['symbol'] == 'BRK.B'
        assert result['name'] == "BERKSHIRE HATHAWAY 'B'"
        assert result['market'] == 'US'

    def test_us_dummy_filtered(self):
        """測試美股 DUMMY 记录被过滤"""
        row = {
            'ts_code': 'DUMMY001',
            'name': '測試',
            'enname': 'DUMMY Test Stock'
        }
        result = parse_stock_row(row, 'US')
        assert result is None

    def test_us_dummy_case_insensitive(self):
        """測試 DUMMY 过滤不区分大小写"""
        row = {
            'ts_code': 'DUMMY002',
            'name': '測試',
            'enname': 'dummy test stock'
        }
        result = parse_stock_row(row, 'US')
        assert result is None

    def test_empty_ts_code(self):
        """測試空 ts_code 被过滤"""
        row = {
            'ts_code': '',
            'symbol': '000001',
            'name': '平安银行'
        }
        result = parse_stock_row(row, 'CN')
        assert result is None

    def test_empty_name(self):
        """測試空名称被过滤"""
        row = {
            'ts_code': '000001.SZ',
            'symbol': '000001',
            'name': ''
        }
        result = parse_stock_row(row, 'CN')
        assert result is None

    def test_us_empty_enname(self):
        """測試美股空 enname 被过滤"""
        row = {
            'ts_code': 'AAPL',
            'name': '苹果',
            'enname': ''
        }
        result = parse_stock_row(row, 'US')
        assert result is None

    def test_us_delist_priority_prefers_blank_over_nat(self):
        """測試美股去重优先级：空 delist_date 优先于 NaT"""
        assert get_us_delist_priority({'delist_date': ''}) == 2
        assert get_us_delist_priority({'delist_date': 'NaT'}) == 1
        assert get_us_delist_priority({'delist_date': '20250131'}) == 0


class TestAliases:
    """測試别名生成函數"""

    def test_cn_aliases(self):
        """測試 A股别名"""
        result = generate_aliases('贵州茅台', 'CN')
        assert '茅台' in result

    def test_hk_aliases(self):
        """測試港股别名"""
        result = generate_aliases('腾讯控股', 'HK')
        assert '腾讯' in result or 'Tencent' in result

    def test_us_aliases(self):
        """測試美股别名"""
        result = generate_aliases('Apple Inc.', 'US')
        assert 'Apple' in result or 'AAPL' in result

    def test_no_aliases(self):
        """測試无别名的情况"""
        result = generate_aliases('未知股票', 'CN')
        assert result == []


class TestOutputFormat:
    """測試输出格式"""

    def test_compress_index_field_order(self):
        """測試压缩格式的欄位顺序"""
        index = [{
            "canonicalCode": "000001.SZ",
            "displayCode": "000001",
            "nameZh": "平安银行",
            "pinyinFull": "pinganyinhang",
            "pinyinAbbr": "pyyh",
            "aliases": ["平银"],
            "market": "CN",
            "assetType": "stock",
            "active": True,
            "popularity": 100,
        }]

        compressed = compress_index(index)

        assert len(compressed) == 1
        item = compressed[0]

        # 验证欄位顺序
        assert item[0] == "000001.SZ"      # canonicalCode
        assert item[1] == "000001"         # displayCode
        assert item[2] == "平安银行"       # nameZh
        assert item[3] == "pinganyinhang"  # pinyinFull
        assert item[4] == "pyyh"           # pinyinAbbr
        assert item[5] == ["平银"]         # aliases
        assert item[6] == "CN"             # market
        assert item[7] == "stock"          # assetType
        assert item[8] == True             # active
        assert item[9] == 100              # popularity

    def test_compress_index_field_count(self):
        """測試压缩格式的欄位数量"""
        index = [{
            "canonicalCode": "AAPL",
            "displayCode": "AAPL",
            "nameZh": "Apple Inc.",
            "pinyinFull": None,
            "pinyinAbbr": None,
            "aliases": [],
            "market": "US",
            "assetType": "stock",
            "active": True,
            "popularity": 100,
        }]

        compressed = compress_index(index)
        assert len(compressed[0]) == 10  # 10个欄位

    def test_json_serialization(self):
        """測試 JSON 序列化"""
        index = [{
            "canonicalCode": "00700.HK",
            "displayCode": "00700",
            "nameZh": "腾讯控股",
            "pinyinFull": "xunxiongkonggu",
            "pinyinAbbr": "xxkg",
            "aliases": ["腾讯"],
            "market": "HK",
            "assetType": "stock",
            "active": True,
            "popularity": 100,
        }]

        compressed = compress_index(index)

        # 应该能成功序列化为 JSON
        json_str = json.dumps(compressed, ensure_ascii=False)
        assert json_str is not None

        # 应该能成功反序列化
        loaded = json.loads(json_str)
        assert len(loaded) == 1


class TestIntegration:
    """集成測試"""

    def test_full_workflow_tushare(self, tmp_path):
        """測試完整的 Tushare 工作流"""
        # 建立測試 CSV 文件
        a_csv = tmp_path / 'stock_list_a.csv'
        with open(a_csv, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['ts_code', 'symbol', 'name'])
            writer.writeheader()
            writer.writerow({
                'ts_code': '000001.SZ',
                'symbol': '000001',
                'name': '平安银行'
            })

        hk_csv = tmp_path / 'stock_list_hk.csv'
        with open(hk_csv, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['ts_code', 'name', 'enname'])
            writer.writeheader()
            writer.writerow({
                'ts_code': '00700.HK',
                'name': '腾讯控股',
                'enname': 'Tencent'
            })

        us_csv = tmp_path / 'stock_list_us.csv'
        with open(us_csv, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['ts_code', 'name', 'enname'])
            writer.writeheader()
            writer.writerow({
                'ts_code': 'AAPL',
                'name': '苹果',
                'enname': 'Apple Inc.'
            })

        # 加载數據
        stocks = load_tushare_data(tmp_path)

        # 验证數據
        assert len(stocks) == 3

        # 构建索引
        index = build_stock_index(stocks)

        # 验证索引
        assert len(index) == 3

        # 压缩索引
        compressed = compress_index(index)

        # 验证压缩
        assert len(compressed) == 3

        # 验证欄位数量
        for item in compressed:
            assert len(item) == 10

    def test_market_distribution(self, tmp_path):
        """測試市场分布统计"""
        # 建立測試數據
        csv_file = tmp_path / 'stock_list_a.csv'
        with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['ts_code', 'symbol', 'name'])
            writer.writeheader()
            writer.writerow({'ts_code': '000001.SZ', 'symbol': '000001', 'name': '平安银行'})
            writer.writerow({'ts_code': '600519.SH', 'symbol': '600519', 'name': '贵州茅台'})
            writer.writerow({'ts_code': '832566.BJ', 'symbol': '832566', 'name': '梓撞科技'})

        stocks = load_tushare_data(tmp_path)
        index = build_stock_index(stocks)

        # 统计市场分布
        market_stats = {}
        for item in index:
            market = item['market']
            market_stats[market] = market_stats.get(market, 0) + 1

        # 验证统计
        assert market_stats.get('CN', 0) == 2  # SZ, SH
        assert market_stats.get('BSE', 0) == 1  # BJ

    def test_us_reused_symbols_are_deduplicated(self, tmp_path):
        """測試美股复用 ticker 在加载时会先去重"""
        us_csv = tmp_path / 'stock_list_us.csv'
        with open(us_csv, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['ts_code', 'name', 'enname', 'list_date', 'delist_date']
            )
            writer.writeheader()
            writer.writerow({
                'ts_code': 'B',
                'name': '',
                'enname': 'BARNES GROUP',
                'list_date': '19631014',
                'delist_date': 'NaT',
            })
            writer.writerow({
                'ts_code': 'B',
                'name': '',
                'enname': 'BARRICK MINING (NYS)',
                'list_date': '19850213',
                'delist_date': '',
            })
            writer.writerow({
                'ts_code': 'DOC',
                'name': '',
                'enname': 'HEALTHPEAK PROPERTIES',
                'list_date': '19850523',
                'delist_date': '',
            })
            writer.writerow({
                'ts_code': 'DOC',
                'name': '',
                'enname': 'PHYSICIANS REALTY TST.',
                'list_date': '20130719',
                'delist_date': '',
            })
            writer.writerow({
                'ts_code': 'SPWR',
                'name': '',
                'enname': 'COMPLETE SOLARIA',
                'list_date': '20210419',
                'delist_date': '',
            })
            writer.writerow({
                'ts_code': 'SPWR',
                'name': '',
                'enname': 'SUNPOWER',
                'list_date': '20051109',
                'delist_date': 'NaT',
            })

        stocks = load_tushare_data(tmp_path)

        assert len(stocks) == 3
        assert {stock['ts_code'] for stock in stocks} == {'B', 'DOC', 'SPWR'}
        assert next(stock for stock in stocks if stock['ts_code'] == 'B')['name'] == 'BARRICK MINING (NYS)'
        assert next(stock for stock in stocks if stock['ts_code'] == 'DOC')['name'] == 'HEALTHPEAK PROPERTIES'
        assert next(stock for stock in stocks if stock['ts_code'] == 'SPWR')['name'] == 'COMPLETE SOLARIA'


class TestPinyin:
    """測試拼音生成"""

    def test_normalize_name(self):
        """測試名称标准化"""
        # 測試 ST 前缀去除
        result = normalize_name_for_pinyin('*ST平安')
        assert 'ST' not in result

        # 測試 N 前缀去除
        result = normalize_name_for_pinyin('N平安银行')
        assert 'N' not in result

    def test_generate_pinyin(self):
        """測試拼音生成"""
        # 注意：这个測試需要 pypinyin 可用
        pinyin_full, pinyin_abbr = generate_pinyin('平安银行')
        if pinyin_full:
            assert isinstance(pinyin_full, str)
        if pinyin_abbr:
            assert isinstance(pinyin_abbr, str)
