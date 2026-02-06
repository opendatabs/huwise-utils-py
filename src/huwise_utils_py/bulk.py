"""Bulk operations for Huwise datasets.

This module provides both synchronous and asynchronous functions for
performing bulk operations on multiple datasets efficiently.
"""

import asyncio
from typing import Any

from huwise_utils_py.config import HuwiseConfig
from huwise_utils_py.http import AsyncHttpClient, HttpClient
from huwise_utils_py.logger import get_logger

logger = get_logger(__name__)


# =============================================================================
# Async Bulk Operations
# =============================================================================


async def bulk_get_metadata_async(
    dataset_uids: list[str],
    config: HuwiseConfig | None = None,
) -> dict[str, dict[str, Any]]:
    """Fetch metadata for multiple datasets concurrently.

    Uses async HTTP requests to fetch metadata in parallel, providing
    significant performance improvements over sequential requests.

    Args:
        dataset_uids: List of dataset UIDs to fetch metadata for.
        config: Optional HuwiseConfig instance.

    Returns:
        Dictionary mapping dataset UID to its metadata.

    Example:
        >>> metadata = await bulk_get_metadata_async(["da_123", "da_456"])
        >>> for uid, meta in metadata.items():
        ...     print(f"{uid}: {meta.get('default', {}).get('title', {}).get('value')}")
    """
    config = config or HuwiseConfig.from_env()
    client = AsyncHttpClient(config)

    logger.info("Starting bulk metadata fetch", dataset_count=len(dataset_uids))

    async with client.session() as session:
        tasks = [session.get(f"{config.base_url}/datasets/{uid}") for uid in dataset_uids]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    result: dict[str, dict[str, Any]] = {}
    for uid, response in zip(dataset_uids, responses, strict=True):
        if isinstance(response, Exception):
            logger.warning("Failed to fetch metadata", uid=uid, error=str(response))
            result[uid] = {"error": str(response)}
        else:
            result[uid] = response.json()["metadata"]

    logger.info(
        "Completed bulk metadata fetch",
        successful=len([r for r in result.values() if "error" not in r]),
        failed=len([r for r in result.values() if "error" in r]),
    )

    return result


async def bulk_update_metadata_async(  # noqa: C901
    updates: list[dict[str, Any]],
    config: HuwiseConfig | None = None,
    *,
    publish: bool = True,
) -> dict[str, dict[str, Any]]:
    """Update metadata for multiple datasets concurrently.

    Each update dict must contain either 'dataset_uid' or 'dataset_id'
    along with the metadata fields to update.

    Args:
        updates: List of update dictionaries, each containing:
            - dataset_uid or dataset_id: Identifier for the dataset
            - Other keys: Metadata fields to update (e.g., title, description)
        config: Optional HuwiseConfig instance.
        publish: Whether to publish datasets after updating.

    Returns:
        Dictionary mapping dataset UID to update result.

    Raises:
        ValueError: If an update dict contains both or neither identifier.

    Example:
        >>> updates = [
        ...     {"dataset_uid": "da_123", "title": "New Title 1"},
        ...     {"dataset_uid": "da_456", "title": "New Title 2"},
        ... ]
        >>> results = await bulk_update_metadata_async(updates)
    """
    config = config or HuwiseConfig.from_env()
    client = HttpClient(config)

    logger.info("Starting bulk metadata update", update_count=len(updates))

    results: dict[str, dict[str, Any]] = {}

    for update in updates:
        dataset_uid = update.get("dataset_uid")
        dataset_id = update.get("dataset_id")

        if dataset_uid and dataset_id:
            raise ValueError(f"Update contains both dataset_id and dataset_uid: {update}")
        if not dataset_uid and not dataset_id:
            raise ValueError(f"Update must contain either dataset_id or dataset_uid: {update}")

        # Resolve dataset_id to uid if needed
        if dataset_id:
            response = client.get("/datasets/", params={"dataset_id": dataset_id})
            dataset_uid = response.json()["results"][0]["uid"]

        try:
            # Get current metadata
            response = client.get(f"/datasets/{dataset_uid}/metadata/")
            metadata: dict[str, Any] = response.json()

            # Update fields
            fields_updated = []
            for key, value in update.items():
                if key in ("dataset_uid", "dataset_id"):
                    continue
                if "default" not in metadata:
                    metadata["default"] = {}
                if key not in metadata["default"]:
                    metadata["default"][key] = {}
                metadata["default"][key]["value"] = value
                fields_updated.append(key)

            # Push updated metadata
            client.put(f"/datasets/{dataset_uid}/metadata/", json=metadata)

            if publish:
                client.post(f"/datasets/{dataset_uid}/publish/")

            results[dataset_uid] = {"status": "success", "fields_updated": fields_updated}
            logger.debug("Updated dataset", uid=dataset_uid, fields=fields_updated)

        except Exception as e:
            results[dataset_uid] = {"status": "error", "error": str(e)}
            logger.warning("Failed to update dataset", uid=dataset_uid, error=str(e))

    logger.info(
        "Completed bulk metadata update",
        successful=len([r for r in results.values() if r["status"] == "success"]),
        failed=len([r for r in results.values() if r["status"] == "error"]),
    )

    return results


# =============================================================================
# Sync Implementations
# =============================================================================


def bulk_get_metadata(
    dataset_uids: list[str],
    config: HuwiseConfig | None = None,
) -> dict[str, dict[str, Any]]:
    """Fetch metadata for multiple datasets synchronously.

    Uses sequential HTTP requests. For better performance with many datasets,
    use bulk_get_metadata_async instead.

    Args:
        dataset_uids: List of dataset UIDs to fetch metadata for.
        config: Optional HuwiseConfig instance.

    Returns:
        Dictionary mapping dataset UID to its metadata.

    Example:
        >>> metadata = bulk_get_metadata(["da_123", "da_456"])
    """
    config = config or HuwiseConfig.from_env()
    client = HttpClient(config)

    logger.info("Starting bulk metadata fetch", dataset_count=len(dataset_uids))

    result: dict[str, dict[str, Any]] = {}
    for uid in dataset_uids:
        try:
            response = client.get(f"/datasets/{uid}")
            result[uid] = response.json()["metadata"]
        except Exception as e:
            logger.warning("Failed to fetch metadata", uid=uid, error=str(e))
            result[uid] = {"error": str(e)}

    logger.info(
        "Completed bulk metadata fetch",
        successful=len([r for r in result.values() if "error" not in r]),
        failed=len([r for r in result.values() if "error" in r]),
    )

    return result


def bulk_update_metadata(
    updates: list[dict[str, Any]],
    config: HuwiseConfig | None = None,
    *,
    publish: bool = True,
) -> dict[str, dict[str, Any]]:
    """Update metadata for multiple datasets synchronously.

    Each update dict must contain either 'dataset_uid' or 'dataset_id'
    along with the metadata fields to update.

    Args:
        updates: List of update dictionaries.
        config: Optional HuwiseConfig instance.
        publish: Whether to publish datasets after updating.

    Returns:
        Dictionary mapping dataset UID to update result.
    """
    # The async version uses sync HttpClient, so we can use asyncio.run
    # Note: If called from async context, use bulk_update_metadata_async instead
    return asyncio.run(bulk_update_metadata_async(updates, config, publish=publish))


# =============================================================================
# Additional Bulk Operations
# =============================================================================


async def bulk_get_dataset_ids_async(
    config: HuwiseConfig | None = None,
    *,
    include_restricted: bool = True,
    max_datasets: int | None = None,
) -> list[str]:
    """Retrieve all dataset IDs asynchronously.

    Args:
        config: Optional HuwiseConfig instance.
        include_restricted: Include restricted datasets.
        max_datasets: Maximum number of datasets to return.

    Returns:
        Sorted list of dataset IDs.
    """
    config = config or HuwiseConfig.from_env()
    client = AsyncHttpClient(config)

    all_ids: list[str] = []
    batch_size = 100

    async with client.session() as session:
        # First request
        response = await session.get(f"{config.base_url}/datasets/?limit={batch_size}")
        data = response.json()

        while True:
            results = data.get("results", [])

            if include_restricted:
                all_ids.extend(item["dataset_id"] for item in results)
            else:
                all_ids.extend(item["dataset_id"] for item in results if not item["is_restricted"])

            if max_datasets and len(all_ids) >= max_datasets:
                all_ids = all_ids[:max_datasets]
                break

            next_url = data.get("next")
            if not next_url:
                break

            response = await session.get(next_url)
            data = response.json()

    all_ids.sort()
    logger.info("Retrieved dataset IDs", count=len(all_ids))
    return all_ids


def bulk_get_dataset_ids(
    config: HuwiseConfig | None = None,
    *,
    include_restricted: bool = True,
    max_datasets: int | None = None,
) -> list[str]:
    """Retrieve all dataset IDs synchronously.

    Uses sequential HTTP requests with pagination.

    Args:
        config: Optional HuwiseConfig instance.
        include_restricted: Include restricted datasets.
        max_datasets: Maximum number of datasets to return.

    Returns:
        Sorted list of dataset IDs.
    """
    config = config or HuwiseConfig.from_env()
    client = HttpClient(config)

    all_ids: list[str] = []
    batch_size = 100
    offset = 0

    while True:
        response = client.get(f"/datasets/?limit={batch_size}&offset={offset}")
        data = response.json()
        results = data.get("results", [])

        if not results:
            break

        if include_restricted:
            all_ids.extend(item["dataset_id"] for item in results)
        else:
            all_ids.extend(item["dataset_id"] for item in results if not item["is_restricted"])

        if max_datasets and len(all_ids) >= max_datasets:
            all_ids = all_ids[:max_datasets]
            break

        if not data.get("next"):
            break

        offset += batch_size

    all_ids.sort()
    logger.info("Retrieved dataset IDs", count=len(all_ids))
    return all_ids
