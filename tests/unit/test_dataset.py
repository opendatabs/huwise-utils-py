"""Unit tests for HuwiseDataset.

These tests use mocked responses based on real API response structures
captured from dataset ID 100522 (UID: da_tbcnel).
"""

from unittest.mock import MagicMock

from huwise_utils_py.config import HuwiseConfig
from huwise_utils_py.dataset import HuwiseDataset


class TestHuwiseDatasetCreation:
    """Tests for HuwiseDataset instantiation."""

    def test_huwise_dataset_with_uid_creates_instance(self, mock_config: HuwiseConfig) -> None:
        """Test that creating a dataset with UID works."""
        dataset = HuwiseDataset(uid="da_test123", config=mock_config)

        assert dataset.uid == "da_test123"
        assert dataset.config == mock_config

    def test_huwise_dataset_uid_format_accepted(self, mock_config: HuwiseConfig) -> None:
        """Test that standard UID format is accepted."""
        dataset = HuwiseDataset(uid="da_tbcnel", config=mock_config)

        assert dataset.uid == "da_tbcnel"


class TestHuwiseDatasetGetters:
    """Tests for HuwiseDataset getter methods."""

    def test_get_title_returns_title_from_default_template(
        self, mock_dataset: HuwiseDataset, sample_metadata: dict
    ) -> None:
        """Test that get_title extracts title from default template."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"metadata": sample_metadata}
        mock_dataset._client.get.return_value = mock_response

        title = mock_dataset.get_title()

        # Based on realistic fixture data
        assert title == "Test Dataset Title"

    def test_get_description_returns_description_with_html(
        self, mock_dataset: HuwiseDataset, sample_metadata: dict
    ) -> None:
        """Test that get_description returns description including HTML."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"metadata": sample_metadata}
        mock_dataset._client.get.return_value = mock_response

        description = mock_dataset.get_description()

        # Description includes HTML tags in real responses
        assert description == "<p>Test description with HTML</p>"

    def test_get_keywords_returns_list_from_metadata(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_keywords returns the keywords list."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"metadata": sample_metadata}
        mock_dataset._client.get.return_value = mock_response

        keywords = mock_dataset.get_keywords()

        # Based on realistic fixture data
        assert keywords == ["Test", "sample", "data"]

    def test_get_language_returns_language_code(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_language returns the language code."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"metadata": sample_metadata}
        mock_dataset._client.get.return_value = mock_response

        language = mock_dataset.get_language()

        assert language == "de"

    def test_get_publisher_returns_publisher_name(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_publisher returns the publisher name."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"metadata": sample_metadata}
        mock_dataset._client.get.return_value = mock_response

        publisher = mock_dataset.get_publisher()

        assert publisher == "DCC Data Competence Center"

    def test_get_metadata_returns_full_metadata_dict(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_metadata returns the full metadata dictionary."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"metadata": sample_metadata}
        mock_dataset._client.get.return_value = mock_response

        metadata = mock_dataset.get_metadata()

        # Verify all template sections are present
        assert "default" in metadata
        assert "dcat" in metadata
        assert "visualization" in metadata
        assert "internal" in metadata

    def test_get_license_returns_internal_license_id_when_set(
        self, mock_dataset: HuwiseDataset, sample_metadata: dict
    ) -> None:
        """Test that get_license returns internal.license_id (the canonical field)."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"metadata": sample_metadata}
        mock_dataset._client.get.return_value = mock_response

        license_value = mock_dataset.get_license()

        # sample_metadata has internal.license_id = "5sylls5"
        assert license_value == "5sylls5"

    def test_get_license_falls_back_to_default_license_string(self, mock_dataset: HuwiseDataset) -> None:
        """Test that get_license falls back to default.license when internal.license_id is missing."""
        metadata_without_internal_id = {
            "internal": {},
            "default": {
                "license": {"value": "CC BY"},
            },
        }
        mock_response = MagicMock()
        mock_response.json.return_value = {"metadata": metadata_without_internal_id}
        mock_dataset._client.get.return_value = mock_response

        license_value = mock_dataset.get_license()

        assert license_value == "CC BY"

    def test_get_license_prefers_internal_license_id_over_default_license(self, mock_dataset: HuwiseDataset) -> None:
        """Test that get_license prefers internal.license_id when both fields are set."""
        metadata_with_both = {
            "internal": {
                "license_id": {"value": "cc_by"},
            },
            "default": {
                "license": {"value": "CC BY"},
            },
        }
        mock_response = MagicMock()
        mock_response.json.return_value = {"metadata": metadata_with_both}
        mock_dataset._client.get.return_value = mock_response

        license_value = mock_dataset.get_license()

        assert license_value == "cc_by"

    def test_get_license_returns_none_when_neither_field_set(self, mock_dataset: HuwiseDataset) -> None:
        """Test that get_license returns None when no license fields are set."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"metadata": {"internal": {}, "default": {}}}
        mock_dataset._client.get.return_value = mock_response

        license_value = mock_dataset.get_license()

        assert license_value is None

    def test_get_title_returns_none_when_missing(self, mock_dataset: HuwiseDataset) -> None:
        """Test that get_title returns None when title is not set."""
        empty_metadata = {"default": {}}
        mock_response = MagicMock()
        mock_response.json.return_value = {"metadata": empty_metadata}
        mock_dataset._client.get.return_value = mock_response

        title = mock_dataset.get_title()

        assert title is None


class TestHuwiseDatasetSetters:
    """Tests for HuwiseDataset setter methods."""

    def test_set_title_returns_self_for_chaining(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that set_title returns self for method chaining."""
        # Setup mocks
        metadata_response = MagicMock()
        metadata_response.json.return_value = sample_metadata
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.side_effect = [metadata_response, status_response]
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        result = mock_dataset.set_title("New Title")

        assert result is mock_dataset

    def test_set_description_returns_self_for_chaining(
        self, mock_dataset: HuwiseDataset, sample_metadata: dict
    ) -> None:
        """Test that set_description returns self for method chaining."""
        metadata_response = MagicMock()
        metadata_response.json.return_value = sample_metadata
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.side_effect = [metadata_response, status_response]
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        result = mock_dataset.set_description("<p>New Description</p>")

        assert result is mock_dataset

    def test_set_keywords_returns_self_for_chaining(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that set_keywords returns self for method chaining."""
        metadata_response = MagicMock()
        metadata_response.json.return_value = sample_metadata
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.side_effect = [metadata_response, status_response]
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        result = mock_dataset.set_keywords(["new", "keywords"])

        assert result is mock_dataset

    def test_set_license_sets_default_license_id_and_default_license(
        self, mock_dataset: HuwiseDataset, sample_metadata: dict
    ) -> None:
        """Test that set_license writes default.license_id and default.license."""
        metadata_response = MagicMock()
        metadata_response.json.return_value = sample_metadata
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.side_effect = [metadata_response, status_response]
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        result = mock_dataset.set_license("5sylls5", license_name="CC BY 4.0")

        assert result is mock_dataset
        # Verify the PUT writes to default (writable), not internal (read-only)
        put_call_args = mock_dataset._client.put.call_args
        sent_metadata = put_call_args.kwargs["json"]
        assert sent_metadata["default"]["license_id"]["value"] == "5sylls5"
        assert sent_metadata["default"]["license"]["value"] == "CC BY 4.0"

    def test_set_license_without_name_only_sets_default_license_id(self, mock_dataset: HuwiseDataset) -> None:
        """Test that set_license without license_name only sets default.license_id."""
        metadata = {"internal": {}, "default": {"title": {"value": "Test"}}}
        metadata_response = MagicMock()
        metadata_response.json.return_value = metadata
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.side_effect = [metadata_response, status_response]
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        mock_dataset.set_license("5sylls5")

        put_call_args = mock_dataset._client.put.call_args
        sent_metadata = put_call_args.kwargs["json"]
        assert sent_metadata["default"]["license_id"]["value"] == "5sylls5"
        assert "license" not in sent_metadata["default"]


class TestHuwiseDatasetPublishing:
    """Tests for HuwiseDataset publish/unpublish methods."""

    def test_publish_calls_correct_endpoint(self, mock_dataset: HuwiseDataset) -> None:
        """Test that publish calls the correct API endpoint."""
        mock_dataset._client.post.return_value = MagicMock()

        mock_dataset.publish()

        mock_dataset._client.post.assert_called_once_with("/datasets/da_tbcnel/publish/")

    def test_unpublish_calls_correct_endpoint(self, mock_dataset: HuwiseDataset) -> None:
        """Test that unpublish calls the correct API endpoint."""
        mock_dataset._client.post.return_value = MagicMock()

        mock_dataset.unpublish()

        mock_dataset._client.post.assert_called_once_with("/datasets/da_tbcnel/unpublish/")

    def test_publish_returns_self_for_chaining(self, mock_dataset: HuwiseDataset) -> None:
        """Test that publish returns self for method chaining."""
        mock_dataset._client.post.return_value = MagicMock()

        result = mock_dataset.publish()

        assert result is mock_dataset

    def test_unpublish_returns_self_for_chaining(self, mock_dataset: HuwiseDataset) -> None:
        """Test that unpublish returns self for method chaining."""
        mock_dataset._client.post.return_value = MagicMock()

        result = mock_dataset.unpublish()

        assert result is mock_dataset


class TestHuwiseDatasetMethodChaining:
    """Tests for HuwiseDataset method chaining functionality."""

    def test_multiple_setters_can_be_chained(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that multiple setter methods can be chained."""
        # Setup mocks
        metadata_response = MagicMock()
        metadata_response.json.return_value = sample_metadata
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        def mock_get(endpoint, **kwargs):
            if "status" in endpoint:
                return status_response
            return metadata_response

        mock_dataset._client.get.side_effect = mock_get
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        result = (
            mock_dataset.set_title("Title", publish=False)
            .set_description("Description", publish=False)
            .set_keywords(["test"], publish=False)
            .publish()
        )

        assert result is mock_dataset

    def test_refresh_returns_self_for_chaining(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that refresh returns self for method chaining."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"metadata": sample_metadata}
        mock_dataset._client.get.return_value = mock_response

        result = mock_dataset.refresh()

        assert result is mock_dataset


class TestHuwiseDatasetStatusHandling:
    """Tests for dataset status handling (wait for idle)."""

    def test_wait_for_idle_polls_until_idle(self, mock_dataset: HuwiseDataset) -> None:
        """Test that _wait_for_idle polls status until idle."""
        # First call returns processing, second returns idle
        processing_response = MagicMock()
        processing_response.json.return_value = {"status": "processing"}
        idle_response = MagicMock()
        idle_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.side_effect = [processing_response, idle_response]

        # This should poll twice
        mock_dataset._wait_for_idle()

        assert mock_dataset._client.get.call_count == 2
