"""Getter functions for dataset metadata.

These functions provide a simple interface for reading dataset metadata.
They wrap the HuwiseDataset class internally.
"""

from typing import Any

from huwise_utils_py.bulk import bulk_get_dataset_ids
from huwise_utils_py.config import HuwiseConfig
from huwise_utils_py.dataset import HuwiseDataset
from huwise_utils_py.http import HttpClient
from huwise_utils_py.utils.validators import validate_dataset_identifier


def get_uid_by_id(dataset_id: str) -> str:
    """Get the UID of a dataset by its ID.

    Args:
        dataset_id: The numeric identifier of the dataset.

    Returns:
        The unique string identifier (UID) of the dataset.

    Raises:
        IndexError: If no dataset is found with the given ID.
    """
    config = HuwiseConfig.from_env()
    client = HttpClient(config)
    response = client.get("/datasets/", params={"dataset_id": dataset_id})
    return response.json()["results"][0]["uid"]


def get_all_dataset_ids(
    include_restricted: bool = True,
    max_datasets: int | None = None,
    cooldown: float = 1.0,
) -> list[str]:
    """Retrieve all dataset IDs.

    Args:
        include_restricted: Include restricted datasets.
        max_datasets: Maximum number of datasets to return.
        cooldown: Deprecated parameter, kept for backwards compatibility.

    Returns:
        Sorted list of dataset IDs.
    """
    return bulk_get_dataset_ids(include_restricted=include_restricted, max_datasets=max_datasets)


def get_number_of_datasets() -> int:
    """Get the total number of datasets.

    Returns:
        The total count of datasets.
    """
    config = HuwiseConfig.from_env()
    client = HttpClient(config)
    response = client.get("/datasets/?limit=1")
    return response.json()["total_count"]


def get_dataset_metadata(
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
) -> dict[str, Any]:
    """Get the full metadata of a dataset.

    Args:
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.

    Returns:
        Dictionary containing all metadata.

    Raises:
        ValueError: If both or neither identifiers are provided.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    return dataset.get_metadata()


def get_dataset_title(
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
) -> str | None:
    """Get the title of a dataset.

    Args:
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.

    Returns:
        The dataset title or None if not set.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    return dataset.get_title()


def get_dataset_description(
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
) -> str | None:
    """Get the description of a dataset.

    Args:
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.

    Returns:
        The dataset description or None if not set.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    return dataset.get_description()


def get_dataset_keywords(
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
) -> list[str] | None:
    """Get the keywords of a dataset.

    Args:
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.

    Returns:
        List of keywords or None if not set.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    return dataset.get_keywords()


def get_dataset_language(
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
) -> str | None:
    """Get the language of a dataset.

    Args:
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.

    Returns:
        The language code or None if not set.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    return dataset.get_language()


def get_dataset_publisher(
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
) -> str | None:
    """Get the publisher of a dataset.

    Args:
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.

    Returns:
        The publisher name or None if not set.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    return dataset.get_publisher()


def get_dataset_theme(
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
) -> str | None:
    """Get the theme of a dataset.

    Args:
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.

    Returns:
        The theme ID or None if not set.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    return dataset.get_theme()


def get_dataset_license(
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    no_license_default_value: str = "none_specified",
) -> str:
    """Get the license of a dataset.

    Args:
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        no_license_default_value: Value to return if no license is set.

    Returns:
        The license ID or the default value if not set.

    Raises:
        ValueError: If no_license_default_value is a valid license ID.
    """
    valid_license_ids = [
        "cc_by",
        "cc_by_sa",
        "cc_by_nd",
        "cc_by_nc",
        "cc_by_nc_sa",
        "cc_by_nc_nd",
        "cc0",
        "odbl",
        "pddl",
        "fr_lo",
        "ogl",
    ]
    if no_license_default_value in valid_license_ids:
        raise ValueError(f"no_license_default_value must not be a valid license ID: {valid_license_ids}")

    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    license_id = dataset.get_license()
    return license_id if license_id else no_license_default_value


def get_dataset_custom_view(
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
) -> dict[str, Any] | None:
    """Get the custom view configuration of a dataset.

    Args:
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.

    Returns:
        Custom view dictionary or None if not set.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    return dataset.get_custom_view()


def get_dataset_metadata_temporal_period(
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
) -> dict[str, str | None]:
    """Get the temporal period metadata of a dataset.

    Args:
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.

    Returns:
        Dictionary with 'start_date' and 'end_date' keys.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    metadata = dataset.get_metadata()

    dcat = metadata.get("dcat", {})
    start_date = dcat.get("temporal_coverage_start_date", {}).get("value")
    end_date = dcat.get("temporal_coverage_end_date", {}).get("value")

    return {"start_date": start_date, "end_date": end_date}


def get_template_metadata(
    template_name: str,
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
) -> dict[str, Any]:
    """Get metadata from a specific template.

    Args:
        template_name: Name of the metadata template.
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.

    Returns:
        Dictionary containing the template metadata.
    """
    uid = validate_dataset_identifier(dataset_id, dataset_uid)
    dataset = HuwiseDataset(uid=uid)
    metadata = dataset.get_metadata()
    return metadata.get(template_name, {})
