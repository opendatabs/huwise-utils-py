# Function-based API

Standalone functions for dataset operations.

## Overview

The function-based API provides standalone functions for common operations. These functions internally use `HuwiseDataset` but offer a simpler interface for straightforward tasks.

!!! tip "Recommendation"
    For complex workflows or when working with multiple fields, consider using `HuwiseDataset` directly for better type safety and method chaining.

## Usage

### Getters

```python
from huwise_utils_py import (
    get_dataset_title,
    get_dataset_description,
    get_dataset_keywords,
    get_dataset_language,
    get_dataset_publisher,
    get_dataset_theme,
    get_dataset_license,
    get_dataset_metadata,
    get_number_of_datasets,
    get_all_dataset_ids,
    # New DCAT-AP-CH getters
    get_dataset_dcat_ap_ch_rights,
    get_dataset_dcat_ap_ch_license,
    # New DCAT getters
    get_dataset_created,
    get_dataset_issued,
    get_dataset_creator,
    get_dataset_contributor,
    get_dataset_contact_name,
    get_dataset_contact_email,
    get_dataset_accrualperiodicity,
    get_dataset_relation,
    # New default template getters
    get_dataset_modified,
    get_dataset_geographic_reference,
)

# Get metadata by dataset ID
title = get_dataset_title(dataset_id="100123")
description = get_dataset_description(dataset_id="100123")

# Get all metadata
metadata = get_dataset_metadata(dataset_id="100123")

# Get dataset counts and IDs
count = get_number_of_datasets()
ids = get_all_dataset_ids()

# DCAT-AP-CH fields
rights = get_dataset_dcat_ap_ch_rights(dataset_id="100123")
dcat_license = get_dataset_dcat_ap_ch_license(dataset_id="100123")

# DCAT fields
creator = get_dataset_creator(dataset_id="100123")
contact = get_dataset_contact_name(dataset_id="100123")
issued = get_dataset_issued(dataset_id="100123")

# Default template fields
modified = get_dataset_modified(dataset_id="100123")
geo_refs = get_dataset_geographic_reference(dataset_id="100123")
```

### Setters

```python
from huwise_utils_py import (
    set_dataset_title,
    set_dataset_description,
    set_dataset_keywords,
    set_dataset_language,
    set_dataset_publisher,
    set_dataset_theme,
    set_dataset_license,
    set_dataset_public,
    # New DCAT-AP-CH setters
    set_dataset_dcat_ap_ch_rights,
    set_dataset_dcat_ap_ch_license,
    # New DCAT setters
    set_dataset_created,
    set_dataset_issued,
    set_dataset_creator,
    set_dataset_contributor,
    set_dataset_contact_name,
    set_dataset_contact_email,
    set_dataset_accrualperiodicity,
    set_dataset_relation,
    # New default template setters
    set_dataset_modified,
    set_dataset_geographic_reference,
)

# Set metadata (publishes by default)
set_dataset_title("New Title", dataset_id="100123")

# Set without publishing
set_dataset_title("New Title", dataset_id="100123", publish=False)

# Publish/unpublish
set_dataset_public(dataset_id="100123", should_be_public=True)
set_dataset_public(dataset_id="100123", should_be_public=False)

# DCAT-AP-CH fields
set_dataset_dcat_ap_ch_rights(
    "NonCommercialAllowed-CommercialAllowed-ReferenceRequired",
    dataset_id="100123",
)
set_dataset_dcat_ap_ch_license("terms_by", dataset_id="100123")

# Modified date with companion flags
set_dataset_modified(
    "2024-06-01T12:00:00Z",
    dataset_id="100123",
    updates_on_metadata_change=True,
    updates_on_data_change=False,
)
```

## Comparison with HuwiseDataset

```python
# Function-based approach
from huwise_utils_py import get_dataset_title, set_dataset_title

title = get_dataset_title(dataset_id="100123")
set_dataset_title("New Title", dataset_id="100123")
set_dataset_description("Desc", dataset_id="100123")

# HuwiseDataset approach (recommended for multiple operations)
from huwise_utils_py import HuwiseDataset

dataset = HuwiseDataset.from_id("100123")
title = dataset.get_title()
dataset.set_title("New Title", publish=False) \
       .set_description("Desc") \
       .publish()
```

## Available Functions

### Getters

| Function | Description |
|----------|-------------|
| `get_all_dataset_ids()` | Get all dataset IDs |
| `get_number_of_datasets()` | Get total dataset count |
| `get_dataset_metadata()` | Get full metadata |
| `get_dataset_title()` | Get dataset title |
| `get_dataset_description()` | Get dataset description |
| `get_dataset_keywords()` | Get dataset keywords |
| `get_dataset_language()` | Get dataset language |
| `get_dataset_publisher()` | Get dataset publisher |
| `get_dataset_theme()` | Get dataset theme |
| `get_dataset_license()` | Get dataset license |
| `get_dataset_custom_view()` | Get custom view config |
| `get_dataset_dcat_ap_ch_rights()` | Get DCAT-AP-CH rights statement |
| `get_dataset_dcat_ap_ch_license()` | Get DCAT-AP-CH license code |
| `get_dataset_created()` | Get creation date (`dcat.created`) |
| `get_dataset_issued()` | Get publication date (`dcat.issued`) |
| `get_dataset_creator()` | Get dataset creator |
| `get_dataset_contributor()` | Get dataset contributor |
| `get_dataset_contact_name()` | Get contact name |
| `get_dataset_contact_email()` | Get contact email |
| `get_dataset_accrualperiodicity()` | Get accrual periodicity (EU frequency URI) |
| `get_dataset_relation()` | Get relation URL |
| `get_dataset_modified()` | Get last-modified date (`default.modified`) |
| `get_dataset_geographic_reference()` | Get geographic reference codes |
| `get_dataset_metadata_temporal_period()` | Get temporal coverage |
| `get_template_metadata()` | Get template-specific metadata |

### Setters

| Function | Description |
|----------|-------------|
| `set_dataset_public()` | Publish/unpublish dataset |
| `set_dataset_title()` | Set dataset title |
| `set_dataset_description()` | Set dataset description |
| `set_dataset_keywords()` | Set dataset keywords |
| `set_dataset_language()` | Set dataset language |
| `set_dataset_publisher()` | Set dataset publisher |
| `set_dataset_theme()` | Set dataset theme |
| `set_dataset_license()` | Set dataset license (supports optional `license_name` for the human-readable string) |
| `set_dataset_dcat_ap_ch_rights()` | Set DCAT-AP-CH rights statement |
| `set_dataset_dcat_ap_ch_license()` | Set DCAT-AP-CH license code |
| `set_dataset_created()` | Set creation date (`dcat.created`) |
| `set_dataset_issued()` | Set publication date (`dcat.issued`) |
| `set_dataset_creator()` | Set dataset creator |
| `set_dataset_contributor()` | Set dataset contributor |
| `set_dataset_contact_name()` | Set contact name |
| `set_dataset_contact_email()` | Set contact email |
| `set_dataset_accrualperiodicity()` | Set accrual periodicity (EU frequency URI) |
| `set_dataset_relation()` | Set relation URL |
| `set_dataset_geographic_reference()` | Set geographic reference codes |
| `set_dataset_modified()` | Set last-modified date with optional companion flags |
| `set_dataset_metadata_temporal_period()` | Set both dates |
| `set_dataset_metadata_temporal_coverage_start_date()` | Set start date |
| `set_dataset_metadata_temporal_coverage_end_date()` | Set end date |
| `set_template_metadata()` | Set template-specific field |
