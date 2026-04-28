"""Unit tests for custom metadata fields and dataset tags helpers."""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from huwise_utils_py import (
    get_dataset_custom_field,
    get_dataset_tags,
    set_dataset_custom_field,
    set_dataset_tags,
    set_dataset_title,
)
from huwise_utils_py.config import HuwiseConfig
from huwise_utils_py.dataset import HuwiseDataset


def _make_dataset() -> HuwiseDataset:
    """Build dataset instance without environment dependency."""
    return HuwiseDataset(uid="dataset-uid", config=HuwiseConfig(api_key="test-key"))


def _mock_template_response(payload: dict[str, Any]) -> MagicMock:
    """Build response object for metadata template endpoints."""
    response = MagicMock()
    response.json.return_value = payload
    return response


def test_huwise_dataset_set_custom_field_with_valid_value_calls_put_endpoint() -> None:
    """Custom field setter should delegate to custom template endpoint."""
    dataset = _make_dataset()
    dataset._wait_for_idle = MagicMock()
    dataset._client = MagicMock()

    result = dataset.set_custom_field("publizierende_organisation", "Open Data", publish=False)

    assert result is dataset
    dataset._client.put.assert_called_once_with(
        "/datasets/dataset-uid/metadata/custom/publizierende_organisation/",
        json={"value": "Open Data"},
    )
    dataset._client.post.assert_not_called()


def test_huwise_dataset_get_custom_field_with_valid_key_returns_value() -> None:
    """Custom field getter should read from custom template."""
    dataset = _make_dataset()
    dataset._client = MagicMock()
    dataset._client.get.return_value = _mock_template_response({
        "publizierende_organisation": {"value": "Open Data Basel-Stadt"}
    })

    result = dataset.get_custom_field("publizierende_organisation")

    assert result == "Open Data Basel-Stadt"
    dataset._client.get.assert_called_once_with("/datasets/dataset-uid/metadata/custom/")


def test_huwise_dataset_set_tags_with_valid_values_calls_default_tags_endpoint() -> None:
    """Tags setter should write to default.tags endpoint."""
    dataset = _make_dataset()
    dataset._wait_for_idle = MagicMock()
    dataset._client = MagicMock()

    result = dataset.set_tags(["opendata.swiss", "mobility"], publish=False)

    assert result is dataset
    dataset._client.put.assert_called_once_with(
        "/datasets/dataset-uid/metadata/default/tags/",
        json={"value": ["opendata.swiss", "mobility"]},
    )
    dataset._client.post.assert_not_called()


def test_huwise_dataset_get_tags_when_missing_returns_empty_list() -> None:
    """Unset tags should map to an empty list."""
    dataset = _make_dataset()
    dataset._client = MagicMock()
    dataset._client.get.return_value = _mock_template_response({})

    assert dataset.get_tags() == []


def test_huwise_dataset_set_custom_field_with_empty_key_raises_value_error() -> None:
    """Empty custom field key should raise clear validation error."""
    dataset = _make_dataset()

    with pytest.raises(ValueError, match="field_key must be a non-empty string"):
        dataset.set_custom_field("   ", "value")


def test_huwise_dataset_set_custom_field_with_non_serializable_value_raises_value_error() -> None:
    """Non-JSON payload should fail early with explicit error."""
    dataset = _make_dataset()

    with pytest.raises(ValueError, match="value must be JSON-serializable"):
        dataset.set_custom_field("publizierende_organisation", {"raw": {1, 2, 3}})


def test_huwise_dataset_set_tags_with_invalid_payload_raises_error() -> None:
    """Invalid tag payload should be rejected before API call."""
    dataset = _make_dataset()

    with pytest.raises(TypeError, match="tags must be a list\\[str\\]"):
        dataset.set_tags("opendata.swiss")  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="tags must contain only non-empty strings"):
        dataset.set_tags(["ok", " "])


def test_legacy_set_dataset_custom_field_with_missing_dataset_identifier_raises_value_error() -> None:
    """Legacy helper should preserve dataset identifier validation behavior."""
    with pytest.raises(ValueError):
        set_dataset_custom_field("publizierende_organisation", "Open Data")


def test_legacy_set_dataset_tags_delegates_to_dataset_by_uid() -> None:
    """Legacy helper should resolve uid and call HuwiseDataset API."""
    with (
        patch("huwise_utils_py._legacy.setters.validate_dataset_identifier", return_value="resolved-uid") as validate,
        patch("huwise_utils_py._legacy.setters.HuwiseDataset") as dataset_cls,
    ):
        set_dataset_tags(["opendata.swiss"], dataset_uid="dataset-uid", publish=False)

    validate.assert_called_once_with(None, "dataset-uid")
    dataset_cls.assert_called_once_with(uid="resolved-uid")
    dataset_cls.return_value.set_tags.assert_called_once_with(["opendata.swiss"], publish=False)


def test_legacy_get_dataset_custom_field_and_tags_delegate_to_dataset_api() -> None:
    """Legacy getters should call new dataset methods."""
    with (
        patch("huwise_utils_py._legacy.getters.validate_dataset_identifier", return_value="resolved-uid"),
        patch("huwise_utils_py._legacy.getters.HuwiseDataset") as dataset_cls,
    ):
        dataset_instance = dataset_cls.return_value
        dataset_instance.get_custom_field.return_value = "Open Data Basel-Stadt"
        dataset_instance.get_tags.return_value = ["opendata.swiss"]

        custom_field = get_dataset_custom_field("publizierende_organisation", dataset_id="100123")
        tags = get_dataset_tags(dataset_id="100123")

    assert custom_field == "Open Data Basel-Stadt"
    assert tags == ["opendata.swiss"]


def test_existing_legacy_set_dataset_title_still_delegates_without_regression() -> None:
    """Existing metadata setter behavior should remain unchanged."""
    with (
        patch("huwise_utils_py._legacy.setters.validate_dataset_identifier", return_value="resolved-uid"),
        patch("huwise_utils_py._legacy.setters.HuwiseDataset") as dataset_cls,
    ):
        set_dataset_title("Updated title", dataset_id="100123", publish=False)

    dataset_cls.return_value.set_title.assert_called_once_with("Updated title", publish=False)
