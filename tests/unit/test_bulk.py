"""Unit tests for bulk operations.

These tests verify the dual-parameter support (dataset_ids / dataset_uids)
for bulk_get_metadata and bulk_get_metadata_async.
"""

from unittest.mock import MagicMock, patch

import pytest

from huwise_utils_py.bulk import bulk_get_metadata, bulk_get_metadata_async

# =============================================================================
# Helpers
# =============================================================================


def _make_uid_lookup_response(uid: str) -> MagicMock:
    """Create a mock response for a UID lookup by dataset ID."""
    response = MagicMock()
    response.json.return_value = {"results": [{"uid": uid}]}
    return response


def _make_dataset_response(metadata: dict | None = None) -> MagicMock:
    """Create a mock response for a dataset GET request."""
    response = MagicMock()
    response.json.return_value = {"metadata": metadata or {"default": {"title": {"value": "Test"}}}}
    return response


# =============================================================================
# Sync: bulk_get_metadata
# =============================================================================


class TestBulkGetMetadataValidation:
    """Tests for parameter validation in bulk_get_metadata."""

    def test_raises_if_both_ids_and_uids_provided(self) -> None:
        """Providing both dataset_ids and dataset_uids raises ValueError."""
        with pytest.raises(ValueError, match="mutually exclusive"):
            bulk_get_metadata(dataset_ids=["100123"], dataset_uids=["da_abc"])

    def test_raises_if_neither_ids_nor_uids_provided(self) -> None:
        """Providing neither dataset_ids nor dataset_uids raises ValueError."""
        with pytest.raises(ValueError, match="must be specified"):
            bulk_get_metadata()


class TestBulkGetMetadataWithUids:
    """Tests for bulk_get_metadata when called with dataset_uids."""

    @patch("huwise_utils_py.bulk.HttpClient")
    @patch("huwise_utils_py.bulk.HuwiseConfig")
    def test_returns_metadata_keyed_by_uid(self, mock_config_cls, mock_http_cls) -> None:
        """When dataset_uids is provided, result is keyed by UID."""
        mock_config_cls.from_env.return_value = MagicMock()
        mock_client = MagicMock()
        mock_http_cls.return_value = mock_client
        mock_client.get.return_value = _make_dataset_response()

        result = bulk_get_metadata(dataset_uids=["da_abc", "da_def"])

        assert "da_abc" in result
        assert "da_def" in result
        assert len(result) == 2


class TestBulkGetMetadataWithIds:
    """Tests for bulk_get_metadata when called with dataset_ids."""

    @patch("huwise_utils_py.bulk.HttpClient")
    @patch("huwise_utils_py.bulk.HuwiseConfig")
    def test_resolves_ids_and_returns_metadata_keyed_by_id(self, mock_config_cls, mock_http_cls) -> None:
        """When dataset_ids is provided, IDs are resolved and result is keyed by dataset ID."""
        mock_config_cls.from_env.return_value = MagicMock()
        mock_client = MagicMock()
        mock_http_cls.return_value = mock_client

        # First two calls resolve IDs -> UIDs, next two fetch metadata
        mock_client.get.side_effect = [
            _make_uid_lookup_response("da_resolved1"),
            _make_uid_lookup_response("da_resolved2"),
            _make_dataset_response(),
            _make_dataset_response(),
        ]

        result = bulk_get_metadata(dataset_ids=["100123", "100456"])

        assert "100123" in result
        assert "100456" in result
        assert len(result) == 2


# =============================================================================
# Async: bulk_get_metadata_async
# =============================================================================


class TestBulkGetMetadataAsyncValidation:
    """Tests for parameter validation in bulk_get_metadata_async."""

    @pytest.mark.asyncio
    async def test_raises_if_both_ids_and_uids_provided(self) -> None:
        """Providing both dataset_ids and dataset_uids raises ValueError."""
        with pytest.raises(ValueError, match="mutually exclusive"):
            await bulk_get_metadata_async(dataset_ids=["100123"], dataset_uids=["da_abc"])

    @pytest.mark.asyncio
    async def test_raises_if_neither_ids_nor_uids_provided(self) -> None:
        """Providing neither dataset_ids nor dataset_uids raises ValueError."""
        with pytest.raises(ValueError, match="must be specified"):
            await bulk_get_metadata_async()
