"""Unit tests for new legacy schema and creation wrappers."""

from unittest.mock import MagicMock, patch

from huwise_utils_py._legacy.getters import (
    get_dataset_field_configuration,
    list_dataset_field_configurations,
)
from huwise_utils_py._legacy.setters import (
    append_dataset_field_configuration,
    create_dataset,
    delete_dataset_field_configuration,
    update_dataset_configuration,
    update_dataset_field_configuration,
)
from huwise_utils_py.dataset import HuwiseDataset


def test_create_dataset_delegates_to_classmethod() -> None:
    """Test create_dataset delegates to HuwiseDataset.create."""
    created = MagicMock(spec=HuwiseDataset)
    with patch.object(HuwiseDataset, "create", return_value=created) as create_mock:
        result = create_dataset(metadata={"default": {"title": {"value": "Title"}}}, dataset_id="new-id")

    assert result is created
    create_mock.assert_called_once_with(
        metadata={"default": {"title": {"value": "Title"}}},
        dataset_id="new-id",
        is_restricted=None,
        default_security=None,
        config=None,
    )


def test_update_dataset_configuration_delegates_to_dataset_method() -> None:
    """Test update_dataset_configuration delegates to HuwiseDataset.update_configuration."""
    with patch("huwise_utils_py._legacy.setters.HuwiseDataset") as dataset_cls:
        dataset_instance = MagicMock()
        dataset_cls.return_value = dataset_instance

        update_dataset_configuration(
            dataset_id="updated-id",
            is_restricted=False,
            target_dataset_uid="da_tbcnel",
        )

    dataset_cls.assert_called_once_with(uid="da_tbcnel")
    dataset_instance.update_configuration.assert_called_once_with(
        dataset_id="updated-id",
        is_restricted=False,
        default_security=None,
    )


def test_field_configuration_wrappers_delegate_to_dataset_methods() -> None:
    """Test field configuration wrappers delegate to corresponding dataset methods."""
    with patch("huwise_utils_py._legacy.setters.HuwiseDataset") as dataset_cls:
        dataset_instance = MagicMock()
        dataset_cls.return_value = dataset_instance
        payload = {"type": "rename", "from_name": "a", "to_name": "b", "label": "Rename"}

        append_dataset_field_configuration(payload, dataset_uid="da_tbcnel")
        update_dataset_field_configuration("pr_123", payload, dataset_uid="da_tbcnel")
        delete_dataset_field_configuration("pr_123", dataset_uid="da_tbcnel")

    dataset_instance.append_field_configuration.assert_called_once_with(payload)
    dataset_instance.update_field_configuration.assert_called_once_with("pr_123", payload)
    dataset_instance.delete_field_configuration.assert_called_once_with("pr_123")


def test_field_configuration_getter_wrappers_delegate_to_dataset_methods() -> None:
    """Test getter wrappers for field configuration delegate to HuwiseDataset."""
    with patch("huwise_utils_py._legacy.getters.HuwiseDataset") as dataset_cls:
        dataset_instance = MagicMock()
        dataset_cls.return_value = dataset_instance

        list_dataset_field_configurations(dataset_uid="da_tbcnel", limit=10, offset=2)
        get_dataset_field_configuration("pr_123", dataset_uid="da_tbcnel")

    dataset_instance.list_field_configurations.assert_called_once_with(limit=10, offset=2)
    dataset_instance.retrieve_field_configuration.assert_called_once_with("pr_123")
