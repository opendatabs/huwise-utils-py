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
    """Tests for HuwiseDataset getter methods.

    Getter helpers now use the per-template endpoint
    ``GET /datasets/{uid}/metadata/{template}/`` which returns just the
    template dict, not the full dataset.
    """

    def test_get_title_returns_title_from_default_template(
        self, mock_dataset: HuwiseDataset, sample_metadata: dict
    ) -> None:
        """Test that get_title extracts title from default template."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["default"]
        mock_dataset._client.get.return_value = mock_response

        title = mock_dataset.get_title()

        assert title == "Test Dataset Title"

    def test_get_description_returns_description_with_html(
        self, mock_dataset: HuwiseDataset, sample_metadata: dict
    ) -> None:
        """Test that get_description returns description including HTML."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["default"]
        mock_dataset._client.get.return_value = mock_response

        description = mock_dataset.get_description()

        assert description == "<p>Test description with HTML</p>"

    def test_get_keywords_returns_list_from_metadata(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_keywords returns the keywords list."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["default"]
        mock_dataset._client.get.return_value = mock_response

        keywords = mock_dataset.get_keywords()

        assert keywords == ["Test", "sample", "data"]

    def test_get_language_returns_language_code(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_language returns the language code."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["default"]
        mock_dataset._client.get.return_value = mock_response

        language = mock_dataset.get_language()

        assert language == "de"

    def test_get_publisher_returns_publisher_name(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_publisher returns the publisher name."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["default"]
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
        mock_response.json.return_value = sample_metadata["internal"]
        mock_dataset._client.get.return_value = mock_response

        license_value = mock_dataset.get_license()

        assert license_value == "5sylls5"

    def test_get_license_falls_back_to_default_license_string(self, mock_dataset: HuwiseDataset) -> None:
        """Test that get_license falls back to default.license when internal.license_id is missing."""
        internal_response = MagicMock()
        internal_response.json.return_value = {}  # no license_id
        default_response = MagicMock()
        default_response.json.return_value = {"license": {"value": "CC BY"}}

        mock_dataset._client.get.side_effect = [internal_response, default_response]

        license_value = mock_dataset.get_license()

        assert license_value == "CC BY"

    def test_get_license_prefers_internal_license_id_over_default_license(self, mock_dataset: HuwiseDataset) -> None:
        """Test that get_license prefers internal.license_id when both fields are set."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"license_id": {"value": "cc_by"}}
        mock_dataset._client.get.return_value = mock_response

        license_value = mock_dataset.get_license()

        assert license_value == "cc_by"

    def test_get_license_returns_none_when_neither_field_set(self, mock_dataset: HuwiseDataset) -> None:
        """Test that get_license returns None when no license fields are set."""
        empty_internal = MagicMock()
        empty_internal.json.return_value = {}
        empty_default = MagicMock()
        empty_default.json.return_value = {}

        mock_dataset._client.get.side_effect = [empty_internal, empty_default]

        license_value = mock_dataset.get_license()

        assert license_value is None

    def test_get_title_returns_none_when_missing(self, mock_dataset: HuwiseDataset) -> None:
        """Test that get_title returns None when title is not set."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_dataset._client.get.return_value = mock_response

        title = mock_dataset.get_title()

        assert title is None


class TestHuwiseDatasetNewGetters:
    """Tests for the new HuwiseDataset getter methods."""

    def test_get_dcat_ap_ch_rights_returns_rights_string(
        self, mock_dataset: HuwiseDataset, sample_metadata: dict
    ) -> None:
        """Test that get_dcat_ap_ch_rights extracts rights from dcat_ap_ch template."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["dcat_ap_ch"]
        mock_dataset._client.get.return_value = mock_response

        result = mock_dataset.get_dcat_ap_ch_rights()

        assert result == "NonCommercialAllowed-CommercialAllowed-ReferenceNotRequired"

    def test_get_dcat_ap_ch_license_returns_license_code(
        self, mock_dataset: HuwiseDataset, sample_metadata: dict
    ) -> None:
        """Test that get_dcat_ap_ch_license extracts license from dcat_ap_ch template."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["dcat_ap_ch"]
        mock_dataset._client.get.return_value = mock_response

        result = mock_dataset.get_dcat_ap_ch_license()

        assert result == "terms_open"

    def test_get_created_returns_iso_datetime(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_created extracts created date from dcat template."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["dcat"]
        mock_dataset._client.get.return_value = mock_response

        result = mock_dataset.get_created()

        assert result == "2026-02-06T15:09:51Z"

    def test_get_issued_returns_published_date(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_issued extracts issued date from dcat template."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["dcat"]
        mock_dataset._client.get.return_value = mock_response

        result = mock_dataset.get_issued()

        assert result == "2026-02-06"

    def test_get_creator_returns_creator_name(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_creator extracts creator from dcat template."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["dcat"]
        mock_dataset._client.get.return_value = mock_response

        result = mock_dataset.get_creator()

        assert result == "DCC Data Competence Center"

    def test_get_contributor_returns_contributor_name(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_contributor extracts contributor from dcat template."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["dcat"]
        mock_dataset._client.get.return_value = mock_response

        result = mock_dataset.get_contributor()

        assert result == "Open Data Basel-Stadt"

    def test_get_contact_name_returns_contact_name(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_contact_name extracts contact name from dcat template."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["dcat"]
        mock_dataset._client.get.return_value = mock_response

        result = mock_dataset.get_contact_name()

        assert result == "Open Data Basel-Stadt"

    def test_get_contact_email_returns_email(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_contact_email extracts contact email from dcat template."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["dcat"]
        mock_dataset._client.get.return_value = mock_response

        result = mock_dataset.get_contact_email()

        assert result == "opendata@bs.ch"

    def test_get_accrualperiodicity_returns_frequency_uri(
        self, mock_dataset: HuwiseDataset, sample_metadata: dict
    ) -> None:
        """Test that get_accrualperiodicity extracts frequency URI from dcat template."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["dcat"]
        mock_dataset._client.get.return_value = mock_response

        result = mock_dataset.get_accrualperiodicity()

        assert result == "http://publications.europa.eu/resource/authority/frequency/IRREG"

    def test_get_relation_returns_url(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_relation extracts relation URL from dcat template."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["dcat"]
        mock_dataset._client.get.return_value = mock_response

        result = mock_dataset.get_relation()

        assert result == "https://example.com/related-dataset"

    def test_get_modified_returns_modified_date(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_modified extracts modified date from default template."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["default"]
        mock_dataset._client.get.return_value = mock_response

        result = mock_dataset.get_modified()

        assert result == "2026-02-06T14:56:31Z"

    def test_get_geographic_reference_returns_list(self, mock_dataset: HuwiseDataset, sample_metadata: dict) -> None:
        """Test that get_geographic_reference extracts reference codes from default template."""
        mock_response = MagicMock()
        mock_response.json.return_value = sample_metadata["default"]
        mock_dataset._client.get.return_value = mock_response

        result = mock_dataset.get_geographic_reference()

        assert result == ["ch_40_12"]

    def test_get_issued_returns_none_when_not_set(self, mock_dataset: HuwiseDataset) -> None:
        """Test that get_issued returns None when issued date is not set."""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_dataset._client.get.return_value = mock_response

        result = mock_dataset.get_issued()

        assert result is None


class TestHuwiseDatasetSetters:
    """Tests for HuwiseDataset setter methods.

    Setter helpers now use the per-field endpoint
    ``PUT /datasets/{uid}/metadata/{template}/{field}/`` which only needs
    a status GET (for ``_wait_for_idle``) followed by the per-field PUT.
    """

    def test_set_title_returns_self_for_chaining(self, mock_dataset: HuwiseDataset) -> None:
        """Test that set_title returns self for method chaining."""
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.return_value = status_response
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        result = mock_dataset.set_title("New Title")

        assert result is mock_dataset
        mock_dataset._client.put.assert_called_once_with(
            "/datasets/da_tbcnel/metadata/default/title/",
            json={"value": "New Title"},
        )

    def test_set_description_returns_self_for_chaining(self, mock_dataset: HuwiseDataset) -> None:
        """Test that set_description returns self for method chaining."""
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.return_value = status_response
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        result = mock_dataset.set_description("<p>New Description</p>")

        assert result is mock_dataset
        mock_dataset._client.put.assert_called_once_with(
            "/datasets/da_tbcnel/metadata/default/description/",
            json={"value": "<p>New Description</p>"},
        )

    def test_set_keywords_returns_self_for_chaining(self, mock_dataset: HuwiseDataset) -> None:
        """Test that set_keywords returns self for method chaining."""
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.return_value = status_response
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        result = mock_dataset.set_keywords(["new", "keywords"])

        assert result is mock_dataset
        mock_dataset._client.put.assert_called_once_with(
            "/datasets/da_tbcnel/metadata/default/keyword/",
            json={"value": ["new", "keywords"]},
        )

    def test_set_license_sets_default_license_id_and_default_license(self, mock_dataset: HuwiseDataset) -> None:
        """Test that set_license issues per-field PUTs for license_id and license."""
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.return_value = status_response
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        result = mock_dataset.set_license("5sylls5", license_name="CC BY 4.0")

        assert result is mock_dataset
        # Verify two per-field PUT calls
        assert mock_dataset._client.put.call_count == 2
        put_calls = mock_dataset._client.put.call_args_list
        assert put_calls[0] == (
            ("/datasets/da_tbcnel/metadata/default/license_id/",),
            {"json": {"value": "5sylls5"}},
        )
        assert put_calls[1] == (
            ("/datasets/da_tbcnel/metadata/default/license/",),
            {"json": {"value": "CC BY 4.0"}},
        )

    def test_set_license_without_name_only_sets_default_license_id(self, mock_dataset: HuwiseDataset) -> None:
        """Test that set_license without license_name only PUTs license_id."""
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.return_value = status_response
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        mock_dataset.set_license("5sylls5")

        # Only one PUT for license_id, none for license
        mock_dataset._client.put.assert_called_once_with(
            "/datasets/da_tbcnel/metadata/default/license_id/",
            json={"value": "5sylls5"},
        )


class TestHuwiseDatasetNewSetters:
    """Tests for the new HuwiseDataset setter methods.

    All setters now use per-field PUT endpoints.
    """

    def test_set_modified_sets_date_and_flags(self, mock_dataset: HuwiseDataset) -> None:
        """Test that set_modified issues per-field PUTs for date and both flags."""
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.return_value = status_response
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        result = mock_dataset.set_modified(
            "2026-03-01T10:00:00Z",
            updates_on_metadata_change=True,
            updates_on_data_change=False,
        )

        assert result is mock_dataset
        # Three per-field PUTs: modified, metadata_change flag, data_change flag
        assert mock_dataset._client.put.call_count == 3
        put_calls = mock_dataset._client.put.call_args_list
        assert put_calls[0] == (
            ("/datasets/da_tbcnel/metadata/default/modified/",),
            {"json": {"value": "2026-03-01T10:00:00Z"}},
        )
        assert put_calls[1] == (
            ("/datasets/da_tbcnel/metadata/default/modified_updates_on_metadata_change/",),
            {"json": {"value": True}},
        )
        assert put_calls[2] == (
            ("/datasets/da_tbcnel/metadata/default/modified_updates_on_data_change/",),
            {"json": {"value": False}},
        )

    def test_set_modified_without_flags_only_sets_date(self, mock_dataset: HuwiseDataset) -> None:
        """Test that set_modified without flags only PUTs the modified date."""
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.return_value = status_response
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        mock_dataset.set_modified("2026-03-01T10:00:00Z")

        # Only one PUT for modified date, no flag PUTs
        mock_dataset._client.put.assert_called_once_with(
            "/datasets/da_tbcnel/metadata/default/modified/",
            json={"value": "2026-03-01T10:00:00Z"},
        )

    def test_set_dcat_ap_ch_rights_returns_self(self, mock_dataset: HuwiseDataset) -> None:
        """Test that set_dcat_ap_ch_rights returns self for method chaining."""
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.return_value = status_response
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        result = mock_dataset.set_dcat_ap_ch_rights("NonCommercialAllowed-CommercialAllowed-ReferenceRequired")

        assert result is mock_dataset
        mock_dataset._client.put.assert_called_once_with(
            "/datasets/da_tbcnel/metadata/dcat_ap_ch/rights/",
            json={"value": "NonCommercialAllowed-CommercialAllowed-ReferenceRequired"},
        )

    def test_set_geographic_reference_returns_self(self, mock_dataset: HuwiseDataset) -> None:
        """Test that set_geographic_reference returns self for method chaining."""
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.return_value = status_response
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        result = mock_dataset.set_geographic_reference(["ch_80_2477"])

        assert result is mock_dataset
        mock_dataset._client.put.assert_called_once_with(
            "/datasets/da_tbcnel/metadata/default/geographic_reference/",
            json={"value": ["ch_80_2477"]},
        )

    def test_new_setters_can_be_chained(self, mock_dataset: HuwiseDataset) -> None:
        """Test that new setters can be chained together."""
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.return_value = status_response
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        result = (
            mock_dataset.set_dcat_ap_ch_rights(
                "NonCommercialAllowed-CommercialAllowed-ReferenceRequired",
                publish=False,
            )
            .set_dcat_ap_ch_license("terms_by", publish=False)
            .set_creator("Test Creator", publish=False)
            .set_contact_email("test@example.com", publish=False)
            .publish()
        )

        assert result is mock_dataset
        # 4 per-field PUTs (one per setter with publish=False)
        assert mock_dataset._client.put.call_count == 4


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

    def test_multiple_setters_can_be_chained(self, mock_dataset: HuwiseDataset) -> None:
        """Test that multiple setter methods can be chained."""
        status_response = MagicMock()
        status_response.json.return_value = {"status": "idle"}

        mock_dataset._client.get.return_value = status_response
        mock_dataset._client.put.return_value = MagicMock()
        mock_dataset._client.post.return_value = MagicMock()

        result = (
            mock_dataset.set_title("Title", publish=False)
            .set_description("Description", publish=False)
            .set_keywords(["test"], publish=False)
            .publish()
        )

        assert result is mock_dataset
        # 3 per-field PUTs (one per setter with publish=False)
        assert mock_dataset._client.put.call_count == 3

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
