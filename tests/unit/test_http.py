"""Unit tests for HTTP client module."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from huwise_utils_py.config import HuwiseConfig
from huwise_utils_py.http import (
    DEFAULT_LIMITS,
    DEFAULT_TIMEOUT,
    HttpClient,
    retry,
)


class TestHttpClient:
    """Tests for HttpClient class."""

    def test_http_client_get_calls_correct_url(
        self, mock_config: HuwiseConfig
    ) -> None:
        """Test that GET request uses correct URL."""
        client = HttpClient(mock_config)

        with patch("huwise_utils_py.http.httpx.Client") as mock_httpx:
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_instance = MagicMock()
            mock_instance.__enter__ = MagicMock(return_value=mock_instance)
            mock_instance.__exit__ = MagicMock(return_value=False)
            mock_instance.get.return_value = mock_response
            mock_httpx.return_value = mock_instance

            client.get("/datasets/da_123")

            mock_instance.get.assert_called_once()
            call_args = mock_instance.get.call_args
            assert "/datasets/da_123" in call_args[0][0]

    def test_http_client_post_calls_correct_url(
        self, mock_config: HuwiseConfig
    ) -> None:
        """Test that POST request uses correct URL."""
        client = HttpClient(mock_config)

        with patch("huwise_utils_py.http.httpx.Client") as mock_httpx:
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_instance = MagicMock()
            mock_instance.__enter__ = MagicMock(return_value=mock_instance)
            mock_instance.__exit__ = MagicMock(return_value=False)
            mock_instance.post.return_value = mock_response
            mock_httpx.return_value = mock_instance

            client.post("/datasets/da_123/publish/")

            mock_instance.post.assert_called_once()

    def test_http_client_uses_config_headers(
        self, mock_config: HuwiseConfig
    ) -> None:
        """Test that requests include authorization headers."""
        client = HttpClient(mock_config)

        with patch("huwise_utils_py.http.httpx.Client") as mock_httpx:
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_instance = MagicMock()
            mock_instance.__enter__ = MagicMock(return_value=mock_instance)
            mock_instance.__exit__ = MagicMock(return_value=False)
            mock_instance.get.return_value = mock_response
            mock_httpx.return_value = mock_instance

            client.get("/test")

            call_kwargs = mock_instance.get.call_args[1]
            assert "headers" in call_kwargs
            assert "Authorization" in call_kwargs["headers"]


class TestRetryDecorator:
    """Tests for retry decorator."""

    def test_retry_returns_result_on_success(self) -> None:
        """Test that retry returns result when function succeeds."""
        @retry(ValueError, tries=3)
        def always_succeeds():
            return "success"

        result = always_succeeds()
        assert result == "success"

    def test_retry_retries_on_specified_exception(self) -> None:
        """Test that retry retries on specified exception."""
        call_count = 0

        @retry(ValueError, tries=3, delay=0.01)
        def fails_then_succeeds():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("temporary failure")
            return "success"

        result = fails_then_succeeds()
        assert result == "success"
        assert call_count == 2

    def test_retry_raises_after_max_tries(self) -> None:
        """Test that retry raises exception after max tries."""
        @retry(ValueError, tries=2, delay=0.01)
        def always_fails():
            raise ValueError("permanent failure")

        with pytest.raises(ValueError, match="permanent failure"):
            always_fails()


class TestDefaultConstants:
    """Tests for default configuration constants."""

    def test_default_timeout_is_httpx_timeout(self) -> None:
        """Test that DEFAULT_TIMEOUT is an httpx.Timeout."""
        assert isinstance(DEFAULT_TIMEOUT, httpx.Timeout)

    def test_default_limits_is_httpx_limits(self) -> None:
        """Test that DEFAULT_LIMITS is an httpx.Limits."""
        assert isinstance(DEFAULT_LIMITS, httpx.Limits)
