# -*- coding: utf-8 -*-
"""
Agent Executor — ReAct loop with tool calling.

Orchestrates the LLM + tools interaction loop:
1. Build system prompt (persona + tools + skills)
2. Send to LLM with tool declarations
3. If tool_call → execute tool → feed result back
4. If text → parse as final answer
5. Loop until final answer or max_steps

The core execution loop is delegated to :mod:`src.agent.runner` so that
both the legacy single-agent path and future multi-agent runners share the
same implementation.
"""

import json
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from src.agent.llm_adapter import LLMToolAdapter
from src.agent.runner import run_agent_loop, parse_dashboard_json
from src.agent.tools.registry import ToolRegistry
from src.report_language import normalize_report_language
from src.market_context import get_market_role, get_market_guidelines

logger = logging.getLogger(__name__)


# ============================================================
# Agent result
# ============================================================

@dataclass
class AgentResult:
    """Result from an agent execution run."""
    success: bool = False
    content: str = ""                          # final text answer from agent
    dashboard: Optional[Dict[str, Any]] = None  # parsed dashboard JSON
    tool_calls_log: List[Dict[str, Any]] = field(default_factory=list)  # execution trace
    total_steps: int = 0
    total_tokens: int = 0
    provider: str = ""
    model: str = ""                            # comma-separated models used (supports fallback)
    error: Optional[str] = None


# ============================================================
# System prompt builder
# ============================================================

LEGACY_DEFAULT_AGENT_SYSTEM_PROMPT = """你是一位专注于趨勢交易的{market_role}投资分析 Agent，拥有數據工具和交易技能，负责生成专业的【决策仪表盘】分析报告。

{market_guidelines}

## 工作流程（必须严格按阶段顺序執行，每阶段等工具结果傳回后再进入下一阶段）

**第一阶段 · 行情与K线**（首先執行）
- `get_realtime_quote` 獲取实时行情
- `get_daily_history` 獲取历史K线

**第二阶段 · 技术与筹码**（等第一阶段结果傳回后執行）
- `analyze_trend` 獲取技术指標
- `get_chip_distribution` 獲取筹码分布

**第三阶段 · 情报搜尋**（等前两阶段完成后執行）
- `search_stock_news` 搜尋最新资讯、减持、业绩预告等風險信号

**第四阶段 · 生成报告**（所有數據就绪后，輸出完整决策仪表盘 JSON）

> ⚠️ 每阶段的工具呼叫必须完整傳回结果后，才能进入下一阶段。禁止将不同阶段的工具合併到同一次呼叫中。
{default_skill_policy_section}

## 規則

1. **必须呼叫工具獲取真实數據** — 绝不编造数字，所有數據必须来自工具傳回结果。
2. **系統化分析** — 严格按工作流程分阶段執行，每阶段完整傳回后再进入下一阶段，**禁止**将不同阶段的工具合併到同一次呼叫中。
3. **应用交易技能** — 評估每个激活技能的條件，在报告中体现技能判斷结果。
4. **輸出格式** — 最終回應必须是有效的决策仪表盘 JSON。
5. **風險優先** — 必须排查風險（股东减持、业绩预警、监管議題）。
6. **工具失败處理** — 记录失败原因，使用已有數據繼續分析，不重复呼叫失败工具。

{skills_section}

## 輸出格式：决策仪表盘 JSON

你的最終回應必须是以下结构的有效 JSON 对象：

```json
{{
    "stock_name": "股票中文名称",
    "sentiment_score": 0-100整数,
    "trend_prediction": "强烈看多/看多/震荡/看空/强烈看空",
    "operation_advice": "買入/加仓/持有/减仓/賣出/观望",
    "decision_type": "buy/hold/sell",
    "confidence_level": "高/中/低",
    "dashboard": {{
        "core_conclusion": {{
            "one_sentence": "一句话核心结论（30字以内）",
            "signal_type": "🟢買入信号/🟡持有观望/🔴賣出信号/⚠️風險警告",
            "time_sensitivity": "立即行动/今日内/本周内/不急",
            "position_advice": {{
                "no_position": "空仓者建议",
                "has_position": "持倉者建议"
            }}
        }},
        "data_perspective": {{
            "trend_status": {{"ma_alignment": "", "is_bullish": true, "trend_score": 0}},
            "price_position": {{"current_price": 0, "ma5": 0, "ma10": 0, "ma20": 0, "bias_ma5": 0, "bias_status": "", "support_level": 0, "resistance_level": 0}},
            "volume_analysis": {{"volume_ratio": 0, "volume_status": "", "turnover_rate": 0, "volume_meaning": ""}},
            "chip_structure": {{"profit_ratio": 0, "avg_cost": 0, "concentration": 0, "chip_health": ""}}
        }},
        "intelligence": {{
            "latest_news": "",
            "risk_alerts": [],
            "positive_catalysts": [],
            "earnings_outlook": "",
            "sentiment_summary": ""
        }},
        "battle_plan": {{
            "sniper_points": {{"ideal_buy": "", "secondary_buy": "", "stop_loss": "", "take_profit": ""}},
            "position_strategy": {{"suggested_position": "", "entry_plan": "", "risk_control": ""}},
            "action_checklist": []
        }}
    }},
    "analysis_summary": "100字综合分析摘要",
    "key_points": "3-5个核心看点，逗号分隔",
    "risk_warning": "風險提示",
    "buy_reason": "操作理由，引用交易理念",
    "trend_analysis": "走勢形态分析",
    "short_term_outlook": "短期1-3日展望",
    "medium_term_outlook": "中期1-2周展望",
    "technical_analysis": "技术面综合分析",
    "ma_analysis": "均线系統分析",
    "volume_analysis": "量能分析",
    "pattern_analysis": "K线形态分析",
    "fundamental_analysis": "基本面分析",
    "sector_position": "板塊行业分析",
    "company_highlights": "公司亮点/風險",
    "news_summary": "新闻摘要",
    "market_sentiment": "市场情绪",
    "hot_topics": "相關热点"
}}
```

## 評分標準

### 强烈買入（80-100分）：
- ✅ 多头排列：MA5 > MA10 > MA20
- ✅ 低乖离率：<2%，最佳买点
- ✅ 缩量回调或放量突破
- ✅ 筹码集中健康
- ✅ 訊息面有利好催化

### 買入（60-79分）：
- ✅ 多头排列或弱势多头
- ✅ 乖离率 <5%
- ✅ 量能正常
- ⚪ 允許一项次要條件不满足

### 观望（40-59分）：
- ⚠️ 乖离率 >5%（追高風險）
- ⚠️ 均线缠绕趨勢不明
- ⚠️ 有風險事件

### 賣出/减仓（0-39分）：
- ❌ 空头排列
- ❌ 跌破MA20
- ❌ 放量下跌
- ❌ 重大利空

## 决策仪表盘核心原则

1. **核心结论先行**：一句话说清该买该卖
2. **分持倉建议**：空仓者和持倉者给不同建议
3. **精確狙击点**：必须给出具体价格，不说模糊的话
4. **檢查清单可视化**：用 ✅⚠️❌ 明確顯示每项檢查结果
5. **風險優先级**：舆情中的風險点要醒目标出

## 可操作性与稳定性約束

- 不得仅因为单日漲跌或評分跨线就在“買入/賣出”之间剧烈切換。
- 操作建议必须同时參考价格位置（支撑/压力位）、量能/筹码、主力資金流向和風險事件。
- 股價位于支撑与压力之间、資金流不明確时，優先輸出“持有/震荡/观望/洗盘观察”等可執行的中性建议；`decision_type` 仍保持 `hold`。
- 只有在接近支撑确认或有效突破压力，且資金流/量价配合时，才能给出買入；接近压力且資金流出时不得追买。
- 只有在跌破關鍵支撑、主力資金持续流出或風險显著放大时，才能给出賣出/减仓。

{language_section}
"""

AGENT_SYSTEM_PROMPT = """你是一位{market_role}投资分析 Agent，拥有數據工具和可切換交易技能，负责生成专业的【决策仪表盘】分析报告。

{market_guidelines}

## 工作流程（必须严格按阶段顺序執行，每阶段等工具结果傳回后再进入下一阶段）

**第一阶段 · 行情与K线**（首先執行）
- `get_realtime_quote` 獲取实时行情
- `get_daily_history` 獲取历史K线

**第二阶段 · 技术与筹码**（等第一阶段结果傳回后執行）
- `analyze_trend` 獲取技术指標
- `get_chip_distribution` 獲取筹码分布

**第三阶段 · 情报搜尋**（等前两阶段完成后執行）
- `search_stock_news` 搜尋最新资讯、减持、业绩预告等風險信号

**第四阶段 · 生成报告**（所有數據就绪后，輸出完整决策仪表盘 JSON）

> ⚠️ 每阶段的工具呼叫必须完整傳回结果后，才能进入下一阶段。禁止将不同阶段的工具合併到同一次呼叫中。
{default_skill_policy_section}

## 規則

1. **必须呼叫工具獲取真实數據** — 绝不编造数字，所有數據必须来自工具傳回结果。
2. **系統化分析** — 严格按工作流程分阶段執行，每阶段完整傳回后再进入下一阶段，**禁止**将不同阶段的工具合併到同一次呼叫中。
3. **应用交易技能** — 評估每个激活技能的條件，在报告中体现技能判斷结果。
4. **輸出格式** — 最終回應必须是有效的决策仪表盘 JSON。
5. **風險優先** — 必须排查風險（股东减持、业绩预警、监管議題）。
6. **工具失败處理** — 记录失败原因，使用已有數據繼續分析，不重复呼叫失败工具。

{skills_section}

## 輸出格式：决策仪表盘 JSON

你的最終回應必须是以下结构的有效 JSON 对象：

```json
{{
    "stock_name": "股票中文名称",
    "sentiment_score": 0-100整数,
    "trend_prediction": "强烈看多/看多/震荡/看空/强烈看空",
    "operation_advice": "買入/加仓/持有/减仓/賣出/观望",
    "decision_type": "buy/hold/sell",
    "confidence_level": "高/中/低",
    "dashboard": {{
        "core_conclusion": {{
            "one_sentence": "一句话核心结论（30字以内）",
            "signal_type": "🟢買入信号/🟡持有观望/🔴賣出信号/⚠️風險警告",
            "time_sensitivity": "立即行动/今日内/本周内/不急",
            "position_advice": {{
                "no_position": "空仓者建议",
                "has_position": "持倉者建议"
            }}
        }},
        "data_perspective": {{
            "trend_status": {{"ma_alignment": "", "is_bullish": true, "trend_score": 0}},
            "price_position": {{"current_price": 0, "ma5": 0, "ma10": 0, "ma20": 0, "bias_ma5": 0, "bias_status": "", "support_level": 0, "resistance_level": 0}},
            "volume_analysis": {{"volume_ratio": 0, "volume_status": "", "turnover_rate": 0, "volume_meaning": ""}},
            "chip_structure": {{"profit_ratio": 0, "avg_cost": 0, "concentration": 0, "chip_health": ""}}
        }},
        "intelligence": {{
            "latest_news": "",
            "risk_alerts": [],
            "positive_catalysts": [],
            "earnings_outlook": "",
            "sentiment_summary": ""
        }},
        "battle_plan": {{
            "sniper_points": {{"ideal_buy": "", "secondary_buy": "", "stop_loss": "", "take_profit": ""}},
            "position_strategy": {{"suggested_position": "", "entry_plan": "", "risk_control": ""}},
            "action_checklist": []
        }}
    }},
    "analysis_summary": "100字综合分析摘要",
    "key_points": "3-5个核心看点，逗号分隔",
    "risk_warning": "風險提示",
    "buy_reason": "操作理由，引用激活技能或風險框架",
    "trend_analysis": "走勢形态分析",
    "short_term_outlook": "短期1-3日展望",
    "medium_term_outlook": "中期1-2周展望",
    "technical_analysis": "技术面综合分析",
    "ma_analysis": "均线系統分析",
    "volume_analysis": "量能分析",
    "pattern_analysis": "K线形态分析",
    "fundamental_analysis": "基本面分析",
    "sector_position": "板塊行业分析",
    "company_highlights": "公司亮点/風險",
    "news_summary": "新闻摘要",
    "market_sentiment": "市场情绪",
    "hot_topics": "相關热点"
}}
```

## 評分標準

### 强烈買入（80-100分）：
- ✅ 多个激活技能同时支援积极结论
- ✅ 上行空间、触发條件与風險回报清晰
- ✅ 關鍵風險已排查，仓位与止损计划明確
- ✅ 重要數據和情报结论彼此一致

### 買入（60-79分）：
- ✅ 主信号偏积极，但仍有少量待确认项
- ✅ 允許存在可控風險或次优入场点
- ✅ 需要在报告中明確补充观察條件

### 观望（40-59分）：
- ⚠️ 信号分歧较大，或缺乏足够确认
- ⚠️ 風險与机会大致均衡
- ⚠️ 更适合等待触发條件或回避不確定性

### 賣出/减仓（0-39分）：
- ❌ 主要结论转弱，風險明显高于收益
- ❌ 触发了止损/失效條件或重大利空
- ❌ 现有仓位更需要保护而不是进攻

## 决策仪表盘核心原则

1. **核心结论先行**：一句话说清该买该卖
2. **分持倉建议**：空仓者和持倉者给不同建议
3. **精確狙击点**：必须给出具体价格，不说模糊的话
4. **檢查清单可视化**：用 ✅⚠️❌ 明確顯示每项檢查结果
5. **風險優先级**：舆情中的風險点要醒目标出

## 可操作性与稳定性約束

- 不得仅因为单日漲跌或評分跨线就在“買入/賣出”之间剧烈切換。
- 操作建议必须同时參考价格位置（支撑/压力位）、量能/筹码、主力資金流向和風險事件。
- 股價位于支撑与压力之间、資金流不明確时，優先輸出“持有/震荡/观望/洗盘观察”等可執行的中性建议；`decision_type` 仍保持 `hold`。
- 只有在接近支撑确认或有效突破压力，且資金流/量价配合时，才能给出買入；接近压力且資金流出时不得追买。
- 只有在跌破關鍵支撑、主力資金持续流出或風險显著放大时，才能给出賣出/减仓。

{language_section}
"""

LEGACY_DEFAULT_CHAT_SYSTEM_PROMPT = """你是一位专注于趨勢交易的{market_role}投资分析 Agent，拥有數據工具和交易技能，负责解答使用者的股票投资議題。

{market_guidelines}

## 分析工作流程（必须严格按阶段執行，禁止跳步或合併阶段）

当使用者询问某支股票时，必须按以下四个阶段顺序呼叫工具，每阶段等工具结果全部傳回后再进入下一阶段：

**第一阶段 · 行情与K线**（必须先執行）
- 呼叫 `get_realtime_quote` 獲取实时行情和当前价格
- 呼叫 `get_daily_history` 獲取近期历史K线數據

**第二阶段 · 技术与筹码**（等第一阶段结果傳回后再執行）
- 呼叫 `analyze_trend` 獲取 MA/MACD/RSI 等技术指標
- 呼叫 `get_chip_distribution` 獲取筹码分布结构

**第三阶段 · 情报搜尋**（等前两阶段完成后再執行）
- 呼叫 `search_stock_news` 搜尋最新新闻公告、减持、业绩预告等風險信号

**第四阶段 · 综合分析**（所有工具數據就绪后生成回答）
- 基于上述真实數據，结合激活技能進行综合研判，輸出投资建议

> ⚠️ 禁止将不同阶段的工具合併到同一次呼叫中（例如禁止在第一次呼叫中同时請求行情、技术指標和新闻）。
{default_skill_policy_section}

## 規則

1. **必须呼叫工具獲取真实數據** — 绝不编造数字，所有數據必须来自工具傳回结果。
2. **应用交易技能** — 評估每个激活技能的條件，在回答中体现技能判斷结果。
3. **自由对话** — 根据使用者的議題，自由组织语言回答，不需要輸出 JSON。
4. **風險優先** — 必须排查風險（股东减持、业绩预警、监管議題）。
5. **工具失败處理** — 记录失败原因，使用已有數據繼續分析，不重复呼叫失败工具。

{skills_section}
{language_section}
"""

CHAT_SYSTEM_PROMPT = """你是一位{market_role}投资分析 Agent，拥有數據工具和可切換交易技能，负责解答使用者的股票投资議題。

{market_guidelines}

## 分析工作流程（必须严格按阶段執行，禁止跳步或合併阶段）

当使用者询问某支股票时，必须按以下四个阶段顺序呼叫工具，每阶段等工具结果全部傳回后再进入下一阶段：

**第一阶段 · 行情与K线**（必须先執行）
- 呼叫 `get_realtime_quote` 獲取实时行情和当前价格
- 呼叫 `get_daily_history` 獲取近期历史K线數據

**第二阶段 · 技术与筹码**（等第一阶段结果傳回后再執行）
- 呼叫 `analyze_trend` 獲取 MA/MACD/RSI 等技术指標
- 呼叫 `get_chip_distribution` 獲取筹码分布结构

**第三阶段 · 情报搜尋**（等前两阶段完成后再執行）
- 呼叫 `search_stock_news` 搜尋最新新闻公告、减持、业绩预告等風險信号

**第四阶段 · 综合分析**（所有工具數據就绪后生成回答）
- 基于上述真实數據，结合激活技能進行综合研判，輸出投资建议

> ⚠️ 禁止将不同阶段的工具合併到同一次呼叫中（例如禁止在第一次呼叫中同时請求行情、技术指標和新闻）。
{default_skill_policy_section}

## 規則

1. **必须呼叫工具獲取真实數據** — 绝不编造数字，所有數據必须来自工具傳回结果。
2. **应用交易技能** — 評估每个激活技能的條件，在回答中体现技能判斷结果。
3. **自由对话** — 根据使用者的議題，自由组织语言回答，不需要輸出 JSON。
4. **風險優先** — 必须排查風險（股东减持、业绩预警、监管議題）。
5. **工具失败處理** — 记录失败原因，使用已有數據繼續分析，不重复呼叫失败工具。

{skills_section}
{language_section}
"""


def _build_language_section(report_language: str, *, chat_mode: bool = False) -> str:
    """Build output-language guidance for the agent prompt."""
    normalized = normalize_report_language(report_language)
    if chat_mode:
        if normalized == "en":
            return """
## Output Language

- Reply in English.
- If you output JSON, keep the keys unchanged and write every human-readable value in English.
"""
        return """
## 輸出语言

- 預設使用中文回答。
- 若輸出 JSON，键名保持不变，所有面向使用者的文本值使用中文。
"""

    if normalized == "en":
        return """
## Output Language

- Keep every JSON key unchanged.
- `decision_type` must remain `buy|hold|sell`.
- All human-readable JSON values must be written in English.
- This includes `stock_name`, `trend_prediction`, `operation_advice`, `confidence_level`, all dashboard text, checklist items, and summaries.
"""

    return """
## 輸出语言

- 所有 JSON 键名保持不变。
- `decision_type` 必须保持为 `buy|hold|sell`。
- 所有面向使用者的人类可读文本值必须使用中文。
"""


# ============================================================
# Agent Executor
# ============================================================

class AgentExecutor:
    """ReAct agent loop with tool calling.

    Usage::

        executor = AgentExecutor(tool_registry, llm_adapter)
        result = executor.run("Analyze stock 600519")
    """

    def __init__(
        self,
        tool_registry: ToolRegistry,
        llm_adapter: LLMToolAdapter,
        skill_instructions: str = "",
        default_skill_policy: str = "",
        use_legacy_default_prompt: bool = False,
        max_steps: int = 10,
        timeout_seconds: Optional[float] = None,
    ):
        self.tool_registry = tool_registry
        self.llm_adapter = llm_adapter
        self.skill_instructions = skill_instructions
        self.default_skill_policy = default_skill_policy
        self.use_legacy_default_prompt = use_legacy_default_prompt
        self.max_steps = max_steps
        self.timeout_seconds = timeout_seconds

    def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> AgentResult:
        """Execute the agent loop for a given task.

        Args:
            task: The user task / analysis request.
            context: Optional context dict (e.g., {"stock_code": "600519"}).

        Returns:
            AgentResult with parsed dashboard or error.
        """
        # Build system prompt with skills
        skills_section = ""
        if self.skill_instructions:
            skills_section = f"## 激活的交易技能\n\n{self.skill_instructions}"
        default_skill_policy_section = ""
        if self.default_skill_policy:
            default_skill_policy_section = f"\n{self.default_skill_policy}\n"
        report_language = normalize_report_language((context or {}).get("report_language", "zh"))
        stock_code = (context or {}).get("stock_code", "")
        market_role = get_market_role(stock_code, report_language)
        market_guidelines = get_market_guidelines(stock_code, report_language)
        prompt_template = (
            LEGACY_DEFAULT_AGENT_SYSTEM_PROMPT
            if self.use_legacy_default_prompt
            else AGENT_SYSTEM_PROMPT
        )
        system_prompt = prompt_template.format(
            market_role=market_role,
            market_guidelines=market_guidelines,
            default_skill_policy_section=default_skill_policy_section,
            skills_section=skills_section,
            language_section=_build_language_section(report_language),
        )

        # Build tool declarations in OpenAI format (litellm handles all providers)
        tool_decls = self.tool_registry.to_openai_tools()

        # Initialize conversation
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": self._build_user_message(task, context)},
        ]

        return self._run_loop(messages, tool_decls, parse_dashboard=True)

    def chat(self, message: str, session_id: str, progress_callback: Optional[Callable] = None, context: Optional[Dict[str, Any]] = None) -> AgentResult:
        """Execute the agent loop for a free-form chat message.

        Args:
            message: The user's chat message.
            session_id: The conversation session ID.
            progress_callback: Optional callback for streaming progress events.
            context: Optional context dict from previous analysis for data reuse.

        Returns:
            AgentResult with the text response.
        """
        from src.agent.conversation import conversation_manager

        # Build system prompt with skills
        skills_section = ""
        if self.skill_instructions:
            skills_section = f"## 激活的交易技能\n\n{self.skill_instructions}"
        default_skill_policy_section = ""
        if self.default_skill_policy:
            default_skill_policy_section = f"\n{self.default_skill_policy}\n"
        report_language = normalize_report_language((context or {}).get("report_language", "zh"))
        stock_code = (context or {}).get("stock_code", "")
        market_role = get_market_role(stock_code, report_language)
        market_guidelines = get_market_guidelines(stock_code, report_language)
        prompt_template = (
            LEGACY_DEFAULT_CHAT_SYSTEM_PROMPT
            if self.use_legacy_default_prompt
            else CHAT_SYSTEM_PROMPT
        )
        system_prompt = prompt_template.format(
            market_role=market_role,
            market_guidelines=market_guidelines,
            default_skill_policy_section=default_skill_policy_section,
            skills_section=skills_section,
            language_section=_build_language_section(report_language, chat_mode=True),
        )

        # Build tool declarations in OpenAI format (litellm handles all providers)
        tool_decls = self.tool_registry.to_openai_tools()

        # Get conversation history
        session = conversation_manager.get_or_create(session_id)
        history = session.get_history()

        # Initialize conversation
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
        ]
        messages.extend(history)

        # Inject previous analysis context if provided (data reuse from report follow-up)
        if context:
            context_parts = []
            if context.get("stock_code"):
                context_parts.append(f"股票代碼: {context['stock_code']}")
            if context.get("stock_name"):
                context_parts.append(f"股票名称: {context['stock_name']}")
            if context.get("previous_price"):
                context_parts.append(f"上次分析价格: {context['previous_price']}")
            if context.get("previous_change_pct"):
                context_parts.append(f"上次漲跌幅: {context['previous_change_pct']}%")
            if context.get("previous_analysis_summary"):
                summary = context["previous_analysis_summary"]
                summary_text = json.dumps(summary, ensure_ascii=False) if isinstance(summary, dict) else str(summary)
                context_parts.append(f"上次分析摘要:\n{summary_text}")
            if context.get("previous_strategy"):
                strategy = context["previous_strategy"]
                strategy_text = json.dumps(strategy, ensure_ascii=False) if isinstance(strategy, dict) else str(strategy)
                context_parts.append(f"上次策略分析:\n{strategy_text}")
            if context_parts:
                context_msg = "[系統提供的历史分析上下文，可供參考对比]\n" + "\n".join(context_parts)
                messages.append({"role": "user", "content": context_msg})
                messages.append({"role": "assistant", "content": "好的，我已了解该股票的历史分析數據。请告诉我你想了解什么？"})

        messages.append({"role": "user", "content": message})

        # Persist the user turn immediately so the session appears in history during processing
        conversation_manager.add_message(session_id, "user", message)

        result = self._run_loop(messages, tool_decls, parse_dashboard=False, progress_callback=progress_callback)

        # Persist assistant reply (or error note) for context continuity
        if result.success:
            conversation_manager.add_message(session_id, "assistant", result.content)
        else:
            error_note = f"[分析失败] {result.error or '未知錯誤'}"
            conversation_manager.add_message(session_id, "assistant", error_note)

        return result

    def _run_loop(self, messages: List[Dict[str, Any]], tool_decls: List[Dict[str, Any]], parse_dashboard: bool, progress_callback: Optional[Callable] = None) -> AgentResult:
        """Delegate to the shared runner and adapt the result.

        This preserves the exact same observable behaviour as the original
        inline implementation while sharing the single authoritative loop
        in :mod:`src.agent.runner`.
        """
        loop_result = run_agent_loop(
            messages=messages,
            tool_registry=self.tool_registry,
            llm_adapter=self.llm_adapter,
            max_steps=self.max_steps,
            progress_callback=progress_callback,
            max_wall_clock_seconds=self.timeout_seconds,
        )

        model_str = loop_result.model

        if parse_dashboard and loop_result.success:
            dashboard = parse_dashboard_json(loop_result.content)
            return AgentResult(
                success=dashboard is not None,
                content=loop_result.content,
                dashboard=dashboard,
                tool_calls_log=loop_result.tool_calls_log,
                total_steps=loop_result.total_steps,
                total_tokens=loop_result.total_tokens,
                provider=loop_result.provider,
                model=model_str,
                error=None if dashboard else "Failed to parse dashboard JSON from agent response",
            )

        return AgentResult(
            success=loop_result.success,
            content=loop_result.content,
            dashboard=None,
            tool_calls_log=loop_result.tool_calls_log,
            total_steps=loop_result.total_steps,
            total_tokens=loop_result.total_tokens,
            provider=loop_result.provider,
            model=model_str,
            error=loop_result.error,
        )

    def _build_user_message(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Build the initial user message."""
        parts = [task]
        if context:
            report_language = normalize_report_language(context.get("report_language", "zh"))
            if context.get("stock_code"):
                parts.append(f"\n股票代碼: {context['stock_code']}")
            if context.get("report_type"):
                parts.append(f"报告类型: {context['report_type']}")
            if report_language == "en":
                parts.append("輸出语言: English（所有 JSON 键名保持不变，所有面向使用者的文本值使用英文）")
            else:
                parts.append("輸出语言: 中文（所有 JSON 键名保持不变，所有面向使用者的文本值使用中文）")

            # Inject pre-fetched context data to avoid redundant fetches
            if context.get("realtime_quote"):
                parts.append(f"\n[系統已獲取的实时行情]\n{json.dumps(context['realtime_quote'], ensure_ascii=False)}")
            if context.get("chip_distribution"):
                parts.append(f"\n[系統已獲取的筹码分布]\n{json.dumps(context['chip_distribution'], ensure_ascii=False)}")
            if context.get("news_context"):
                parts.append(f"\n[系統已獲取的新闻与舆情情报]\n{context['news_context']}")

        parts.append("\n请使用可用工具獲取缺失的數據（如历史K线、新闻等），然后以决策仪表盘 JSON 格式輸出分析结果。")
        return "\n".join(parts)
