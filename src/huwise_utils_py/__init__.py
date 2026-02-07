"""Huwise Utils Python - A Python wrapper library for the Huwise Automation API.

This package provides a modern, type-safe interface for interacting with the Huwise
(formerly OpenDataSoft) Automation API to manage datasets, metadata, and more.

Examples:
    Using the object-oriented API:

    ```python
    from huwise_utils_py import HuwiseDataset

    dataset = HuwiseDataset(uid="da_abc123")
    dataset.set_title("New Title").set_description("Description").publish()
    ```

    Using the function-based API:

    ```python
    from huwise_utils_py import get_dataset_title, set_dataset_title

    title = get_dataset_title(dataset_uid="da_abc123")
    ```
"""

# Function-based API
from huwise_utils_py._legacy import (
    get_all_dataset_ids,
    get_dataset_custom_view,
    get_dataset_description,
    get_dataset_keywords,
    get_dataset_language,
    get_dataset_license,
    get_dataset_metadata,
    get_dataset_metadata_temporal_period,
    get_dataset_publisher,
    get_dataset_theme,
    get_dataset_title,
    get_number_of_datasets,
    get_template_metadata,
    get_uid_by_id,
    set_dataset_description,
    set_dataset_keywords,
    set_dataset_language,
    set_dataset_license,
    set_dataset_metadata_temporal_coverage_end_date,
    set_dataset_metadata_temporal_coverage_start_date,
    set_dataset_metadata_temporal_period,
    set_dataset_public,
    set_dataset_publisher,
    set_dataset_theme,
    set_dataset_title,
    set_template_metadata,
)
from huwise_utils_py.bulk import (
    bulk_get_dataset_ids,
    bulk_get_dataset_ids_async,
    bulk_get_metadata,
    bulk_get_metadata_async,
    bulk_update_metadata,
    bulk_update_metadata_async,
)
from huwise_utils_py.config import HuwiseConfig
from huwise_utils_py.dataset import LICENSE_MAP, HuwiseDataset
from huwise_utils_py.http import AsyncHttpClient, HttpClient
from huwise_utils_py.logger import get_logger, init_logger

# Utilities
from huwise_utils_py.utils import retry, validate_dataset_identifier

__version__ = "1.1.0"

__all__ = [
    "LICENSE_MAP",
    "AsyncHttpClient",
    "HttpClient",
    # Core components (new API)
    "HuwiseConfig",
    "HuwiseDataset",
    # Version
    "__version__",
    "bulk_get_dataset_ids",
    "bulk_get_dataset_ids_async",
    # Bulk operations (new API)
    "bulk_get_metadata",
    "bulk_get_metadata_async",
    "bulk_update_metadata",
    "bulk_update_metadata_async",
    # Function-based API
    "get_all_dataset_ids",
    "get_dataset_custom_view",
    "get_dataset_description",
    "get_dataset_keywords",
    "get_dataset_language",
    "get_dataset_license",
    "get_dataset_metadata",
    "get_dataset_metadata_temporal_period",
    "get_dataset_publisher",
    "get_dataset_theme",
    "get_dataset_title",
    "get_logger",
    "get_number_of_datasets",
    "get_template_metadata",
    "get_uid_by_id",
    "init_logger",
    # Utilities
    "retry",
    "set_dataset_description",
    "set_dataset_keywords",
    "set_dataset_language",
    "set_dataset_license",
    "set_dataset_metadata_temporal_coverage_end_date",
    "set_dataset_metadata_temporal_coverage_start_date",
    "set_dataset_metadata_temporal_period",
    "set_dataset_public",
    "set_dataset_publisher",
    "set_dataset_theme",
    "set_dataset_title",
    "set_template_metadata",
    "validate_dataset_identifier",
]
