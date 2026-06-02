# -*- coding: utf-8 -*-
"""
===================================
实时行情统一类型定义 & 熔断机制
===================================

设计目标：
1. 统一各數據源的实时行情傳回结构
2. 实现熔断/冷却机制，避免连续失败时反复請求
3. 支援多數據源故障切换

使用方式：
- 所有 Fetcher 的 get_realtime_quote() 统一傳回 UnifiedRealtimeQuote
- CircuitBreaker 管理各數據源的熔断狀態
"""

import logging
import time
from threading import RLock
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Union
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================
# 通用类型转换工具函數
# ============================================
# 设计说明：
# 各數據源傳回的原始數據类型不一致（str/float/int/NaN），
# 使用这些函數统一转换，避免在各 Fetcher 中重复定义。

def safe_float(val: Any, default: Optional[float] = None) -> Optional[float]:
    """
    安全转换为浮点数
    
    處理场景：
    - None / 空字符串 → default
    - pandas NaN / numpy NaN → default
    - 数值字符串 → float
    - 已是数值 → float
    
    Args:
        val: 待转换的值
        default: 转换失败时的默认值
        
    Returns:
        转换后的浮点数，或默认值
    """
    try:
        if val is None:
            return default
        
        # 處理字符串
        if isinstance(val, str):
            val = val.strip()
            if val == "" or val == "-" or val == "--":
                return default
        
        # 處理 pandas/numpy NaN
        # 使用 math.isnan 而不是 pd.isna，避免强制依賴 pandas
        import math
        try:
            if math.isnan(float(val)):
                return default
        except (ValueError, TypeError):
            pass
        
        return float(val)
    except (ValueError, TypeError):
        return default


def safe_int(val: Any, default: Optional[int] = None) -> Optional[int]:
    """
    安全转换为整数
    
    先转换为 float，再取整，處理 "123.0" 这类情况
    
    Args:
        val: 待转换的值
        default: 转换失败时的默认值
        
    Returns:
        转换后的整数，或默认值
    """
    f_val = safe_float(val, default=None)
    if f_val is not None:
        return int(f_val)
    return default


class RealtimeSource(Enum):
    """实时行情數據源"""
    EFINANCE = "efinance"           # 东方财富（efinance库）
    AKSHARE_EM = "akshare_em"       # 东方财富（akshare库）
    AKSHARE_SINA = "akshare_sina"   # 新浪财经
    AKSHARE_QQ = "akshare_qq"       # 腾讯财经
    TUSHARE = "tushare"             # Tushare Pro
    TENCENT = "tencent"             # 腾讯直连
    SINA = "sina"                   # 新浪直连
    STOOQ = "stooq"                 # Stooq 美股兜底
    LONGBRIDGE = "longbridge"       # 长桥（美股/港股兜底）
    FALLBACK = "fallback"           # 降级兜底


@dataclass
class UnifiedRealtimeQuote:
    """
    统一实时行情數據结构
    
    设计原则：
    - 各數據源傳回的欄位可能不同，缺失欄位用 None 表示
    - 主流程使用 getattr(quote, field, None) 获取，保证兼容性
    - source 欄位标记數據来源，便于调试
    """
    code: str
    name: str = ""
    source: RealtimeSource = RealtimeSource.FALLBACK
    
    # === 核心价格數據（几乎所有源都有）===
    price: Optional[float] = None           # 最新价
    change_pct: Optional[float] = None      # 漲跌幅(%)
    change_amount: Optional[float] = None   # 漲跌额
    
    # === 量价指标（部分源可能缺失）===
    volume: Optional[int] = None            # 成交量（手）
    amount: Optional[float] = None          # 成交额（元）
    volume_ratio: Optional[float] = None    # 量比
    turnover_rate: Optional[float] = None   # 换手率(%)
    amplitude: Optional[float] = None       # 振幅(%)
    
    # === 价格区间 ===
    open_price: Optional[float] = None      # 開盤价
    high: Optional[float] = None            # 最高价
    low: Optional[float] = None             # 最低价
    pre_close: Optional[float] = None       # 昨收价
    
    # === 估值指标（仅东财等全量接口有）===
    pe_ratio: Optional[float] = None        # 市盈率(动态)
    pb_ratio: Optional[float] = None        # 市净率
    total_mv: Optional[float] = None        # 总市值(元)
    circ_mv: Optional[float] = None         # 流通市值(元)
    
    # === 其他指标 ===
    change_60d: Optional[float] = None      # 60日漲跌幅(%)
    high_52w: Optional[float] = None        # 52周最高
    low_52w: Optional[float] = None         # 52周最低
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典（过滤 None 值）"""
        result = {
            'code': self.code,
            'name': self.name,
            'source': self.source.value,
        }
        # 只添加非 None 的欄位
        optional_fields = [
            'price', 'change_pct', 'change_amount', 'volume', 'amount',
            'volume_ratio', 'turnover_rate', 'amplitude',
            'open_price', 'high', 'low', 'pre_close',
            'pe_ratio', 'pb_ratio', 'total_mv', 'circ_mv',
            'change_60d', 'high_52w', 'low_52w'
        ]
        for f in optional_fields:
            val = getattr(self, f, None)
            if val is not None:
                result[f] = val
        return result
    
    def has_basic_data(self) -> bool:
        """检查是否有基本的价格數據"""
        return self.price is not None and self.price > 0
    
    def has_volume_data(self) -> bool:
        """检查是否有量价數據"""
        return self.volume_ratio is not None or self.turnover_rate is not None


@dataclass
class ChipDistribution:
    """
    筹码分布數據
    
    反映持倉成本分布和获利情况
    """
    code: str
    date: str = ""
    source: str = "akshare"
    
    # 获利情况
    profit_ratio: float = 0.0     # 获利比例(0-1)
    avg_cost: float = 0.0         # 平均成本
    
    # 筹码集中度
    cost_90_low: float = 0.0      # 90%筹码成本下限
    cost_90_high: float = 0.0     # 90%筹码成本上限
    concentration_90: float = 0.0  # 90%筹码集中度（越小越集中）
    
    cost_70_low: float = 0.0      # 70%筹码成本下限
    cost_70_high: float = 0.0     # 70%筹码成本上限
    concentration_70: float = 0.0  # 70%筹码集中度
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'code': self.code,
            'date': self.date,
            'source': self.source,
            'profit_ratio': self.profit_ratio,
            'avg_cost': self.avg_cost,
            'cost_90_low': self.cost_90_low,
            'cost_90_high': self.cost_90_high,
            'concentration_90': self.concentration_90,
            'concentration_70': self.concentration_70,
        }
    
    def get_chip_status(self, current_price: float) -> str:
        """
        获取筹码狀態描述
        
        Args:
            current_price: 当前股價
            
        Returns:
            筹码狀態描述
        """
        status_parts = []
        
        # 获利比例分析
        if self.profit_ratio >= 0.9:
            status_parts.append("获利盘极高(获利盘>90%)")
        elif self.profit_ratio >= 0.7:
            status_parts.append("获利盘较高(获利盘70-90%)")
        elif self.profit_ratio >= 0.5:
            status_parts.append("获利盘中等(获利盘50-70%)")
        elif self.profit_ratio >= 0.3:
            status_parts.append("套牢盘中等(套牢盘50-70%)")
        elif self.profit_ratio >= 0.1:
            status_parts.append("套牢盘较高(套牢盘70-90%)")
        else:
            status_parts.append("套牢盘极高(套牢盘>90%)")
        
        # 筹码集中度分析 (90%集中度 < 10% 表示集中)
        if self.concentration_90 < 0.08:
            status_parts.append("筹码高度集中")
        elif self.concentration_90 < 0.15:
            status_parts.append("筹码较集中")
        elif self.concentration_90 < 0.25:
            status_parts.append("筹码分散度中等")
        else:
            status_parts.append("筹码较分散")
        
        # 成本与现价关系
        if current_price > 0 and self.avg_cost > 0:
            cost_diff = (current_price - self.avg_cost) / self.avg_cost * 100
            if cost_diff > 20:
                status_parts.append(f"现价高于平均成本{cost_diff:.1f}%")
            elif cost_diff > 5:
                status_parts.append(f"现价略高于成本{cost_diff:.1f}%")
            elif cost_diff > -5:
                status_parts.append("现价接近平均成本")
            else:
                status_parts.append(f"现价低于平均成本{abs(cost_diff):.1f}%")
        
        return "，".join(status_parts)


class CircuitBreaker:
    """
    熔断器 - 管理數據源的熔断/冷却狀態
    
    策略：
    - 连续失败 N 次后进入熔断狀態
    - 熔断期间略過该數據源
    - 冷却时间后自动恢復半开狀態
    - 半开狀態下单次成功则完全恢復，失败则繼續熔断
    
    狀態机：
    CLOSED（正常） --失败N次--> OPEN（熔断）--冷却时间到--> HALF_OPEN（半开）
    HALF_OPEN --成功--> CLOSED
    HALF_OPEN --失败--> OPEN
    """
    
    # 狀態常量
    CLOSED = "closed"      # 正常狀態
    OPEN = "open"          # 熔断狀態（不可用）
    HALF_OPEN = "half_open"  # 半开狀態（试探性請求）
    
    def __init__(
        self,
        failure_threshold: int = 3,       # 连续失败次数阈值
        cooldown_seconds: float = 300.0,  # 冷却时间（秒），默认5分钟
        half_open_max_calls: int = 1      # 半开狀態最大尝试次数
    ):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self.half_open_max_calls = half_open_max_calls
        
        # 各數據源狀態 {source_name: {state, failures, last_failure_time, half_open_calls}}
        self._states: Dict[str, Dict[str, Any]] = {}
        self._lock = RLock()
    
    def _get_state_locked(self, source: str) -> Dict[str, Any]:
        """获取或初始化數據源狀態（调用方需持有锁）。"""
        if source not in self._states:
            self._states[source] = {
                'state': self.CLOSED,
                'failures': 0,
                'last_failure_time': 0.0,
                'half_open_calls': 0
            }
        return self._states[source]
    
    def is_available(self, source: str) -> bool:
        """
        检查數據源是否可用
        
        傳回 True 表示可以尝试請求
        傳回 False 表示应略過该數據源
        """
        with self._lock:
            state = self._get_state_locked(source)
            current_time = time.time()

            if state['state'] == self.CLOSED:
                return True

            if state['state'] == self.OPEN:
                # 检查冷却时间
                time_since_failure = current_time - state['last_failure_time']
                if time_since_failure >= self.cooldown_seconds:
                    # 冷却完成，进入半开狀態（不预占名额，由 HALF_OPEN 分支统一管理）
                    state['state'] = self.HALF_OPEN
                    state['half_open_calls'] = 0
                    state['last_failure_time'] = current_time
                    logger.info(f"[熔断器] {source} 冷却完成，进入半开狀態")
                    # Fall through to HALF_OPEN check below
                else:
                    remaining = self.cooldown_seconds - time_since_failure
                    logger.debug(f"[熔断器] {source} 处于熔断狀態，剩余冷却时间: {remaining:.0f}s")
                    return False

            if state['state'] == self.HALF_OPEN:
                if state['half_open_calls'] < self.half_open_max_calls:
                    state['half_open_calls'] += 1
                    return True
                # 所有探测名额已用完；若冷却时间再次到期仍未收到
                # record_success/record_failure 回调，重置名额允许重新探测，
                # 避免永久卡在 HALF_OPEN。
                time_since_failure = current_time - state['last_failure_time']
                if time_since_failure >= self.cooldown_seconds:
                    state['half_open_calls'] = 1
                    state['last_failure_time'] = current_time
                    logger.info(f"[熔断器] {source} 半开狀態探测逾時，重新探测")
                    return True
                return False

            return True
    
    def record_inconclusive(self, source: str) -> None:
        """记录不確定的探测结果（如傳回 None）。

        仅影响 HALF_OPEN 狀態：将其转回 OPEN 以便冷却后重新探测。
        CLOSED 狀態下为空操作，不影响失败计数。
        """
        with self._lock:
            state = self._get_state_locked(source)
            if state['state'] == self.HALF_OPEN:
                state['state'] = self.OPEN
                state['half_open_calls'] = 0
                state['last_failure_time'] = time.time()
                logger.info(f"[熔断器] {source} 半开探测结果不確定，重新进入冷却")

    def record_success(self, source: str) -> None:
        """记录成功請求"""
        with self._lock:
            state = self._get_state_locked(source)

            if state['state'] == self.HALF_OPEN:
                # 半开狀態下成功，完全恢復
                logger.info(f"[熔断器] {source} 半开狀態請求成功，恢復正常")

            # 重置狀態
            state['state'] = self.CLOSED
            state['failures'] = 0
            state['half_open_calls'] = 0
    
    def record_failure(self, source: str, error: Optional[str] = None) -> None:
        """记录失败請求"""
        with self._lock:
            state = self._get_state_locked(source)
            current_time = time.time()

            state['failures'] += 1
            state['last_failure_time'] = current_time

            if state['state'] == self.HALF_OPEN:
                # 半开狀態下失败，繼續熔断
                state['state'] = self.OPEN
                state['half_open_calls'] = 0
                logger.warning(f"[熔断器] {source} 半开狀態請求失败，繼續熔断 {self.cooldown_seconds}s")
            elif state['failures'] >= self.failure_threshold:
                # 达到阈值，进入熔断
                state['state'] = self.OPEN
                logger.warning(f"[熔断器] {source} 连续失败 {state['failures']} 次，进入熔断狀態 "
                              f"(冷却 {self.cooldown_seconds}s)")
                if error:
                    logger.warning(f"[熔断器] 最后錯誤: {error}")
    
    def get_status(self) -> Dict[str, str]:
        """获取所有數據源狀態"""
        with self._lock:
            return {source: info['state'] for source, info in self._states.items()}
    
    def reset(self, source: Optional[str] = None) -> None:
        """重置熔断器狀態"""
        with self._lock:
            if source:
                if source in self._states:
                    del self._states[source]
            else:
                self._states.clear()


# 全局熔断器实例（实时行情专用）
_realtime_circuit_breaker = CircuitBreaker(
    failure_threshold=3,      # 连续失败3次熔断
    cooldown_seconds=300.0,   # 冷却5分钟
    half_open_max_calls=1
)

# 筹码接口熔断器（更保守的策略，因为该接口更不稳定）
_chip_circuit_breaker = CircuitBreaker(
    failure_threshold=2,      # 连续失败2次熔断
    cooldown_seconds=600.0,   # 冷却10分钟
    half_open_max_calls=1
)


def get_realtime_circuit_breaker() -> CircuitBreaker:
    """获取实时行情熔断器"""
    return _realtime_circuit_breaker


def get_chip_circuit_breaker() -> CircuitBreaker:
    """获取筹码接口熔断器"""
    return _chip_circuit_breaker
