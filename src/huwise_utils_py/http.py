"""HTTP client implementations for Huwise API.

This module provides both synchronous and asynchronous HTTP clients
with retry logic, proper timeout handling, and structured logging.
"""

import functools
import ssl
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import httpx

from huwise_utils_py.config import HuwiseConfig
from huwise_utils_py.logger import get_logger

logger = get_logger(__name__)

# Default configuration
DEFAULT_TIMEOUT = httpx.Timeout(30.0, connect=10.0)
DEFAULT_LIMITS = httpx.Limits(max_connections=100, max_keepalive_connections=20)

# HTTP errors that should trigger a retry
HTTP_ERRORS_TO_RETRY = (
    ConnectionResetError,
    httpx.ConnectError,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.ConnectTimeout,
    httpx.HTTPStatusError,
    ssl.SSLCertVerificationError,
)


def retry(
    exceptions_to_check: type[Exception] | tuple[type[Exception], ...],
    tries: int = 4,
    delay: float = 3,
    backoff: float = 2,
) -> Any:
    """Retry decorator with exponential backoff.

    Args:
        exceptions_to_check: Exception(s) to catch and retry on.
        tries: Number of attempts before giving up.
        delay: Initial delay between retries in seconds.
        backoff: Multiplier for delay after each retry.

    Returns:
        Decorated function with retry logic.
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
                        "Request failed, retrying",
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


class HttpClient:
    """Synchronous HTTP client for Huwise API.

    Provides GET, POST, PUT, PATCH, DELETE methods with automatic
    retry logic and proper header handling.

    Attributes:
        config: HuwiseConfig instance for API credentials.

    Example:
        >>> client = HttpClient(HuwiseConfig.from_env())
        >>> response = client.get("/datasets")
        >>> data = response.json()
    """

    def __init__(self, config: HuwiseConfig) -> None:
        """Initialize the HTTP client.

        Args:
            config: HuwiseConfig instance with API credentials.
        """
        self.config = config

    @retry(HTTP_ERRORS_TO_RETRY, tries=6, delay=5, backoff=1)
    def get(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Make a GET request.

        Args:
            endpoint: API endpoint (e.g., "/datasets/da_123").
            **kwargs: Additional arguments for httpx.

        Returns:
            HTTP response object.

        Raises:
            httpx.HTTPStatusError: If response indicates an error.
        """
        url = f"{self.config.base_url}{endpoint}"
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            response = client.get(url, headers=self.config.headers, **kwargs)
            response.raise_for_status()
            return response

    @retry(HTTP_ERRORS_TO_RETRY, tries=6, delay=5, backoff=1)
    def post(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Make a POST request.

        Args:
            endpoint: API endpoint.
            **kwargs: Additional arguments for httpx (e.g., json=data).

        Returns:
            HTTP response object.
        """
        url = f"{self.config.base_url}{endpoint}"
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            response = client.post(url, headers=self.config.headers, **kwargs)
            response.raise_for_status()
            return response

    @retry(HTTP_ERRORS_TO_RETRY, tries=6, delay=5, backoff=1)
    def put(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Make a PUT request.

        Args:
            endpoint: API endpoint.
            **kwargs: Additional arguments for httpx (e.g., json=data).

        Returns:
            HTTP response object.
        """
        url = f"{self.config.base_url}{endpoint}"
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            response = client.put(url, headers=self.config.headers, **kwargs)
            response.raise_for_status()
            return response

    @retry(HTTP_ERRORS_TO_RETRY, tries=6, delay=5, backoff=1)
    def patch(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Make a PATCH request.

        Args:
            endpoint: API endpoint.
            **kwargs: Additional arguments for httpx (e.g., json=data).

        Returns:
            HTTP response object.
        """
        url = f"{self.config.base_url}{endpoint}"
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            response = client.patch(url, headers=self.config.headers, **kwargs)
            response.raise_for_status()
            return response

    @retry(HTTP_ERRORS_TO_RETRY, tries=6, delay=5, backoff=1)
    def delete(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Make a DELETE request.

        Args:
            endpoint: API endpoint.
            **kwargs: Additional arguments for httpx.

        Returns:
            HTTP response object.
        """
        url = f"{self.config.base_url}{endpoint}"
        with httpx.Client(timeout=DEFAULT_TIMEOUT) as client:
            response = client.delete(url, headers=self.config.headers, **kwargs)
            response.raise_for_status()
            return response


class AsyncHttpClient:
    """Asynchronous HTTP client for concurrent Huwise API operations.

    Optimized for bulk operations with connection pooling and HTTP/2 support.

    Attributes:
        config: HuwiseConfig instance for API credentials.

    Example:
        >>> client = AsyncHttpClient(HuwiseConfig.from_env())
        >>> async with client.session() as session:
        ...     response = await session.get(f"{client.config.base_url}/datasets")
    """

    def __init__(self, config: HuwiseConfig) -> None:
        """Initialize the async HTTP client.

        Args:
            config: HuwiseConfig instance with API credentials.
        """
        self.config = config

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        """Create an async HTTP session context.

        Yields:
            Configured AsyncClient with proper timeouts and limits.

        Example:
            >>> async with client.session() as session:
            ...     tasks = [session.get(url) for url in urls]
            ...     responses = await asyncio.gather(*tasks)
        """
        async with httpx.AsyncClient(
            timeout=DEFAULT_TIMEOUT,
            limits=DEFAULT_LIMITS,
            headers=self.config.headers,
        ) as client:
            yield client

    async def get(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Make an async GET request.

        Args:
            endpoint: API endpoint.
            **kwargs: Additional arguments for httpx.

        Returns:
            HTTP response object.
        """
        url = f"{self.config.base_url}{endpoint}"
        async with self.session() as client:
            response = await client.get(url, **kwargs)
            response.raise_for_status()
            return response

    async def post(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Make an async POST request.

        Args:
            endpoint: API endpoint.
            **kwargs: Additional arguments for httpx.

        Returns:
            HTTP response object.
        """
        url = f"{self.config.base_url}{endpoint}"
        async with self.session() as client:
            response = await client.post(url, **kwargs)
            response.raise_for_status()
            return response

    async def put(self, endpoint: str, **kwargs: Any) -> httpx.Response:
        """Make an async PUT request.

        Args:
            endpoint: API endpoint.
            **kwargs: Additional arguments for httpx.

        Returns:
            HTTP response object.
        """
        url = f"{self.config.base_url}{endpoint}"
        async with self.session() as client:
            response = await client.put(url, **kwargs)
            response.raise_for_status()
            return response
