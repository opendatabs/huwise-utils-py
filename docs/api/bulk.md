# Bulk Operations

Functions for operating on multiple datasets efficiently.

## Overview

Bulk operations provide significant performance improvements when working with many datasets:

| Operation | Sequential | Bulk (Async) | Speedup |
|-----------|------------|--------------|---------|
| 10 datasets | ~2s | ~0.2s | 10x |
| 100 datasets | ~20s | ~0.5s | 40x |
| 1000 datasets | ~200s | ~2s | 100x |

## Available Functions

### Synchronous

```python
from huwise_utils_py import bulk_get_metadata, bulk_update_metadata, bulk_get_dataset_ids

# Get metadata for multiple datasets
metadata = bulk_get_metadata(dataset_ids=["100123", "100456", "100789"])

# Update multiple datasets
updates = [
    {"dataset_id": "100123", "title": "New Title 1"},
    {"dataset_id": "100456", "title": "New Title 2"},
]
results = bulk_update_metadata(updates)

# Get all dataset IDs
ids = bulk_get_dataset_ids()
```

### Asynchronous

```python
import asyncio
from huwise_utils_py import (
    bulk_get_metadata_async,
    bulk_update_metadata_async,
    bulk_get_dataset_ids_async,
)

async def main():
    # Fetch metadata concurrently
    metadata = await bulk_get_metadata_async(dataset_ids=["100123", "100456", "100789"])

    # Update concurrently
    updates = [
        {"dataset_id": "100123", "title": "New Title 1"},
        {"dataset_id": "100456", "title": "New Title 2"},
    ]
    results = await bulk_update_metadata_async(updates)

    # Get all IDs
    ids = await bulk_get_dataset_ids_async()

asyncio.run(main())
```

## Usage Examples

### Bulk Metadata Fetch

```python
from huwise_utils_py import bulk_get_metadata

dataset_ids = ["100123", "100456", "100789"]
metadata = bulk_get_metadata(dataset_ids=dataset_ids)

for dataset_id, meta in metadata.items():
    title = meta.get("default", {}).get("title", {}).get("value", "No title")
    print(f"{dataset_id}: {title}")
```

### Bulk Update with Error Handling

```python
from huwise_utils_py import bulk_update_metadata

updates = [
    {"dataset_id": "100123", "title": "Title 1", "description": "Desc 1"},
    {"dataset_id": "100456", "title": "Title 2", "description": "Desc 2"},
    {"dataset_id": "100789", "title": "Will fail"},
]

results = bulk_update_metadata(updates, publish=True)

for dataset_id, result in results.items():
    if result["status"] == "success":
        print(f"{dataset_id}: Updated {result['fields_updated']}")
    else:
        print(f"{dataset_id}: Failed - {result['error']}")
```

### Get All Dataset IDs with Filtering

```python
from huwise_utils_py import bulk_get_dataset_ids

# Get all public datasets (exclude restricted)
public_ids = bulk_get_dataset_ids(include_restricted=False)

# Get first 100 datasets
limited_ids = bulk_get_dataset_ids(max_datasets=100)
```

### Async with Custom Configuration

```python
import asyncio
from huwise_utils_py import HuwiseConfig, bulk_get_metadata_async

async def fetch_from_multiple_domains():
    # Config for domain A
    config_a = HuwiseConfig(api_key="key-a", domain="domain-a.com")

    # Config for domain B
    config_b = HuwiseConfig(api_key="key-b", domain="domain-b.com")

    # Fetch concurrently from both domains
    metadata_a, metadata_b = await asyncio.gather(
        bulk_get_metadata_async(dataset_ids=["100123", "100456"], config=config_a),
        bulk_get_metadata_async(dataset_ids=["100789"], config=config_b),
    )

    return {**metadata_a, **metadata_b}

asyncio.run(fetch_from_multiple_domains())
```

## API Reference

::: huwise_utils_py.bulk
    options:
      show_root_heading: false
      show_source: true
      members:
        - bulk_get_metadata
        - bulk_get_metadata_async
        - bulk_update_metadata
        - bulk_update_metadata_async
        - bulk_get_dataset_ids
        - bulk_get_dataset_ids_async
