# huwise-utils-py

A Python library for the Huwise Automation API.

[![PyPI version](https://badge.fury.io/py/huwise-utils-py.svg)](https://badge.fury.io/py/huwise-utils-py)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Type-safe configuration** with Pydantic-based `HuwiseConfig`
- **Object-oriented API** with `HuwiseDataset` class and method chaining
- **Async support** for high-performance bulk operations
- **Structured logging** via `dcc-backend-common`
- **Dependency injection** support for testable code
- **Backwards compatible** function-based API available

## Installation

Using `uv` (recommended):

```bash
uv add huwise-utils-py
```

Or via `pip`:

```bash
pip install huwise-utils-py
```

## Requirements

- **Python Version:** 3.12 or higher
- **API Key:** A valid API key from Huwise

## Quick Start

### Configuration

Create a `.env` file:

```bash
HUWISE_API_KEY=your-api-key
HUWISE_DOMAIN=data.bs.ch
HUWISE_API_TYPE=automation/v1.0
```

### Using HuwiseDataset (Recommended)

```python
from huwise_utils_py import HuwiseDataset

# Create a dataset instance
dataset = HuwiseDataset(uid="da_abc123")

# Read metadata
title = dataset.get_title()
description = dataset.get_description()

# Update with method chaining
dataset.set_title("New Title", publish=False) \
       .set_description("New description") \
       .publish()
```

### Using Functions

```python
from huwise_utils_py import get_dataset_title, set_dataset_title

# Read
title = get_dataset_title(dataset_uid="da_abc123")

# Write
set_dataset_title("New Title", dataset_uid="da_abc123")
```

### Bulk Operations

```python
from huwise_utils_py import bulk_get_metadata, bulk_get_metadata_async
import asyncio

# Synchronous
metadata = bulk_get_metadata(["da_123", "da_456", "da_789"])

# Asynchronous (10-100x faster for many datasets)
metadata = asyncio.run(bulk_get_metadata_async(["da_123", "da_456", "da_789"]))
```

## API Key Setup

To use `huwise-utils-py`, create an API key with these permissions:

- Browse all datasets
- Create new datasets
- Edit all datasets
- Publish own datasets

[For OGD Basel, create your API key here](https://data.bs.ch/account/api-keys/).

**Important:** Add `**/.env` to your `.gitignore` to protect your credentials.

## Documentation

Full documentation is available at [opendatabs.github.io/huwise-utils-py](https://opendatabs.github.io/huwise-utils-py).

## API Reference

This library is a Python client for the [Huwise Automation API](https://help.opendatasoft.com/apis/ods-automation-v1/). The Automation API enables programmatic management of datasets, metadata, resources, security, and more on Huwise (ex Opendatasoft) portals.

For the complete API specification including all available endpoints, request/response schemas, and authentication details, see the [official Automation API documentation](https://help.opendatasoft.com/apis/ods-automation-v1/).

## Related Projects

- **[odsAutomationR](https://github.com/ogdtg/odsAutomationR)** - An R package for accessing the Automation API, developed by the Canton of Thurgau. If you're working in R, this package provides similar functionality.

## Further Links

- [GitHub Repository](https://github.com/opendatabs/huwise-utils-py)
- [PyPI Package](https://pypi.org/project/huwise-utils-py/)
- [Huwise Automation API Documentation](https://help.opendatasoft.com/apis/ods-automation-v1/)
- [DCC Python Coding Standards](https://dcc-bs.github.io/documentation/coding/python.html)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
