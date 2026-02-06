"""Structured logging for Huwise Utils.

This module re-exports the logging utilities from dcc-backend-common
for consistent structured logging across the package.

Usage:
    from huwise_utils_py.logger import get_logger

    logger = get_logger(__name__)
    logger.info("Operation completed", dataset_uid="da_123", field_count=5)
"""

from dcc_backend_common.logger import get_logger, init_logger

__all__ = ["get_logger", "init_logger"]
