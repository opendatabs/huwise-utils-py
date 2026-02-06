# API Reference

This section documents the public API of huwise-utils-py.

!!! info "Huwise Automation API"
    This library wraps the [Huwise Automation API](https://help.opendatasoft.com/apis/ods-automation-v1/). 
    For detailed information about available endpoints, request/response schemas, and the underlying 
    API capabilities, refer to the [official API documentation](https://help.opendatasoft.com/apis/ods-automation-v1/).

## Core Components

The library provides these main components:

### Configuration

- [`HuwiseConfig`](config.md) - Type-safe configuration management

### Dataset Operations

- [`HuwiseDataset`](dataset.md) - Object-oriented dataset interface

### HTTP Clients

- [`HttpClient`](http.md#huwise_utils_py.http.HttpClient) - Synchronous HTTP client
- [`AsyncHttpClient`](http.md#huwise_utils_py.http.AsyncHttpClient) - Asynchronous HTTP client

### Bulk Operations

- [`bulk_get_metadata`](bulk.md) - Fetch metadata for multiple datasets
- [`bulk_update_metadata`](bulk.md) - Update multiple datasets
- [`bulk_get_dataset_ids`](bulk.md) - List all dataset IDs

### Utilities

- [`validate_dataset_identifier`](utils.md) - Validate and resolve dataset IDs
- [`retry`](utils.md) - Retry decorator with exponential backoff

### Function-based API

- [Functions](legacy.md) - Standalone functions for dataset operations

## Import Examples

```python
# Core components
from huwise_utils_py import HuwiseConfig, HuwiseDataset

# HTTP clients
from huwise_utils_py import HttpClient, AsyncHttpClient

# Bulk operations
from huwise_utils_py import (
    bulk_get_metadata,
    bulk_get_metadata_async,
    bulk_update_metadata,
    bulk_update_metadata_async,
)

# Utilities
from huwise_utils_py import validate_dataset_identifier, retry

# Logging
from huwise_utils_py import init_logger, get_logger

# Function-based API
from huwise_utils_py import get_dataset_title, set_dataset_title
```

## Architecture

```
huwise_utils_py/
├── config.py       # HuwiseConfig
├── dataset.py      # HuwiseDataset
├── http.py         # HttpClient, AsyncHttpClient
├── bulk.py         # Bulk operations
├── logger.py       # Logging utilities
├── utils/          # Helpers
│   ├── validators.py
│   └── decorators.py
└── _legacy/        # Backwards-compatible API
    ├── getters.py
    └── setters.py
```
