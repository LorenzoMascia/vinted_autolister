# ============================================================================
# FILE: src/api/middleware.py
# Middleware API
# ============================================================================

from fastapi import Request
import time
import logging

async def log_requests(request: Request, call_next):
    """Middleware per logging richieste API"""
    
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logging.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.2f}s"
    )
    
    return response