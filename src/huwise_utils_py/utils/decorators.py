"""Decorators for Huwise Utils.

This module provides reusable decorators following DCC coding standards.
"""

import functools
import time
from typing import Any

from huwise_utils_py.logger import get_logger

logger = get_logger(__name__)


def retry(
    exceptions_to_check: type[Exception] | tuple[type[Exception], ...],
    tries: int = 4,
    delay: float = 3,
    backoff: float = 2,
) -> Any:
    """Retry decorator with exponential backoff.

    Retries the decorated function on specified exceptions with
    configurable attempts and exponential delay.

    Args:
        exceptions_to_check: Exception(s) to catch and retry on.
        tries: Number of attempts before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Multiplier for delay after each retry.

    Returns:
        Decorated function with retry logic.

    Example:
        ```python
        @retry(ConnectionError, tries=3, delay=1)
        def fetch_data():
            return requests.get("https://api.example.com")
        ```
    """

    def decorator(func: Any) -> Any:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions_to_check as e:
                    logger.warning(
                        "Function failed, retrying",
                        function=func.__name__,
                        error=str(e),
                        retries_left=mtries - 1,
                        delay_seconds=mdelay,
                    )
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_execution_time(func: Any) -> Any:
    """Log the execution time of a function.

    Args:
        func: Function to decorate.

    Returns:
        Decorated function that logs execution time.
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(
            "Function executed",
            function=func.__name__,
            duration_ms=round(elapsed * 1000, 2),
        )
        return result

    return wrapper
