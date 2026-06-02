# -*- coding: utf-8 -*-
"""
===================================
通用回應模型
===================================

职责：
1. 定义通用的回應模型（HealthResponse, ErrorResponse 等）
2. 提供统一的回應格式
"""

from typing import Optional, Any

from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    """API 根路由回應"""
    
    message: str = Field(..., description="API 執行狀態訊息", example="Daily Stock Analysis API is running")
    version: Optional[str] = Field(None, description="API 版本", example="1.0.0")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Daily Stock Analysis API is running",
                "version": "1.0.0"
            }
        }


class HealthResponse(BaseModel):
    """健康檢查回應"""
    
    status: str = Field(..., description="服務狀態", example="ok")
    timestamp: Optional[str] = Field(None, description="时间戳")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "timestamp": "2024-01-01T12:00:00"
            }
        }


class ErrorResponse(BaseModel):
    """錯誤回應"""
    
    error: str = Field(..., description="錯誤类型", example="validation_error")
    message: str = Field(..., description="錯誤详情", example="請求參數錯誤")
    detail: Optional[Any] = Field(None, description="附加錯誤資訊")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "not_found",
                "message": "资源不存在",
                "detail": None
            }
        }


class SuccessResponse(BaseModel):
    """通用成功回應"""
    
    success: bool = Field(True, description="是否成功")
    message: Optional[str] = Field(None, description="成功訊息")
    data: Optional[Any] = Field(None, description="回應數據")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "操作成功",
                "data": None
            }
        }
