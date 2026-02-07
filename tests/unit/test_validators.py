"""Unit tests for validators."""

from unittest.mock import MagicMock, patch

import pytest

from huwise_utils_py.utils.validators import validate_dataset_identifier


class TestValidateDatasetIdentifier:
    """Tests for validate_dataset_identifier function."""

    def test_validate_dataset_identifier_with_both_raises_value_error(self) -> None:
        """Test that providing both identifiers raises ValueError."""
        with pytest.raises(ValueError, match="mutually exclusive"):
            validate_dataset_identifier(dataset_id="123", dataset_uid="uid_123")

    def test_validate_dataset_identifier_with_neither_raises_value_error(self) -> None:
        """Test that providing neither identifier raises ValueError."""
        with pytest.raises(ValueError, match="must be specified"):
            validate_dataset_identifier()

    def test_validate_dataset_identifier_with_uid_returns_uid(self) -> None:
        """Test that providing only UID returns the UID."""
        uid = "da_test123"
        result = validate_dataset_identifier(dataset_uid=uid)
        assert result == uid

    def test_validate_dataset_identifier_with_id_resolves_to_uid(self) -> None:
        """Test that providing dataset_id resolves to UID."""
        with patch("huwise_utils_py.utils.validators.HttpClient") as mock_http:
            mock_client = MagicMock()
            mock_http.return_value = mock_client

            mock_response = MagicMock()
            mock_response.json.return_value = {"results": [{"uid": "da_resolved123"}]}
            mock_client.get.return_value = mock_response

            with patch("huwise_utils_py.utils.validators.HuwiseConfig") as mock_config:
                mock_config.from_env.return_value = MagicMock()

                result = validate_dataset_identifier(dataset_id="12345")

                assert result == "da_resolved123"

    def test_validate_dataset_identifier_with_empty_string_uid_returns_it(self) -> None:
        """Test that empty string UID is returned (validation is caller's responsibility)."""
        result = validate_dataset_identifier(dataset_uid="")
        assert result == ""

    def test_validate_dataset_identifier_with_custom_config_uses_it(self) -> None:
        """Test that custom config is used when provided."""
        from huwise_utils_py.config import HuwiseConfig

        custom_config = HuwiseConfig(
            api_key="custom-key",
            domain="custom.domain.com",
        )

        with patch("huwise_utils_py.utils.validators.HttpClient") as mock_http:
            mock_client = MagicMock()
            mock_http.return_value = mock_client

            mock_response = MagicMock()
            mock_response.json.return_value = {"results": [{"uid": "da_custom123"}]}
            mock_client.get.return_value = mock_response

            result = validate_dataset_identifier(
                dataset_id="12345",
                config=custom_config,
            )

            mock_http.assert_called_once_with(custom_config)
            assert result == "da_custom123"
