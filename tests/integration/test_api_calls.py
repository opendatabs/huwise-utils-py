"""Integration tests for API calls.

These tests make real API calls against dataset ID 100522 (UID: da_tbcnel).
Run manually with: uv run pytest tests/integration/ -v

Note: These tests require valid API credentials in environment variables:
    - HUWISE_API_KEY
    - HUWISE_DOMAIN
"""

import os

import pytest

# Test dataset constants
TEST_DATASET_ID = "100522"
TEST_DATASET_UID = "da_tbcnel"

# Skip all tests in this module if no API key is configured
pytestmark = pytest.mark.skipif(
    not os.getenv("HUWISE_API_KEY"),
    reason="HUWISE_API_KEY not set - skipping integration tests",
)


class TestConfigIntegration:
    """Integration tests for configuration."""

    def test_huwise_config_from_env_loads_successfully(self) -> None:
        """Test that config loads from environment successfully."""
        from huwise_utils_py import HuwiseConfig

        config = HuwiseConfig.from_env()

        assert config.api_key
        assert config.domain
        assert config.base_url.startswith("https://")

    def test_huwise_config_base_url_is_valid(self) -> None:
        """Test that base_url has correct format."""
        from huwise_utils_py import HuwiseConfig

        config = HuwiseConfig.from_env()

        assert "api" in config.base_url
        assert "automation" in config.base_url


class TestHttpClientIntegration:
    """Integration tests for HTTP client."""

    def test_http_client_can_make_basic_request(self) -> None:
        """Test that HTTP client can make a basic request."""
        from huwise_utils_py import HttpClient, HuwiseConfig

        config = HuwiseConfig.from_env()
        client = HttpClient(config)

        response = client.get("/datasets/?limit=1")

        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "total_count" in data

    def test_http_client_returns_correct_response_structure(self) -> None:
        """Test that datasets list response has expected structure."""
        from huwise_utils_py import HttpClient, HuwiseConfig

        config = HuwiseConfig.from_env()
        client = HttpClient(config)

        response = client.get("/datasets/?limit=1")
        data = response.json()

        assert isinstance(data["total_count"], int)
        assert isinstance(data["results"], list)
        if data["results"]:
            result = data["results"][0]
            assert "uid" in result
            assert "dataset_id" in result
            assert "is_published" in result


class TestDatasetInfoIntegration:
    """Integration tests for dataset information retrieval."""

    def test_get_number_of_datasets_returns_positive_int(self) -> None:
        """Test that get_number_of_datasets returns a positive integer."""
        from huwise_utils_py import get_number_of_datasets

        count = get_number_of_datasets()

        assert isinstance(count, int)
        assert count >= 0

    def test_get_all_dataset_ids_returns_list(self) -> None:
        """Test that get_all_dataset_ids returns a list of IDs."""
        from huwise_utils_py import get_all_dataset_ids

        ids = get_all_dataset_ids(max_datasets=5)

        assert isinstance(ids, list)
        assert len(ids) <= 5
        if ids:
            assert all(isinstance(id_, str) for id_ in ids)

    def test_get_uid_by_id_returns_valid_uid(self) -> None:
        """Test that get_uid_by_id returns correct UID for known dataset."""
        from huwise_utils_py import get_uid_by_id

        uid = get_uid_by_id(TEST_DATASET_ID)

        assert uid == TEST_DATASET_UID
        assert uid.startswith("da_")


class TestHuwiseDatasetGettersIntegration:
    """Integration tests for HuwiseDataset getter methods."""

    def test_huwise_dataset_from_id_with_known_dataset(self) -> None:
        """Test that HuwiseDataset.from_id works with known dataset ID."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset.from_id(TEST_DATASET_ID)

        assert dataset.uid == TEST_DATASET_UID

    def test_huwise_dataset_get_metadata_returns_dict(self) -> None:
        """Test that get_metadata returns a dictionary with expected templates."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)
        metadata = dataset.get_metadata()

        assert isinstance(metadata, dict)
        # Check for expected templates based on real response
        assert "default" in metadata
        assert "dcat" in metadata
        assert "visualization" in metadata

    def test_huwise_dataset_get_title_returns_string(self) -> None:
        """Test that get_title returns a string."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)
        title = dataset.get_title()

        assert isinstance(title, str)
        assert len(title) > 0

    def test_huwise_dataset_get_description_returns_string_or_none(self) -> None:
        """Test that get_description returns a string or None."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)
        description = dataset.get_description()

        assert description is None or isinstance(description, str)

    def test_huwise_dataset_get_keywords_returns_list(self) -> None:
        """Test that get_keywords returns a list."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)
        keywords = dataset.get_keywords()

        assert keywords is None or isinstance(keywords, list)
        if keywords:
            assert all(isinstance(k, str) for k in keywords)

    def test_huwise_dataset_get_language_returns_language_code(self) -> None:
        """Test that get_language returns a valid language code."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)
        language = dataset.get_language()

        assert language is None or isinstance(language, str)
        if language:
            assert len(language) == 2  # ISO 639-1 code

    def test_huwise_dataset_get_publisher_returns_string(self) -> None:
        """Test that get_publisher returns a string."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)
        publisher = dataset.get_publisher()

        assert publisher is None or isinstance(publisher, str)

    def test_huwise_dataset_metadata_contains_expected_templates(self) -> None:
        """Test that metadata contains all expected template sections."""
        from huwise_utils_py import HuwiseDataset

        dataset = HuwiseDataset(uid=TEST_DATASET_UID)
        metadata = dataset.get_metadata()

        # These templates were observed in real API responses
        expected_templates = ["default", "dcat", "visualization", "internal"]
        for template in expected_templates:
            assert template in metadata, f"Missing template: {template}"


class TestLegacyFunctionsIntegration:
    """Integration tests for function-based API."""

    def test_get_dataset_title_with_uid(self) -> None:
        """Test get_dataset_title with dataset_uid parameter."""
        from huwise_utils_py import get_dataset_title

        title = get_dataset_title(dataset_uid=TEST_DATASET_UID)

        assert isinstance(title, str)
        assert len(title) > 0

    def test_get_dataset_title_with_id(self) -> None:
        """Test get_dataset_title with dataset_id parameter."""
        from huwise_utils_py import get_dataset_title

        title = get_dataset_title(dataset_id=TEST_DATASET_ID)

        assert isinstance(title, str)
        assert len(title) > 0

    def test_get_dataset_description_with_uid(self) -> None:
        """Test get_dataset_description with dataset_uid parameter."""
        from huwise_utils_py import get_dataset_description

        description = get_dataset_description(dataset_uid=TEST_DATASET_UID)

        assert description is None or isinstance(description, str)

    def test_get_dataset_keywords_with_uid(self) -> None:
        """Test get_dataset_keywords with dataset_uid parameter."""
        from huwise_utils_py import get_dataset_keywords

        keywords = get_dataset_keywords(dataset_uid=TEST_DATASET_UID)

        assert keywords is None or isinstance(keywords, list)

    def test_get_dataset_metadata_with_uid(self) -> None:
        """Test get_dataset_metadata returns full metadata."""
        from huwise_utils_py import get_dataset_metadata

        metadata = get_dataset_metadata(dataset_uid=TEST_DATASET_UID)

        assert isinstance(metadata, dict)
        assert "default" in metadata
