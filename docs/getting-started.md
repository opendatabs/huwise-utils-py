# Getting Started

This guide will help you set up and start using Huwise Utils Python.

## Prerequisites

- Python 3.12 or higher
- A Huwise API key
- Your Huwise domain URL

## Installation

=== "pip"

    ```bash
    pip install huwise-utils-py
    ```

=== "uv"

    ```bash
    uv add huwise-utils-py
    ```

## Configuration

### Environment Variables

The library requires the following environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `HUWISE_API_KEY` | Yes | Your API key for authentication |
| `HUWISE_DOMAIN` | Yes | Your Huwise domain (e.g., `data.bs.ch`) |
| `HUWISE_API_TYPE` | No | API version (defaults to `automation/v1.0`) |

### Setting Up

=== "Environment Variables"

    ```bash
    export HUWISE_API_KEY="your-api-key"
    export HUWISE_DOMAIN="data.bs.ch"
    ```

=== ".env File"

    Create a `.env` file in your project root:

    ```bash
    HUWISE_API_KEY=your-api-key
    HUWISE_DOMAIN=data.bs.ch
    HUWISE_API_TYPE=automation/v1.0
    ```

=== "Programmatic"

    ```python
    from huwise_utils_py import HuwiseConfig

    config = HuwiseConfig(
        api_key="your-api-key",
        domain="data.bs.ch",
        api_type="automation/v1.0",
    )
    ```

## Basic Usage

### Creating a Dataset Instance

```python
from huwise_utils_py import HuwiseDataset

# From a UID
dataset = HuwiseDataset(uid="da_abc123")

# From a numeric ID (resolves to UID automatically)
dataset = HuwiseDataset.from_id("12345")
```

### Reading Metadata

```python
# Get individual fields
title = dataset.get_title()
description = dataset.get_description()
keywords = dataset.get_keywords()

# Get all metadata
metadata = dataset.get_metadata()
```

### Updating Metadata

```python
# Update a single field (publishes automatically)
dataset.set_title("New Title")

# Update without publishing
dataset.set_title("New Title", publish=False)

# Chain multiple updates
dataset.set_title("Title", publish=False) \
       .set_description("Description", publish=False) \
       .set_keywords(["tag1", "tag2"], publish=False) \
       .publish()
```

### Using Custom Configuration

```python
from huwise_utils_py import HuwiseConfig, HuwiseDataset

# Create custom config
config = HuwiseConfig(
    api_key="different-key",
    domain="other.domain.com",
)

# Use with dataset
dataset = HuwiseDataset(uid="da_abc123", config=config)
```

## Bulk Operations

For working with multiple datasets:

```python
from huwise_utils_py import bulk_get_metadata, bulk_get_metadata_async

# Synchronous
metadata = bulk_get_metadata(["da_123", "da_456", "da_789"])

# Asynchronous (much faster for many datasets)
import asyncio

async def fetch_all():
    return await bulk_get_metadata_async(["da_123", "da_456", "da_789"])

metadata = asyncio.run(fetch_all())
```

## Logging

Initialize structured logging for your application:

```python
from huwise_utils_py import init_logger, get_logger

# Initialize once at app startup
init_logger()

# Get a logger for your module
logger = get_logger(__name__)
logger.info("Starting data sync", dataset_count=10)
```

## Next Steps

- Read the [API Reference](api/index.md) for detailed documentation
- Check out [Examples](examples.md) for common use cases
- See the [Migration Guide](migration.md) if coming from `ods-utils-py`
