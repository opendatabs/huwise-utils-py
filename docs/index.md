# Huwise Utils Python

A modern, type-safe Python library for the Huwise Automation API.

## Features

- **Type-safe configuration** with Pydantic-based `HuwiseConfig`
- **Object-oriented API** with `HuwiseDataset` class and method chaining
- **Async support** for high-performance bulk operations
- **Structured logging** via `dcc-backend-common`
- **Dependency injection** support for testable code
- **Backwards compatible** function-based API

## Installation

=== "pip"

    ```bash
    pip install huwise-utils-py
    ```

=== "uv"

    ```bash
    uv add huwise-utils-py
    ```

## Quick Start

### Using the HuwiseDataset Class (Recommended)

```python
from huwise_utils_py import HuwiseDataset

# Create a dataset instance
dataset = HuwiseDataset(uid="da_abc123")

# Read metadata
title = dataset.get_title()
description = dataset.get_description()

# Update metadata with method chaining
dataset.set_title("New Title", publish=False) \
       .set_description("New description") \
       .publish()
```

### Using the Function-based API

```python
from huwise_utils_py import get_dataset_title, set_dataset_title

# Read metadata
title = get_dataset_title(dataset_uid="da_abc123")

# Update metadata
set_dataset_title("New Title", dataset_uid="da_abc123")
```

## Configuration

Set up your environment variables:

```bash
export HUWISE_API_KEY="your-api-key"
export HUWISE_DOMAIN="data.bs.ch"
export HUWISE_API_TYPE="automation/v1.0"  # Optional
```

Or use a `.env` file:

```bash
HUWISE_API_KEY=your-api-key
HUWISE_DOMAIN=data.bs.ch
HUWISE_API_TYPE=automation/v1.0
```

## Note on Previous Package

This package replaces the archived `ods-utils-py` repository. If you're migrating from the old package, see the [Migration Guide](migration.md) for details on the changes.

## Links

- [GitHub Repository](https://github.com/opendatabs/huwise-utils-py)
- [PyPI Package](https://pypi.org/project/huwise-utils-py/)
- [Huwise API Documentation](https://help.opendatasoft.com/apis/ods-automation-v1/)
- [DCC Python Coding Standards](https://dcc-bs.github.io/documentation/coding/python.html)
