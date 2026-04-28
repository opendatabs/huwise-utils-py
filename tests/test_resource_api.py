"""Unit tests for dataset resource APIs."""

from typing import Any
from unittest.mock import MagicMock, patch

from huwise_utils_py import delete_dataset_resource, list_dataset_resources, upsert_dataset_resource_http
from huwise_utils_py.config import HuwiseConfig
from huwise_utils_py.dataset import HuwiseDataset


class _DummyResponse:
    """Minimal response test double with json payload."""

    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload

    def json(self) -> dict[str, Any]:
        """Return stored payload."""
        return self._payload


def _make_dataset() -> HuwiseDataset:
    """Build dataset instance without environment dependency."""
    return HuwiseDataset(uid="dataset-uid", config=HuwiseConfig(api_key="test-key"))


def test_huwise_dataset_upsert_http_resource_create_posts_resource_with_normalized_url() -> None:
    """Create path should normalize URL and call POST."""
    dataset = _make_dataset()
    dataset._wait_for_idle = MagicMock()
    dataset.list_resources = MagicMock(return_value={"results": []})
    dataset._client = MagicMock()
    dataset._client.post.return_value = _DummyResponse({"uid": "resource-uid"})

    result = dataset.upsert_http_resource(
        source_url="https://DATA-BS.CH/stata/fgi/stac/AFBA_Abfuhrzonen.geojson/",
        title="100095stac.geojson",
    )

    assert result == {"uid": "resource-uid"}
    dataset._client.post.assert_called_once_with(
        "/datasets/dataset-uid/resources/",
        json={
            "type": "http",
            "connection": {"url": "https://data-bs.ch"},
            "relative_url": "/stata/fgi/stac/AFBA_Abfuhrzonen.geojson",
            "title": "100095stac.geojson",
        },
    )
    dataset._client.put.assert_not_called()


def test_huwise_dataset_upsert_http_resource_update_puts_existing_resource() -> None:
    """Update path should call PUT when matching URL exists."""
    dataset = _make_dataset()
    dataset._wait_for_idle = MagicMock()
    dataset.list_resources = MagicMock(
        return_value={
            "results": [
                {
                    "uid": "resource-uid",
                    "title": "old-title",
                    "connection": {"url": "https://data-bs.ch"},
                    "relative_url": "/stata/fgi/stac/AFBA_Abfuhrzonen.geojson",
                }
            ]
        }
    )
    dataset._client = MagicMock()
    dataset._client.put.return_value = _DummyResponse({"uid": "resource-uid", "updated": True})

    result = dataset.upsert_http_resource(
        source_url="https://data-bs.ch/stata/fgi/stac/AFBA_Abfuhrzonen.geojson",
        title="new-title",
    )

    assert result == {"uid": "resource-uid", "updated": True}
    dataset._client.put.assert_called_once_with(
        "/datasets/dataset-uid/resources/resource-uid/",
        json={
            "type": "http",
            "connection": {"url": "https://data-bs.ch"},
            "relative_url": "/stata/fgi/stac/AFBA_Abfuhrzonen.geojson",
            "title": "new-title",
        },
    )
    dataset._client.post.assert_not_called()


def test_huwise_dataset_upsert_http_resource_with_extractor_type_passes_value() -> None:
    """Explicit extractor_type should be included in the payload."""
    dataset = _make_dataset()
    dataset._wait_for_idle = MagicMock()
    dataset.list_resources = MagicMock(return_value={"results": []})
    dataset._client = MagicMock()
    dataset._client.post.return_value = _DummyResponse({"uid": "resource-uid"})

    dataset.upsert_http_resource(
        source_url="https://data-bs.ch/resource.geojson",
        extractor_type="geojson",
    )

    call_kwargs = dataset._client.post.call_args.kwargs
    assert call_kwargs["json"]["extractor_type"] == "geojson"


def test_huwise_dataset_upsert_http_resource_without_extractor_type_omits_value() -> None:
    """No extractor_type should result in no extractor key."""
    dataset = _make_dataset()
    dataset._wait_for_idle = MagicMock()
    dataset.list_resources = MagicMock(return_value={"results": []})
    dataset._client = MagicMock()
    dataset._client.post.return_value = _DummyResponse({"uid": "resource-uid"})

    dataset.upsert_http_resource(source_url="https://data-bs.ch/resource.geojson")

    call_kwargs = dataset._client.post.call_args.kwargs
    assert "extractor_type" not in call_kwargs["json"]


def test_upsert_dataset_resource_http_with_dataset_id_uses_identifier_resolution() -> None:
    """Legacy wrapper should resolve dataset_id and delegate to dataset API."""
    with (
        patch("huwise_utils_py._legacy.setters.validate_dataset_identifier", return_value="resolved-uid") as validate,
        patch("huwise_utils_py._legacy.setters.HuwiseDataset") as dataset_cls,
    ):
        dataset_instance = dataset_cls.return_value
        dataset_instance.upsert_http_resource.return_value = {"uid": "resource-uid"}
        result = upsert_dataset_resource_http(dataset_id="100095stac", source_url="https://data-bs.ch/file.geojson")

    validate.assert_called_once_with("100095stac", None)
    dataset_cls.assert_called_once_with(uid="resolved-uid")
    dataset_instance.upsert_http_resource.assert_called_once()
    assert result == {"uid": "resource-uid"}


def test_list_and_delete_dataset_resource_with_dataset_uid_delegate_to_dataset_api() -> None:
    """Legacy wrappers should accept dataset_uid and delegate correctly."""
    with (
        patch(
            "huwise_utils_py._legacy.getters.validate_dataset_identifier", return_value="resolved-uid"
        ) as validate_get,
        patch("huwise_utils_py._legacy.getters.HuwiseDataset") as dataset_get_cls,
    ):
        dataset_get_instance = dataset_get_cls.return_value
        dataset_get_instance.list_resources.return_value = {"results": []}
        list_result = list_dataset_resources(dataset_uid="dataset-uid", limit=10, offset=20)

    validate_get.assert_called_once_with(None, "dataset-uid")
    dataset_get_cls.assert_called_once_with(uid="resolved-uid")
    dataset_get_instance.list_resources.assert_called_once_with(limit=10, offset=20)
    assert list_result == {"results": []}

    with (
        patch(
            "huwise_utils_py._legacy.setters.validate_dataset_identifier", return_value="resolved-uid"
        ) as validate_set,
        patch("huwise_utils_py._legacy.setters.HuwiseDataset") as dataset_set_cls,
    ):
        dataset_set_instance = dataset_set_cls.return_value
        delete_dataset_resource("resource-uid", dataset_uid="dataset-uid")

    validate_set.assert_called_once_with(None, "dataset-uid")
    dataset_set_cls.assert_called_once_with(uid="resolved-uid")
    dataset_set_instance.delete_resource.assert_called_once_with("resource-uid")


def test_huwise_dataset_create_with_resource_upserts_resource_after_creation() -> None:
    """Create should upsert resource when resource_source_url is provided."""
    config = HuwiseConfig(api_key="test-key")
    with (
        patch("huwise_utils_py.dataset.HttpClient") as client_cls,
        patch.object(HuwiseDataset, "_wait_for_idle") as wait_for_idle,
        patch.object(HuwiseDataset, "upsert_http_resource") as upsert_resource,
    ):
        client_instance = client_cls.return_value
        client_instance.post.return_value = _DummyResponse({"uid": "dataset-uid"})

        created = HuwiseDataset.create(
            metadata={"default": {"title": {"value": "Example"}}},
            dataset_id="example-dataset",
            resource_source_url="https://data-bs.ch/source.geojson",
            resource_title="example.geojson",
            resource_extractor_type="geojson",
            resource_headers=[{"name": "Authorization", "value": "token"}],
            config=config,
        )

    assert created.uid == "dataset-uid"
    wait_for_idle.assert_called()
    upsert_resource.assert_called_once_with(
        source_url="https://data-bs.ch/source.geojson",
        title="example.geojson",
        extractor_type="geojson",
        headers=[{"name": "Authorization", "value": "token"}],
    )


def test_huwise_dataset_create_without_resource_does_not_upsert_resource() -> None:
    """Create should skip resource upsert when no source URL is provided."""
    config = HuwiseConfig(api_key="test-key")
    with (
        patch("huwise_utils_py.dataset.HttpClient") as client_cls,
        patch.object(HuwiseDataset, "_wait_for_idle"),
        patch.object(HuwiseDataset, "upsert_http_resource") as upsert_resource,
    ):
        client_instance = client_cls.return_value
        client_instance.post.return_value = _DummyResponse({"uid": "dataset-uid"})

        HuwiseDataset.create(
            metadata={"default": {"title": {"value": "Example"}}},
            dataset_id="example-dataset",
            config=config,
        )

    upsert_resource.assert_not_called()
