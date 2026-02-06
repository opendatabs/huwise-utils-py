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
metadata = bulk_get_metadata(["da_123", "da_456", "da_789"])

# Update multiple datasets
updates = [
    {"dataset_uid": "da_123", "title": "New Title 1"},
    {"dataset_uid": "da_456", "title": "New Title 2"},
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
    metadata = await bulk_get_metadata_async(["da_123", "da_456", "da_789"])

    # Update concurrently
    updates = [
        {"dataset_uid": "da_123", "title": "New Title 1"},
        {"dataset_uid": "da_456", "title": "New Title 2"},
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

uids = ["da_123", "da_456", "da_789"]
metadata = bulk_get_metadata(uids)

for uid, meta in metadata.items():
    title = meta.get("default", {}).get("title", {}).get("value", "No title")
    print(f"{uid}: {title}")
```

### Bulk Update with Error Handling

```python
from huwise_utils_py import bulk_update_metadata

updates = [
    {"dataset_uid": "da_123", "title": "Title 1", "description": "Desc 1"},
    {"dataset_uid": "da_456", "title": "Title 2", "description": "Desc 2"},
    {"dataset_uid": "da_invalid", "title": "Will fail"},
]

results = bulk_update_metadata(updates, publish=True)

for uid, result in results.items():
    if result["status"] == "success":
        print(f"{uid}: Updated {result['fields_updated']}")
    else:
        print(f"{uid}: Failed - {result['error']}")
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
        bulk_get_metadata_async(["da_1", "da_2"], config=config_a),
        bulk_get_metadata_async(["da_3", "da_4"], config=config_b),
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
