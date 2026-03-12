"""Configuration management for Huwise API access.

This module provides a Pydantic-based configuration class for managing
Huwise API credentials and settings.
"""

import os

from pydantic import BaseModel, Field

DEFAULT_HUWISE_DOMAIN = "data.bs.ch"


class AppConfigError(RuntimeError):
    """Raised when a required configuration value is missing."""


def get_env_or_throw(key: str) -> str:
    """Return env var value or raise if missing/empty."""
    value = os.getenv(key)
    if value is None or value.strip() == "":
        raise AppConfigError(f"Missing required environment variable: {key}")
    return value


def log_secret(secret: str, *, visible_suffix_chars: int = 4) -> str:
    """Mask a secret for safe logging while keeping a short suffix."""
    if len(secret) <= visible_suffix_chars:
        return "*" * len(secret)
    return f"{'*' * (len(secret) - visible_suffix_chars)}{secret[-visible_suffix_chars:]}"


class HuwiseConfig(BaseModel):
    """Configuration for Huwise API access.

    Provides type-safe configuration management with environment variable loading
    and supports dependency injection patterns.

    Attributes:
        api_key: API key for Huwise authentication.
        domain: Huwise domain (e.g., data.bs.ch).
        api_type: API version/type (defaults to automation/v1.0).

    Example:
        ```python
        config = HuwiseConfig.from_env()
        print(config.base_url)
        # Output: 'https://data.bs.ch/api/automation/v1.0'
        ```
    """

    api_key: str | None = Field(default=None, description="API key for Huwise authentication")
    domain: str = Field(default=DEFAULT_HUWISE_DOMAIN, description="Huwise domain (e.g., data.bs.ch)")
    api_type: str = Field(default="automation/v1.0", description="API version/type")

    @classmethod
    def from_env(cls, *, require_api_key: bool = True) -> "HuwiseConfig":
        """Load configuration from environment variables.

        For Automation API usage, API key authentication is required by default.
        The domain defaults to ``data.bs.ch`` when not set.
        Set ``require_api_key=False`` only for explicit unauthenticated scenarios.

        Returns:
            HuwiseConfig instance populated from environment.

        Raises:
            AppConfigError: If required environment variables are missing.
        """
        api_key = get_env_or_throw("HUWISE_API_KEY") if require_api_key else os.getenv("HUWISE_API_KEY")
        return cls(
            api_key=api_key,
            domain=os.getenv("HUWISE_DOMAIN", DEFAULT_HUWISE_DOMAIN),
            api_type=os.getenv("HUWISE_API_TYPE", "automation/v1.0"),
        )

    @property
    def base_url(self) -> str:
        """Construct the base API URL.

        Returns:
            The full base URL for API requests without trailing slash.
        """
        return f"https://{self.domain}/api/{self.api_type}"

    @property
    def headers(self) -> dict[str, str]:
        """Get authorization headers for API requests.

        Returns:
            Dictionary containing the Authorization header when api_key exists.
        """
        if self.api_key is None:
            return {}
        return {"Authorization": f"apikey {self.api_key}"}

    def __str__(self) -> str:
        """Return string representation with secrets masked."""
        api_key_repr = log_secret(self.api_key) if self.api_key else None
        return f"HuwiseConfig(domain={self.domain}, api_type={self.api_type}, api_key={api_key_repr})"
