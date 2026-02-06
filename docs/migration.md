# Migration from ods-utils-py

Guide for migrating from the archived `ods-utils-py` package to `huwise-utils-py`.

## Overview

The `ods-utils-py` repository has been archived and replaced by `huwise-utils-py`. This guide covers the changes needed to migrate your code.

## Breaking Changes

### Python Version

`huwise-utils-py` requires Python 3.12 or higher.

```bash
# Check your Python version
python --version
```

### Package Name

The package has been renamed:

```python
# Old
from ods_utils_py import get_dataset_title

# New
from huwise_utils_py import get_dataset_title
```

### Environment Variables

Environment variable names have changed:

| Old | New |
|-----|-----|
| `ODS_API_KEY` | `HUWISE_API_KEY` |
| `ODS_DOMAIN` | `HUWISE_DOMAIN` |
| `ODS_API_TYPE` | `HUWISE_API_TYPE` |

### Configuration Validation

Configuration is now validated at runtime using Pydantic. Invalid or missing configuration will raise `AppConfigError` instead of silently failing.

## Migration Steps

### Step 1: Update Python

Ensure you're running Python 3.12+:

```bash
python --version
# Python 3.12.x
```

### Step 2: Update Environment Variables

Rename your environment variables:

```bash
# Old
export ODS_API_KEY="key"
export ODS_DOMAIN="domain"

# New
export HUWISE_API_KEY="key"
export HUWISE_DOMAIN="domain"
```

### Step 3: Update Package

```bash
# Remove old package
pip uninstall ods-utils-py

# Install new package
pip install huwise-utils-py
```

### Step 4: Update Imports

Update your imports:

```python
# Old
from ods_utils_py import get_dataset_title, set_dataset_title

# New
from huwise_utils_py import get_dataset_title, set_dataset_title
```

## New Features

While migrating, consider taking advantage of new features:

### HuwiseDataset Class

Object-oriented interface with method chaining:

```python
from huwise_utils_py import HuwiseDataset

dataset = HuwiseDataset(uid="da_123")

# Method chaining for efficient updates
dataset.set_title("Title", publish=False) \
       .set_description("Desc", publish=False) \
       .publish()
```

### Async Bulk Operations

For better performance when working with many datasets:

```python
import asyncio
from huwise_utils_py import bulk_get_metadata_async

metadata = asyncio.run(bulk_get_metadata_async(uids))
```

### Structured Logging

Integrated structured logging:

```python
from huwise_utils_py import init_logger, get_logger

init_logger()
logger = get_logger(__name__)
logger.info("Processing dataset", uid="da_123")
```

## Backwards Compatibility

All function names from the old package are preserved:

```python
from huwise_utils_py import (
    get_dataset_title,
    get_dataset_description,
    set_dataset_title,
    set_dataset_description,
    # ... all other functions
)
```

## Getting Help

If you encounter issues during migration:

1. Check the [API Reference](api/index.md) for updated function signatures
2. Review [Examples](examples.md) for usage patterns
3. Open an issue on [GitHub](https://github.com/opendatabs/huwise-utils-py/issues)
