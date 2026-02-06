"""Unit tests for HuwiseConfig."""

import os
from unittest.mock import patch

from huwise_utils_py.config import HuwiseConfig


class TestHuwiseConfig:
    """Tests for HuwiseConfig class."""

    def test_huwise_config_with_valid_values_creates_instance(self) -> None:
        """Test that valid values create a config instance."""
        config = HuwiseConfig(
            api_key="test-key",
            domain="data.example.com",
            api_type="automation/v1.0",
        )

        assert config.api_key == "test-key"
        assert config.domain == "data.example.com"
        assert config.api_type == "automation/v1.0"

    def test_huwise_config_base_url_formats_correctly(self) -> None:
        """Test that base_url property formats correctly."""
        config = HuwiseConfig(
            api_key="test-key",
            domain="data.example.com",
            api_type="automation/v1.0",
        )

        assert config.base_url == "https://data.example.com/api/automation/v1.0"

    def test_huwise_config_headers_contains_authorization(self) -> None:
        """Test that headers property contains correct authorization."""
        config = HuwiseConfig(
            api_key="my-secret-key",
            domain="data.example.com",
            api_type="automation/v1.0",
        )

        assert config.headers == {"Authorization": "apikey my-secret-key"}

    def test_huwise_config_str_masks_api_key(self) -> None:
        """Test that string representation masks the API key."""
        config = HuwiseConfig(
            api_key="my-secret-key-12345",
            domain="data.example.com",
            api_type="automation/v1.0",
        )

        str_repr = str(config)
        assert "data.example.com" in str_repr
        assert "my-secret-key-12345" not in str_repr

    @patch.dict(
        os.environ,
        {
            "HUWISE_API_KEY": "env-api-key",
            "HUWISE_DOMAIN": "env.domain.com",
            "HUWISE_API_TYPE": "automation/v2.0",
        },
    )
    def test_huwise_config_from_env_loads_all_variables(self) -> None:
        """Test that from_env loads all environment variables."""
        config = HuwiseConfig.from_env()

        assert config.api_key == "env-api-key"
        assert config.domain == "env.domain.com"
        assert config.api_type == "automation/v2.0"

    @patch.dict(
        os.environ,
        {
            "HUWISE_API_KEY": "env-api-key",
            "HUWISE_DOMAIN": "env.domain.com",
        },
        clear=True,
    )
    def test_huwise_config_from_env_uses_default_api_type(self) -> None:
        """Test that from_env uses default api_type when not set."""
        # Need to clear HUWISE_API_TYPE if it exists
        os.environ.pop("HUWISE_API_TYPE", None)

        config = HuwiseConfig.from_env()

        assert config.api_type == "automation/v1.0"

    def test_huwise_config_default_api_type_is_automation_v1(self) -> None:
        """Test that default api_type is automation/v1.0."""
        config = HuwiseConfig(
            api_key="test-key",
            domain="data.example.com",
        )

        assert config.api_type == "automation/v1.0"
