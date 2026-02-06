"""Configuration management for Huwise API access.

This module provides a Pydantic-based configuration class for managing
Huwise API credentials and settings, following DCC coding standards.
"""

import os
from typing import override

from dcc_backend_common.config import AbstractAppConfig, get_env_or_throw, log_secret
from pydantic import Field


class HuwiseConfig(AbstractAppConfig):
    """Configuration for Huwise API access.

    Provides type-safe configuration management with environment variable loading
    and supports dependency injection patterns.

    Attributes:
        api_key: API key for Huwise authentication.
        domain: Huwise domain (e.g., data.bs.ch).
        api_type: API version/type (defaults to automation/v1.0).

    Example:
        >>> config = HuwiseConfig.from_env()
        >>> print(config.base_url)
        'https://data.bs.ch/api/automation/v1.0'
    """

    api_key: str = Field(description="API key for Huwise authentication")
    domain: str = Field(description="Huwise domain (e.g., data.bs.ch)")
    api_type: str = Field(default="automation/v1.0", description="API version/type")

    @classmethod
    @override
    def from_env(cls) -> "HuwiseConfig":
        """Load configuration from environment variables.

        Returns:
            HuwiseConfig instance populated from environment.

        Raises:
            AppConfigError: If required environment variables are missing.
        """
        return cls(
            api_key=get_env_or_throw("HUWISE_API_KEY"),
            domain=get_env_or_throw("HUWISE_DOMAIN"),
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
            Dictionary containing the Authorization header.
        """
        return {"Authorization": f"apikey {self.api_key}"}

    @override
    def __str__(self) -> str:
        """Return string representation with secrets masked."""
        return f"HuwiseConfig(domain={self.domain}, api_type={self.api_type}, api_key={log_secret(self.api_key)})"
