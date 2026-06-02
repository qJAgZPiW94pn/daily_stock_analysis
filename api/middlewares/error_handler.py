# -*- coding: utf-8 -*-
"""
===================================
全局异常處理中间件
===================================

职责：
1. 捕获未處理的异常
2. 统一錯誤回應格式
3. 记录錯誤日誌
"""

import logging
import traceback
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    全局异常處理中间件
    
    捕获所有未處理的异常，傳回统一格式的錯誤回應
    """
    
    async def dispatch(
        self, 
        request: Request, 
        call_next: Callable
    ) -> Response:
        """
        處理請求，捕获异常
        
        Args:
            request: 請求对象
            call_next: 下一个處理器
            
        Returns:
            Response: 回應对象
        """
        try:
            response = await call_next(request)
            return response
            
        except Exception as e:
            # 记录錯誤日誌
            logger.error(
                f"未處理的异常: {e}\n"
                f"請求路徑: {request.url.path}\n"
                f"請求方法: {request.method}\n"
                f"堆疊: {traceback.format_exc()}"
            )
            
            # 傳回统一格式的錯誤回應
            return JSONResponse(
                status_code=500,
                content={
                    "error": "internal_error",
                    "message": "服務器内部錯誤，请稍后重试",
                    "detail": str(e) if logger.isEnabledFor(logging.DEBUG) else None
                }
            )


def add_error_handlers(app) -> None:
    """
    添加全局异常處理器
    
    为 FastAPI 应用添加各类异常的處理器
    
    Args:
        app: FastAPI 应用实例
    """
    from fastapi import HTTPException
    from fastapi.exceptions import RequestValidationError
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """處理 HTTP 异常"""
        # 如果 detail 已经是 ErrorResponse 格式的 dict，直接使用
        if isinstance(exc.detail, dict) and "error" in exc.detail and "message" in exc.detail:
            return JSONResponse(
                status_code=exc.status_code,
                content=exc.detail
            )
        # 否则将 detail 包装成 ErrorResponse 格式
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "http_error",
                "message": str(exc.detail) if exc.detail else "HTTP Error",
                "detail": None
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """處理請求验证异常"""
        return JSONResponse(
            status_code=422,
            content={
                "error": "validation_error",
                "message": "請求參數验证失败",
                "detail": exc.errors()
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """處理通用异常"""
        logger.error(
            f"未處理的异常: {exc}\n"
            f"請求路徑: {request.url.path}\n"
            f"堆疊: {traceback.format_exc()}"
        )
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_error",
                "message": "服務器内部錯誤",
                "detail": None
            }
        )
