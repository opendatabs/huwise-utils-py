"""Integration tests for bulk operations.

These tests make real API calls and require valid credentials.
Run manually with: uv run pytest tests/integration/ -v
"""

import os

import pytest

# Skip all tests in this module if no API key is configured
pytestmark = pytest.mark.skipif(
    not os.getenv("HUWISE_API_KEY"),
    reason="HUWISE_API_KEY not set - skipping integration tests",
)


class TestBulkOperationsIntegration:
    """Integration tests for bulk operations."""

    def test_bulk_get_metadata_returns_dict(self) -> None:
        """Test that bulk_get_metadata returns a dictionary of metadata."""
        from huwise_utils_py import bulk_get_metadata, get_all_dataset_ids

        # Get first few dataset IDs to test with
        ids = get_all_dataset_ids(max_datasets=3)
        if not ids:
            pytest.skip("No datasets available for testing")

        # Need to convert IDs to UIDs - use the dataset class
        from huwise_utils_py import HuwiseDataset

        uids = []
        for dataset_id in ids[:2]:  # Just test with 2
            dataset = HuwiseDataset.from_id(dataset_id)
            uids.append(dataset.uid)

        if not uids:
            pytest.skip("Could not resolve any UIDs")

        metadata = bulk_get_metadata(uids)

        assert isinstance(metadata, dict)
        assert len(metadata) == len(uids)

    @pytest.mark.asyncio
    async def test_bulk_get_metadata_async_returns_dict(self) -> None:
        """Test that bulk_get_metadata_async returns a dictionary of metadata."""
        from huwise_utils_py import HuwiseDataset, bulk_get_metadata_async, get_all_dataset_ids

        # Get first few dataset IDs to test with
        ids = get_all_dataset_ids(max_datasets=3)
        if not ids:
            pytest.skip("No datasets available for testing")

        # Resolve to UIDs
        uids = []
        for dataset_id in ids[:2]:
            dataset = HuwiseDataset.from_id(dataset_id)
            uids.append(dataset.uid)

        if not uids:
            pytest.skip("Could not resolve any UIDs")

        metadata = await bulk_get_metadata_async(uids)

        assert isinstance(metadata, dict)
        assert len(metadata) == len(uids)

    def test_bulk_get_dataset_ids_returns_list(self) -> None:
        """Test that bulk_get_dataset_ids returns a list."""
        from huwise_utils_py import bulk_get_dataset_ids

        ids = bulk_get_dataset_ids(max_datasets=5)

        assert isinstance(ids, list)
        assert len(ids) <= 5

    @pytest.mark.asyncio
    async def test_bulk_get_dataset_ids_async_returns_list(self) -> None:
        """Test that bulk_get_dataset_ids_async returns a list."""
        from huwise_utils_py import bulk_get_dataset_ids_async

        ids = await bulk_get_dataset_ids_async(max_datasets=5)

        assert isinstance(ids, list)
        assert len(ids) <= 5
