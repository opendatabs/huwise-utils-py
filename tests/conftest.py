"""Pytest configuration and fixtures for huwise_utils_py tests.

This module provides shared fixtures for both unit and integration tests.
Unit tests use mock configurations; integration tests use real API credentials.

Fixtures are based on real API responses from dataset ID 100522 (UID: da_tbcnel).
"""

from unittest.mock import MagicMock, patch

import pytest

from huwise_utils_py.config import HuwiseConfig
from huwise_utils_py.dataset import HuwiseDataset

# =============================================================================
# Test Dataset Constants
# =============================================================================

TEST_DATASET_ID = "100522"
TEST_DATASET_UID = "da_tbcnel"


# =============================================================================
# Configuration Fixtures
# =============================================================================


@pytest.fixture
def mock_config() -> HuwiseConfig:
    """Provide a test configuration without real credentials.

    Returns:
        HuwiseConfig instance with test values.
    """
    return HuwiseConfig(
        api_key="test-api-key-12345",
        domain="test.huwise.example.com",
        api_type="automation/v1.0",
    )


@pytest.fixture
def mock_client(mock_config: HuwiseConfig):
    """Provide a mocked HTTP client.

    Args:
        mock_config: Test configuration fixture.

    Returns:
        Mocked HttpClient instance.
    """
    with patch("huwise_utils_py.http.HttpClient") as mock_http:
        mock_instance = MagicMock()
        mock_http.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_dataset(mock_config: HuwiseConfig, mock_client) -> HuwiseDataset:
    """Provide a mocked HuwiseDataset for testing.

    Args:
        mock_config: Test configuration fixture.
        mock_client: Mocked HTTP client fixture.

    Returns:
        HuwiseDataset instance with mocked dependencies.
    """
    with patch.object(HuwiseDataset, "__post_init__"):
        dataset = HuwiseDataset(uid=TEST_DATASET_UID, config=mock_config)
        dataset._client = mock_client
        return dataset


# =============================================================================
# API Response Fixtures (based on real responses)
# =============================================================================


@pytest.fixture
def sample_metadata() -> dict:
    """Provide sample metadata matching real API response structure.

    Based on actual response from dataset da_tbcnel (ID: 100522).

    Returns:
        Dictionary mimicking real API metadata response.
    """
    return {
        "visualization": {
            "analyze_disabled": {"value": False},
            "map_disabled": {"value": False},
            "map_marker_hidemarkershape": {"value": False},
            "map_tooltip_disabled": {"value": False},
            "map_tooltip_html_enabled": {"value": False},
            "images_disabled": {"value": False},
            "image_tooltip_html_enabled": {"value": False},
            "calendar_enabled": {"value": False},
            "calendar_tooltip_html_enabled": {"value": False},
            "custom_view_enabled": {"value": False},
        },
        "dcat_ap_ch": {
            "rights": {"value": "NonCommercialAllowed-CommercialAllowed-ReferenceNotRequired"},
            "license": {"value": "terms_open"},
        },
        "dcat": {
            "created": {"value": "2026-02-06T15:09:51Z"},
            "creator": {"value": "DCC Data Competence Center"},
            "contributor": {"value": "Open Data Basel-Stadt"},
            "contact_name": {"value": "Open Data Basel-Stadt"},
            "contact_email": {"value": "opendata@bs.ch"},
            "accrualperiodicity": {"value": "http://publications.europa.eu/resource/authority/frequency/IRREG"},
        },
        "internal": {
            "category_id": {"value": "data"},
            "metadata_source_language": {"value": "de"},
            "license_id": {"value": "5sylls5"},
            "theme_id": {"value": ["7b5b405", "06af88d"]},
            "draft": {"value": False},
        },
        "default": {
            "modified": {"value": "2026-02-06T14:56:31Z"},
            "geographic_reference": {"value": ["ch_40_12"]},
            "language": {"value": "de"},
            "title": {"value": "Test Dataset Title"},
            "description": {"value": "<p>Test description with HTML</p>"},
            "keyword": {"value": ["Test", "sample", "data"]},
            "timezone": {"value": "Europe/Zurich"},
            "modified_updates_on_metadata_change": {"value": False},
            "modified_updates_on_data_change": {"value": False},
            "geographic_reference_auto": {"value": False},
            "publisher": {"value": "DCC Data Competence Center"},
        },
        "custom": {
            "publizierende-organisation": {"value": "Präsidialdepartement"},
            "tags": {"value": ["test-tag"]},
        },
        "asset_content_configuration": {
            "is_explore_data_with_ai_disabled": {"value": False},
        },
    }


@pytest.fixture
def sample_status_response() -> dict:
    """Provide sample status response matching real API structure.

    Returns:
        Dictionary mimicking real API status response.
    """
    return {
        "status": "idle",
        "since": "2026-02-06T15:13:13Z",
        "is_published": True,
        "previous": "processing",
        "next": None,
        "message": None,
        "records_errors": [],
        "params": {},
    }


@pytest.fixture
def sample_datasets_list_response() -> dict:
    """Provide sample datasets list response matching real API structure.

    Returns:
        Dictionary mimicking real API datasets list response.
    """
    return {
        "total_count": 502,
        "next": "https://data.bs.ch/api/automation/v1.0/datasets/?limit=10&offset=10",
        "previous": None,
        "results": [
            {
                "uid": TEST_DATASET_UID,
                "dataset_id": TEST_DATASET_ID,
                "is_published": True,
                "is_restricted": False,
                "default_security": "public",
                "created_at": "2026-02-06T15:09:51Z",
                "updated_at": "2026-02-06T15:13:13Z",
                "metadata": {},
                "asset_type": "federated_dataset",
            }
        ],
    }


@pytest.fixture
def sample_dataset_response(sample_metadata: dict) -> dict:
    """Provide sample single dataset response.

    Args:
        sample_metadata: Sample metadata fixture.

    Returns:
        Dictionary mimicking real API single dataset response.
    """
    return {
        "uid": TEST_DATASET_UID,
        "dataset_id": TEST_DATASET_ID,
        "is_published": True,
        "is_restricted": False,
        "default_security": "public",
        "created_at": "2026-02-06T15:09:51Z",
        "updated_at": "2026-02-06T15:13:13Z",
        "metadata": sample_metadata,
        "asset_type": "federated_dataset",
    }


@pytest.fixture
def sample_uid_lookup_response() -> dict:
    """Provide sample response for UID lookup by dataset ID.

    Returns:
        Dictionary mimicking real API response for dataset lookup.
    """
    return {
        "total_count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "uid": TEST_DATASET_UID,
                "dataset_id": TEST_DATASET_ID,
                "is_published": True,
                "is_restricted": False,
            }
        ],
    }


# =============================================================================
# Error Response Fixtures
# =============================================================================


@pytest.fixture
def sample_404_error() -> dict:
    """Provide sample 404 error response.

    Returns:
        Dictionary mimicking API 404 error response.
    """
    return {
        "error_code": "not_found",
        "message": "Dataset not found",
    }


@pytest.fixture
def sample_validation_error() -> dict:
    """Provide sample validation error response.

    Returns:
        Dictionary mimicking API validation error response.
    """
    return {
        "error_code": "validation_error",
        "message": "Invalid field value",
        "fields": {"title": ["This field is required"]},
    }
