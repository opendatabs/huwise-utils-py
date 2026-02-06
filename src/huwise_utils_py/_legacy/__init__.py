"""Function-based API for dataset operations.

This module provides standalone functions that wrap the HuwiseDataset
class internally for simpler use cases.

Note:
    For complex workflows or multiple field updates, consider using
    the HuwiseDataset class directly for method chaining.
"""

from huwise_utils_py._legacy.getters import (
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
)
from huwise_utils_py._legacy.setters import (
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

__all__ = [
    # Getters
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
    "get_number_of_datasets",
    "get_template_metadata",
    "get_uid_by_id",
    # Setters
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
]
