"""Utility functions for core functionality."""

from __future__ import annotations

from typing import Any

from rest_framework.response import Response


def api_response(
    success: bool,
    message: str | None = None,
    data: dict[str, Any] | list[Any] | None = None,
    status_code: int | None = None,
) -> Response:
    """Build standardized API response.
    
    Args:
        success: Whether the operation was successful
        message: Human-readable message
        data: Response payload
        status_code: HTTP status code
    
    Returns:
        DRF Response object
    """
    body = {"success": success}
    if message:
        body["message"] = message
    if data is not None:
        body["data"] = data
    
    return Response(body, status=status_code)
