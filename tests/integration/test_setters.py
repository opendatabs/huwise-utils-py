"""Integration tests for setter methods.

These tests make real API calls and modify dataset 100522 (UID: da_tbcnel).
Each test stores the original value, modifies it, verifies the change,
then restores the original value.

Run manually with: uv run pytest tests/integration/test_setters.py -v

Warning: These tests modify real data. They attempt to restore original values,
but failures during restoration could leave the dataset in a modified state.

Note: These tests require valid API credentials in environment variables:
    - HUWISE_API_KEY
    - HUWISE_DOMAIN
"""

import os
import time

import pytest

# Test dataset constants
TEST_DATASET_ID = "100522"
TEST_DATASET_UID = "da_tbcnel"

# Skip all tests in this module if no API key is configured
pytestmark = pytest.mark.skipif(
    not os.getenv("HUWISE_API_KEY"),
    reason="HUWISE_API_KEY not set - skipping integration tests",
)


class TestHuwiseDatasetSettersIntegration:
    """Integration tests for HuwiseDataset setter methods with restore logic."""

    def test_set_dataset_title_updates_and_restores(self) -> None:
        """Test that set_title updates the title and can be restored."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)

        # Store original
        original_title = dataset.get_title()

        try:
            # Update
            test_title = "Integration Test - set_title - " + str(int(time.time()))
            dataset.set_title(test_title, publish=False)

            # Verify change
            new_title = dataset.get_title()
            assert new_title == test_title
            assert new_title != original_title

        finally:
            # Restore
            dataset.set_title(original_title, publish=True)
            restored_title = dataset.get_title()
            assert restored_title == original_title

    def test_set_dataset_description_updates_and_restores(self) -> None:
        """Test that set_description updates the description and can be restored."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)

        # Store original
        original_description = dataset.get_description()

        try:
            # Update with test description (preserving required notice)
            test_description = (
                "<p>==========================<br>"
                "Dieser Teil der Beschreibung muss zwingend bestehen bleiben. "
                "Dieser Datensatz dient dazu, dass das Paket "
                '<a href="https://github.com/opendatabs/huwise-utils-py">huwise-utils-py</a> '
                "getestet werden kann.<br>"
                "==========================</p>"
                f"<p>Integration test timestamp: {int(time.time())}</p>"
            )
            dataset.set_description(test_description, publish=False)

            # Verify change
            new_description = dataset.get_description()
            assert "Integration test timestamp" in new_description

        finally:
            # Restore
            if original_description:
                dataset.set_description(original_description, publish=True)

    def test_set_dataset_keywords_updates_and_restores(self) -> None:
        """Test that set_keywords updates the keywords and can be restored."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)

        # Store original
        original_keywords = dataset.get_keywords() or []

        try:
            # Update
            test_keywords = ["integration", "test", f"timestamp-{int(time.time())}"]
            dataset.set_keywords(test_keywords, publish=False)

            # Verify change
            new_keywords = dataset.get_keywords()
            assert set(new_keywords) == set(test_keywords)

        finally:
            # Restore
            dataset.set_keywords(original_keywords, publish=True)
            restored_keywords = dataset.get_keywords()
            assert set(restored_keywords) == set(original_keywords)

    def test_set_dataset_publisher_updates_and_restores(self) -> None:
        """Test that set_publisher updates the publisher and can be restored."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)

        # Store original
        original_publisher = dataset.get_publisher()

        try:
            # Update
            test_publisher = f"Integration Test Publisher {int(time.time())}"
            dataset.set_publisher(test_publisher, publish=False)

            # Verify change
            new_publisher = dataset.get_publisher()
            assert new_publisher == test_publisher

        finally:
            # Restore
            if original_publisher:
                dataset.set_publisher(original_publisher, publish=True)
                restored_publisher = dataset.get_publisher()
                assert restored_publisher == original_publisher


class TestMethodChainingIntegration:
    """Integration tests for method chaining."""

    def test_method_chaining_multiple_fields(self) -> None:
        """Test that method chaining works correctly with multiple fields."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)

        # Store originals
        original_title = dataset.get_title()
        original_keywords = dataset.get_keywords() or []

        try:
            # Chain multiple operations
            test_title = f"Chained Test Title {int(time.time())}"
            test_keywords = ["chained", "test", "keywords"]

            result = dataset.set_title(test_title, publish=False).set_keywords(test_keywords, publish=False).publish()

            # Verify chaining returns self
            assert result is dataset

            # Verify changes
            assert dataset.get_title() == test_title
            assert set(dataset.get_keywords()) == set(test_keywords)

        finally:
            # Restore using chaining
            dataset.set_title(original_title, publish=False).set_keywords(original_keywords, publish=True)

    def test_method_chaining_returns_self(self) -> None:
        """Test that all setter methods return self for chaining."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)

        # Store original
        original_title = dataset.get_title()

        try:
            # Each setter should return the dataset instance
            result = dataset.set_title(original_title, publish=False)
            assert result is dataset

        finally:
            # Ensure we publish to restore clean state
            dataset.publish()


class TestPublishWorkflowIntegration:
    """Integration tests for publish/unpublish workflow."""

    def test_publish_after_modifications(self) -> None:
        """Test that publish works after modifications."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)

        # Store original
        original_title = dataset.get_title()

        try:
            # Make modification without publishing
            test_title = f"Unpublished Test {int(time.time())}"
            dataset.set_title(test_title, publish=False)

            # Explicitly publish
            result = dataset.publish()
            assert result is dataset

            # Verify title is still there after publish
            assert dataset.get_title() == test_title

        finally:
            # Restore
            dataset.set_title(original_title, publish=True)

    def test_refresh_fetches_latest_data(self) -> None:
        """Test that refresh method fetches latest data."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)

        # Get metadata
        metadata1 = dataset.get_metadata()

        # Refresh and get again
        result = dataset.refresh()
        metadata2 = dataset.get_metadata()

        # Verify refresh returns self
        assert result is dataset

        # Verify metadata is fetched (structure should be same)
        assert "default" in metadata1
        assert "default" in metadata2


class TestLegacySetterFunctionsIntegration:
    """Integration tests for function-based setter API."""

    def test_set_dataset_title_function(self) -> None:
        """Test set_dataset_title function works correctly."""
        from huwise_utils_py import get_dataset_title, set_dataset_title

        # Store original
        original_title = get_dataset_title(dataset_uid=TEST_DATASET_UID)

        try:
            # Update
            test_title = f"Function Test Title {int(time.time())}"
            set_dataset_title(test_title, dataset_uid=TEST_DATASET_UID, publish=False)

            # Verify
            new_title = get_dataset_title(dataset_uid=TEST_DATASET_UID)
            assert new_title == test_title

        finally:
            # Restore
            set_dataset_title(original_title, dataset_uid=TEST_DATASET_UID, publish=True)

    def test_set_dataset_keywords_function(self) -> None:
        """Test set_dataset_keywords function works correctly."""
        from huwise_utils_py import get_dataset_keywords, set_dataset_keywords

        # Store original
        original_keywords = get_dataset_keywords(dataset_uid=TEST_DATASET_UID) or []

        try:
            # Update
            test_keywords = ["function", "test", f"ts-{int(time.time())}"]
            set_dataset_keywords(test_keywords, dataset_uid=TEST_DATASET_UID, publish=False)

            # Verify
            new_keywords = get_dataset_keywords(dataset_uid=TEST_DATASET_UID)
            assert set(new_keywords) == set(test_keywords)

        finally:
            # Restore
            set_dataset_keywords(original_keywords, dataset_uid=TEST_DATASET_UID, publish=True)
