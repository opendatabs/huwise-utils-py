"""Airflow-friendly logging utilities for Huwise Utils.

This module provides:
- ``init_logger`` to initialize stdlib logging safely.
- ``get_logger`` returning a logger adapter that accepts structured keyword
  arguments (``logger.info("msg", key=value)``), preserving existing call sites.
"""

import logging
from collections.abc import Mapping
from typing import Any

DEFAULT_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
_STANDARD_LOG_KWARGS = {"exc_info", "stack_info", "stacklevel", "extra"}


class _StructuredLoggerAdapter(logging.LoggerAdapter[logging.Logger]):
    """Logger adapter that serializes keyword fields into single-line messages."""

    def process(self, msg: object, kwargs: Mapping[str, Any]) -> tuple[str, dict[str, Any]]:
        msg_text = str(msg)
        logging_kwargs: dict[str, Any] = {}
        structured_fields: dict[str, Any] = {}

        for key, value in kwargs.items():
            if key in _STANDARD_LOG_KWARGS:
                logging_kwargs[key] = value
            else:
                structured_fields[key] = value

        if structured_fields:
            parts = [f"{field}={value!r}" for field, value in structured_fields.items()]
            msg_text = f"{msg_text} | {' '.join(parts)}"

        return msg_text, logging_kwargs


def init_logger(
    level: int | str = logging.INFO,
    *,
    fmt: str = DEFAULT_LOG_FORMAT,
    datefmt: str = "%Y-%m-%d %H:%M:%S",
    force: bool = False,
) -> None:
    """Initialize root logger.

    This avoids adding duplicate handlers in environments like Airflow where
    logging handlers are often configured externally.
    """
    root_logger = logging.getLogger()
    if not root_logger.handlers or force:
        logging.basicConfig(level=level, format=fmt, datefmt=datefmt, force=force)
    else:
        root_logger.setLevel(level)


def get_logger(name: str | None = None) -> logging.LoggerAdapter[logging.Logger]:
    """Get a structured logger adapter for the given module name."""
    return _StructuredLoggerAdapter(logging.getLogger(name), {})


__all__ = ["DEFAULT_LOG_FORMAT", "get_logger", "init_logger"]
