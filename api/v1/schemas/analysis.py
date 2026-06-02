# -*- coding: utf-8 -*-
"""
===================================
分析相关模型
===================================

职责：
1. 定义分析請求和回應模型
2. 定义工作狀態模型
3. 定义非同步工作隊列相关模型
"""

from typing import Optional, List, Any
from enum import Enum

from pydantic import AliasChoices, BaseModel, Field
from src.utils.analysis_metadata import SELECTION_SOURCE_PATTERN


class TaskStatusEnum(str, Enum):
    """工作狀態枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalyzeRequest(BaseModel):
    """Analysis request parameters"""
    
    stock_code: Optional[str] = Field(
        None, 
        description="单只股票代碼", 
        example="600519"
    )
    stock_codes: Optional[List[str]] = Field(
        None, 
        description="多只股票代碼（与 stock_code 二选一）",
        example=["600519", "000858"]
    )
    report_type: str = Field(
        "detailed",
        description="报告类型：simple(精简) / detailed(完整) / full(完整) / brief(简洁)",
        pattern="^(simple|detailed|full|brief)$",
    )
    force_refresh: bool = Field(
        False,
        description="是否强制刷新（忽略快取）"
    )
    async_mode: bool = Field(
        False,
        description="是否使用非同步模式"
    )
    stock_name: Optional[str] = Field(
        None,
        description="使用者选中的股票名称（自动补全时提供）",
        example="贵州茅台"
    )
    original_query: Optional[str] = Field(
        None,
        description="使用者原始输入（如茅台、gzmt、600519）",
        example="茅台"
    )
    selection_source: Optional[str] = Field(
        None,
        description="股票选择来源：manual(手动输入) | autocomplete(自动补全) | import(匯入) | image(图片识别)",
        pattern=SELECTION_SOURCE_PATTERN,
        example="autocomplete"
    )
    notify: bool = Field(
        True,
        description="是否发送推送通知（Telegram/企业微信等）"
    )
    skills: Optional[List[str]] = Field(
        None,
        validation_alias=AliasChoices("skills", "strategies"),
        description="本次分析使用的策略 skill ID 列表；兼容 legacy strategies 欄位",
        example=["bull_trend", "growth_quality"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "stock_code": "600519",
                "report_type": "detailed",
                "force_refresh": False,
                "async_mode": False,
                "stock_name": "贵州茅台",
                "original_query": "茅台",
                "selection_source": "autocomplete",
                "notify": True,
                "skills": ["bull_trend"]
            }
        }


class MarketReviewRequest(BaseModel):
    """Market review trigger parameters."""

    send_notification: bool = Field(
        True,
        description="是否在大盤复盘完成后发送推送通知",
    )


class MarketReviewAccepted(BaseModel):
    """Market review background task accepted response."""

    status: str = Field("accepted", description="提交狀態")
    message: str = Field(..., description="提示資訊")
    send_notification: bool = Field(..., description="是否发送通知")
    task_id: Optional[str] = Field(
        None,
        description="工作 ID（仅当工作实际提交时傳回）",
    )


class AnalysisResultResponse(BaseModel):
    """分析结果回應模型"""
    
    query_id: str = Field(..., description="分析记录唯一标识")
    stock_code: str = Field(..., description="股票代碼")
    stock_name: Optional[str] = Field(None, description="股票名称")
    report: Optional[Any] = Field(None, description="分析报告")
    created_at: str = Field(..., description="建立时间")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query_id": "abc123def456",
                "stock_code": "600519",
                "stock_name": "贵州茅台",
                "report": {
                    "summary": {
                        "sentiment_score": 75,
                        "operation_advice": "持有"
                    }
                },
                "created_at": "2024-01-01T12:00:00"
            }
        }


class TaskAccepted(BaseModel):
    """非同步工作接受回應"""
    
    task_id: str = Field(..., description="工作 ID，用于查詢狀態")
    status: str = Field(
        ..., 
        description="工作狀態",
        pattern="^(pending|processing)$"
    )
    message: Optional[str] = Field(None, description="提示資訊")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "task_abc123",
                "status": "pending",
                "message": "Analysis task accepted"
            }
        }


class BatchTaskAcceptedItem(BaseModel):
    """批量非同步工作中的单个成功提交项。"""

    task_id: str = Field(..., description="工作 ID，用于查詢狀態")
    stock_code: str = Field(..., description="股票代碼")
    status: str = Field(
        ...,
        description="工作狀態",
        pattern="^(pending|processing)$"
    )
    message: Optional[str] = Field(None, description="提示資訊")

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "task_abc123",
                "stock_code": "600519",
                "status": "pending",
                "message": "分析工作已加入隊列: 600519"
            }
        }


class BatchDuplicateTaskItem(BaseModel):
    """批量非同步工作中的重复提交项。"""

    stock_code: str = Field(..., description="股票代碼")
    existing_task_id: str = Field(..., description="已存在的工作 ID")
    message: str = Field(..., description="錯誤資訊")

    class Config:
        json_schema_extra = {
            "example": {
                "stock_code": "600519",
                "existing_task_id": "task_existing_123",
                "message": "股票 600519 正在分析中 (task_id: task_existing_123)"
            }
        }


class BatchTaskAcceptedResponse(BaseModel):
    """批量非同步工作接受回應。"""

    accepted: List[BatchTaskAcceptedItem] = Field(default_factory=list, description="成功提交的工作列表")
    duplicates: List[BatchDuplicateTaskItem] = Field(default_factory=list, description="重复而略過的工作列表")
    message: str = Field(..., description="汇总資訊")

    class Config:
        json_schema_extra = {
            "example": {
                "accepted": [
                    {
                        "task_id": "task_abc123",
                        "stock_code": "600519",
                        "status": "pending",
                        "message": "分析工作已加入隊列: 600519"
                    }
                ],
                "duplicates": [
                    {
                        "stock_code": "000858",
                        "existing_task_id": "task_existing_456",
                        "message": "股票 000858 正在分析中 (task_id: task_existing_456)"
                    }
                ],
                "message": "已提交 1 个工作，1 个重复略過"
            }
        }


class TaskStatus(BaseModel):
    """Task status model"""
    
    task_id: str = Field(..., description="工作 ID")
    status: str = Field(
        ..., 
        description="工作狀態",
        pattern="^(pending|processing|completed|failed)$"
    )
    progress: Optional[int] = Field(
        None, 
        description="进度百分比 (0-100)",
        ge=0,
        le=100
    )
    result: Optional[AnalysisResultResponse] = Field(
        None, 
        description="分析结果（仅在 completed 时存在）"
    )
    market_review_report: Optional[str] = Field(
        None,
        description="大盤复盘工作傳回的报告文本（仅大盤复盘工作）",
    )
    error: Optional[str] = Field(
        None, 
        description="錯誤資訊（仅在 failed 时存在）"
    )
    stock_name: Optional[str] = Field(None, description="股票名称")
    original_query: Optional[str] = Field(None, description="使用者原始输入")
    selection_source: Optional[str] = Field(
        None,
        description="选择来源",
        pattern=SELECTION_SOURCE_PATTERN,
    )
    skills: Optional[List[str]] = Field(None, description="本次工作使用的策略 skill ID 列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "task_abc123",
                "status": "completed",
                "progress": 100,
                "result": None,
                "market_review_report": None,
                "error": None,
                "stock_name": "贵州茅台",
                "original_query": "茅台",
                "selection_source": "autocomplete",
                "skills": ["bull_trend"]
            }
        }


class TaskInfo(BaseModel):
    """
    Task details model

    Used for task list and SSE event delivery
    """
    
    task_id: str = Field(..., description="工作 ID")
    stock_code: str = Field(..., description="股票代碼")
    stock_name: Optional[str] = Field(None, description="股票名称")
    status: TaskStatusEnum = Field(..., description="工作狀態")
    progress: int = Field(0, description="进度百分比 (0-100)", ge=0, le=100)
    message: Optional[str] = Field(None, description="狀態訊息")
    report_type: str = Field("detailed", description="报告类型")
    created_at: str = Field(..., description="建立时间")
    started_at: Optional[str] = Field(None, description="开始执行时间")
    completed_at: Optional[str] = Field(None, description="完成时间")
    error: Optional[str] = Field(None, description="錯誤資訊（仅在 failed 时存在）")
    original_query: Optional[str] = Field(None, description="使用者原始输入")
    selection_source: Optional[str] = Field(
        None,
        description="选择来源",
        pattern=SELECTION_SOURCE_PATTERN,
    )
    skills: Optional[List[str]] = Field(None, description="本次工作使用的策略 skill ID 列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "abc123def456",
                "stock_code": "600519",
                "stock_name": "贵州茅台",
                "status": "processing",
                "progress": 50,
                "message": "正在分析中...",
                "report_type": "detailed",
                "created_at": "2026-02-05T10:30:00",
                "started_at": "2026-02-05T10:30:01",
                "completed_at": None,
                "error": None,
                "original_query": "茅台",
                "selection_source": "autocomplete",
                "skills": ["bull_trend"]
            }
        }


class TaskListResponse(BaseModel):
    """工作列表回應模型"""
    
    total: int = Field(..., description="工作总数")
    pending: int = Field(..., description="等待中的工作数")
    processing: int = Field(..., description="處理中的工作数")
    tasks: List[TaskInfo] = Field(..., description="工作列表")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total": 3,
                "pending": 1,
                "processing": 2,
                "tasks": []
            }
        }


class DuplicateTaskErrorResponse(BaseModel):
    """重复工作錯誤回應模型"""
    
    error: str = Field("duplicate_task", description="錯誤类型")
    message: str = Field(..., description="錯誤資訊")
    stock_code: str = Field(..., description="股票代碼")
    existing_task_id: str = Field(..., description="已存在的工作 ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "duplicate_task",
                "message": "股票 600519 正在分析中",
                "stock_code": "600519",
                "existing_task_id": "abc123def456"
            }
        }
