"""Huwise Utils Python - A Python wrapper library for the Huwise Automation API.

This package provides a modern, type-safe interface for interacting with the Huwise
(formerly OpenDataSoft) Automation API to manage datasets, metadata, and more.

Examples:
    Using the object-oriented API:

    ```python
    from huwise_utils_py import HuwiseDataset

    dataset = HuwiseDataset.from_id("100123")
    dataset.set_title("New Title").set_description("Description").publish()
    ```

    Using the function-based API:

    ```python
    from huwise_utils_py import get_dataset_title, set_dataset_title

    title = get_dataset_title(dataset_id="100123")
    ```
"""

# Function-based API
from huwise_utils_py._legacy import (
    append_dataset_field_configuration,
    create_dataset,
    delete_dataset,
    delete_dataset_field_configuration,
    delete_dataset_resource,
    get_all_dataset_ids,
    get_dataset_accrualperiodicity,
    get_dataset_contact_email,
    get_dataset_contact_name,
    get_dataset_contributor,
    get_dataset_created,
    get_dataset_creator,
    get_dataset_custom_field,
    get_dataset_custom_view,
    get_dataset_dcat_ap_ch_license,
    get_dataset_dcat_ap_ch_rights,
    get_dataset_description,
    get_dataset_field_configuration,
    get_dataset_geographic_reference,
    get_dataset_issued,
    get_dataset_keywords,
    get_dataset_language,
    get_dataset_license,
    get_dataset_metadata,
    get_dataset_metadata_temporal_period,
    get_dataset_modified,
    get_dataset_publisher,
    get_dataset_relation,
    get_dataset_tags,
    get_dataset_theme,
    get_dataset_title,
    get_number_of_datasets,
    get_template_metadata,
    get_uid_by_id,
    list_dataset_field_configurations,
    list_dataset_resources,
    set_dataset_accrualperiodicity,
    set_dataset_contact_email,
    set_dataset_contact_name,
    set_dataset_contributor,
    set_dataset_created,
    set_dataset_creator,
    set_dataset_custom_field,
    set_dataset_dcat_ap_ch_license,
    set_dataset_dcat_ap_ch_rights,
    set_dataset_description,
    set_dataset_geographic_reference,
    set_dataset_issued,
    set_dataset_keywords,
    set_dataset_language,
    set_dataset_license,
    set_dataset_metadata_temporal_coverage_end_date,
    set_dataset_metadata_temporal_coverage_start_date,
    set_dataset_metadata_temporal_period,
    set_dataset_modified,
    set_dataset_public,
    set_dataset_publisher,
    set_dataset_relation,
    set_dataset_tags,
    set_dataset_theme,
    set_dataset_title,
    set_template_metadata,
    update_dataset_configuration,
    update_dataset_field_configuration,
    upsert_dataset_resource_http,
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
from huwise_utils_py.errors import HuwiseAutomationError
from huwise_utils_py.http import AsyncHttpClient, HttpClient
from huwise_utils_py.logger import get_logger, init_logger

# Utilities
from huwise_utils_py.utils import (
    assert_non_empty_dataset_id,
    build_create_dataset_metadata,
    retry,
    strip_empty_metadata_values,
    validate_dataset_identifier,
)

__version__ = "1.5.1"

__all__ = [
    "LICENSE_MAP",
    "AsyncHttpClient",
    "HttpClient",
    "HuwiseAutomationError",
    "HuwiseConfig",
    "HuwiseDataset",
    "__version__",
    "append_dataset_field_configuration",
    "assert_non_empty_dataset_id",
    "build_create_dataset_metadata",
    "bulk_get_dataset_ids",
    "bulk_get_dataset_ids_async",
    "bulk_get_metadata",
    "bulk_get_metadata_async",
    "bulk_update_metadata",
    "bulk_update_metadata_async",
    "create_dataset",
    "delete_dataset",
    "delete_dataset_field_configuration",
    "delete_dataset_resource",
    "get_all_dataset_ids",
    "get_dataset_accrualperiodicity",
    "get_dataset_contact_email",
    "get_dataset_contact_name",
    "get_dataset_contributor",
    "get_dataset_created",
    "get_dataset_creator",
    "get_dataset_custom_field",
    "get_dataset_custom_view",
    "get_dataset_dcat_ap_ch_license",
    "get_dataset_dcat_ap_ch_rights",
    "get_dataset_description",
    "get_dataset_field_configuration",
    "get_dataset_geographic_reference",
    "get_dataset_issued",
    "get_dataset_keywords",
    "get_dataset_language",
    "get_dataset_license",
    "get_dataset_metadata",
    "get_dataset_metadata_temporal_period",
    "get_dataset_modified",
    "get_dataset_publisher",
    "get_dataset_relation",
    "get_dataset_tags",
    "get_dataset_theme",
    "get_dataset_title",
    "get_logger",
    "get_number_of_datasets",
    "get_template_metadata",
    "get_uid_by_id",
    "init_logger",
    "list_dataset_field_configurations",
    "list_dataset_resources",
    "retry",
    "set_dataset_accrualperiodicity",
    "set_dataset_contact_email",
    "set_dataset_contact_name",
    "set_dataset_contributor",
    "set_dataset_created",
    "set_dataset_creator",
    "set_dataset_custom_field",
    "set_dataset_dcat_ap_ch_license",
    "set_dataset_dcat_ap_ch_rights",
    "set_dataset_description",
    "set_dataset_geographic_reference",
    "set_dataset_issued",
    "set_dataset_keywords",
    "set_dataset_language",
    "set_dataset_license",
    "set_dataset_metadata_temporal_coverage_end_date",
    "set_dataset_metadata_temporal_coverage_start_date",
    "set_dataset_metadata_temporal_period",
    "set_dataset_modified",
    "set_dataset_public",
    "set_dataset_publisher",
    "set_dataset_relation",
    "set_dataset_tags",
    "set_dataset_theme",
    "set_dataset_title",
    "set_template_metadata",
    "strip_empty_metadata_values",
    "update_dataset_configuration",
    "update_dataset_field_configuration",
    "upsert_dataset_resource_http",
    "validate_dataset_identifier",
]
