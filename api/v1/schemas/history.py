# -*- coding: utf-8 -*-
"""
===================================
历史记录相關模型
===================================

职责：
1. 定义历史记录列表和详情模型
2. 定义分析报告完整模型
"""

from typing import Optional, List, Any

from pydantic import BaseModel, ConfigDict, Field


class HistoryItem(BaseModel):
    """历史记录摘要（列表展示用）"""

    id: Optional[int] = Field(None, description="分析历史记录主键 ID")
    query_id: str = Field(..., description="分析记录關聯 query_id（批量分析时重复）")
    stock_code: str = Field(..., description="股票代碼")
    stock_name: Optional[str] = Field(None, description="股票名称")
    report_type: Optional[str] = Field(None, description="报告类型")
    sentiment_score: Optional[int] = Field(
        None,
        description="情绪評分（历史數據可能超出 0-100 範圍，讀取时不做約束）",
    )
    operation_advice: Optional[str] = Field(None, description="操作建议")
    created_at: Optional[str] = Field(None, description="建立时间")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1234,
                "query_id": "abc123",
                "stock_code": "600519",
                "stock_name": "贵州茅台",
                "report_type": "detailed",
                "sentiment_score": 75,
                "operation_advice": "持有",
                "created_at": "2024-01-01T12:00:00"
            }
        }


class HistoryListResponse(BaseModel):
    """历史记录列表回應"""
    
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    limit: int = Field(..., description="每页数量")
    items: List[HistoryItem] = Field(default_factory=list, description="记录列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total": 100,
                "page": 1,
                "limit": 20,
                "items": []
            }
        }


class DeleteHistoryRequest(BaseModel):
    """刪除历史记录請求"""

    record_ids: List[int] = Field(default_factory=list, description="要刪除的历史记录主键 ID 列表")


class DeleteHistoryResponse(BaseModel):
    """刪除历史记录回應"""

    deleted: int = Field(..., description="實際刪除的历史记录数量")


class NewsIntelItem(BaseModel):
    """新闻情报条目"""

    title: str = Field(..., description="新闻标题")
    snippet: str = Field("", description="新闻摘要（最多200字）")
    url: str = Field(..., description="新闻链接")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "公司發佈业绩快报，营收同比增长 20%",
                "snippet": "公司公告顯示，季度营收同比增长 20%...",
                "url": "https://example.com/news/123"
            }
        }


class NewsIntelResponse(BaseModel):
    """新闻情报回應"""

    total: int = Field(..., description="新闻条数")
    items: List[NewsIntelItem] = Field(default_factory=list, description="新闻列表")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 2,
                "items": []
            }
        }


class ReportMeta(BaseModel):
    """报告元資訊"""

    model_config = ConfigDict(protected_namespaces=("model_validate", "model_dump"))

    id: Optional[int] = Field(None, description="分析历史记录主键 ID（仅历史报告有此欄位）")
    query_id: str = Field(..., description="分析记录關聯 query_id（批量分析时重复）")
    stock_code: str = Field(..., description="股票代碼")
    stock_name: Optional[str] = Field(None, description="股票名称")
    report_type: Optional[str] = Field(None, description="报告类型")
    report_language: Optional[str] = Field(None, description="报告輸出语言（zh/en）")
    created_at: Optional[str] = Field(None, description="建立时间")
    current_price: Optional[float] = Field(None, description="分析时股價")
    change_pct: Optional[float] = Field(None, description="分析时漲跌幅(%)")
    model_used: Optional[str] = Field(None, description="分析使用的 LLM 模型")


class ReportSummary(BaseModel):
    """报告概览区"""
    
    analysis_summary: Optional[str] = Field(None, description="關鍵结论")
    operation_advice: Optional[str] = Field(None, description="操作建议")
    trend_prediction: Optional[str] = Field(None, description="趨勢預測")
    sentiment_score: Optional[int] = Field(
        None,
        description="情绪評分（历史數據可能超出 0-100 範圍，讀取时不做約束）",
    )
    sentiment_label: Optional[str] = Field(None, description="情绪標籤")


class ReportStrategy(BaseModel):
    """策略点位区"""
    
    ideal_buy: Optional[str] = Field(None, description="理想買入价")
    secondary_buy: Optional[str] = Field(None, description="第二買入价")
    stop_loss: Optional[str] = Field(None, description="止损价")
    take_profit: Optional[str] = Field(None, description="止盈价")


class ReportDetails(BaseModel):
    """报告详情区"""
    
    news_content: Optional[str] = Field(None, description="新闻摘要")
    raw_result: Optional[Any] = Field(None, description="原始分析结果（JSON）")
    context_snapshot: Optional[Any] = Field(None, description="分析时上下文快照（JSON）")
    financial_report: Optional[Any] = Field(None, description="结构化财报摘要（来自 fundamental_context）")
    dividend_metrics: Optional[Any] = Field(None, description="结构化分红指標（含 TTM 口径）")
    belong_boards: Optional[Any] = Field(None, description="關聯板塊列表")
    sector_rankings: Optional[Any] = Field(None, description="板塊漲跌榜（结构 {top, bottom}）")


class AnalysisReport(BaseModel):
    """完整分析报告"""

    meta: ReportMeta = Field(..., description="元資訊")
    summary: ReportSummary = Field(..., description="概览区")
    strategy: Optional[ReportStrategy] = Field(None, description="策略点位区")
    details: Optional[ReportDetails] = Field(None, description="详情区")

    class Config:
        json_schema_extra = {
            "example": {
                "meta": {
                    "query_id": "abc123",
                    "stock_code": "600519",
                    "stock_name": "贵州茅台",
                    "report_type": "detailed",
                    "report_language": "zh",
                    "created_at": "2024-01-01T12:00:00"
                },
                "summary": {
                    "analysis_summary": "技术面向好，建议持有",
                    "operation_advice": "持有",
                    "trend_prediction": "看多",
                    "sentiment_score": 75,
                    "sentiment_label": "乐观"
                },
                "strategy": {
                    "ideal_buy": "1800.00",
                    "secondary_buy": "1750.00",
                    "stop_loss": "1700.00",
                    "take_profit": "2000.00"
                },
                "details": None
            }
        }


class MarkdownReportResponse(BaseModel):
    """Markdown 格式报告回應"""

    content: str = Field(..., description="Markdown 格式的完整报告内容")

    class Config:
        json_schema_extra = {
            "example": {
                "content": "# 📊 贵州茅台 (600519) 分析报告\n\n> 分析日期：**2024-01-01**\n\n..."
            }
        }
