"""Validators for Huwise Utils.

This module provides validation functions for dataset identifiers
and other input validation needs.
"""

from huwise_utils_py.config import HuwiseConfig
from huwise_utils_py.http import HttpClient


def validate_dataset_identifier(
    dataset_id: str | None = None,
    dataset_uid: str | None = None,
    config: HuwiseConfig | None = None,
) -> str:
    """Validate and resolve dataset identifier to UID.

    Either dataset_id or dataset_uid must be provided, but not both.
    If dataset_id is provided, it will be resolved to the corresponding UID.

    Args:
        dataset_id: The numeric identifier of the dataset.
        dataset_uid: The unique string identifier (UID) of the dataset.
        config: Optional HuwiseConfig for ID resolution.

    Returns:
        The dataset UID.

    Raises:
        ValueError: If both dataset_id and dataset_uid are provided.
        ValueError: If neither dataset_id nor dataset_uid is provided.
        IndexError: If dataset_id cannot be resolved to a UID.

    Examples:
        Resolve a numeric ID to a UID:

        ```python
        uid = validate_dataset_identifier(dataset_id="12345")
        ```

        Use a UID directly:

        ```python
        uid = validate_dataset_identifier(dataset_uid="da_abc123")
        ```
    """
    if dataset_id is not None and dataset_uid is not None:
        raise ValueError("dataset_id and dataset_uid are mutually exclusive")

    if dataset_id is None and dataset_uid is None:
        raise ValueError("Either dataset_id or dataset_uid must be specified")

    if dataset_id is not None:
        config = config or HuwiseConfig.from_env()
        client = HttpClient(config)
        response = client.get("/datasets/", params={"dataset_id": dataset_id})
        return response.json()["results"][0]["uid"]

    return dataset_uid  # type: ignore[return-value]
