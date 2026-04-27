"""Exceptions for Huwise Automation API interactions."""

from __future__ import annotations

import json
from typing import Any

import httpx


class HuwiseAutomationError(httpx.HTTPStatusError):
    """Raised when the Automation API returns an error HTTP status.

    Subclasses :class:`httpx.HTTPStatusError` so existing ``except httpx.HTTPStatusError``
    handlers still catch failures. Prefer this type when you need structured ``detail``
    parsed from JSON error bodies (validation errors, etc.).
    """

    def __init__(
        self,
        message: str,
        *,
        request: httpx.Request,
        response: httpx.Response,
        detail: dict[str, Any] | list[Any] | None = None,
    ) -> None:
        super().__init__(message, request=request, response=response)
        self.detail = detail

    @classmethod
    def from_response(cls, response: httpx.Response) -> HuwiseAutomationError:
        """Build an error from a completed response (status should be >= 400)."""
        request = response.request
        url_str = str(response.url)
        detail_json: dict[str, Any] | list[Any] | None = None
        try:
            data = response.json()
            if isinstance(data, dict | list):
                detail_json = data
            body_preview = json.dumps(data, ensure_ascii=False)[:4096]
        except Exception:
            body_preview = (response.text or "")[:4096]

        reason = (getattr(response, "reason_phrase", None) or "").strip()
        code = response.status_code if isinstance(response.status_code, int) else "?"
        message = f"{code} {reason} for {request.method} {url_str}\nResponse body (preview): {body_preview}"
        return cls(message, request=request, response=response, detail=detail_json)
