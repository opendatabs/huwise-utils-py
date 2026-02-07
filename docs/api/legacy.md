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
)

# Get metadata by dataset ID
title = get_dataset_title(dataset_id="100123")
description = get_dataset_description(dataset_id="100123")

# Get all metadata
metadata = get_dataset_metadata(dataset_id="100123")

# Get dataset counts and IDs
count = get_number_of_datasets()
ids = get_all_dataset_ids()
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
)

# Set metadata (publishes by default)
set_dataset_title("New Title", dataset_id="100123")

# Set without publishing
set_dataset_title("New Title", dataset_id="100123", publish=False)

# Publish/unpublish
set_dataset_public(dataset_id="100123", should_be_public=True)
set_dataset_public(dataset_id="100123", should_be_public=False)
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
| `set_dataset_metadata_temporal_period()` | Set both dates |
| `set_dataset_metadata_temporal_coverage_start_date()` | Set start date |
| `set_dataset_metadata_temporal_coverage_end_date()` | Set end date |
| `set_template_metadata()` | Set template-specific field |
