# Utilities

Helper functions and decorators.

## Overview

The utils module provides:

- **Validators**: Input validation functions
- **Decorators**: Reusable function decorators

## Validators

### validate_dataset_identifier

Validates and resolves dataset identifiers:

```python
from huwise_utils_py import validate_dataset_identifier

# With UID (returns as-is)
uid = validate_dataset_identifier(dataset_uid="da_abc123")
# Returns: "da_abc123"

# With numeric ID (resolves to UID via API)
uid = validate_dataset_identifier(dataset_id="12345")
# Returns: "da_resolved_uid"

# Validation errors
validate_dataset_identifier()  # ValueError: neither provided
validate_dataset_identifier(dataset_id="1", dataset_uid="da_1")  # ValueError: both provided
```

## Decorators

### retry

Retry decorator with exponential backoff:

```python
from huwise_utils_py.utils.decorators import retry
import httpx

@retry(httpx.HTTPError, tries=3, delay=1, backoff=2)
def fetch_data():
    response = httpx.get("https://api.example.com/data")
    response.raise_for_status()
    return response.json()

# First failure: waits 1s
# Second failure: waits 2s
# Third attempt: either succeeds or raises
```

Parameters:

- `exceptions_to_check`: Exception type(s) to catch
- `tries`: Number of attempts (default: 4)
- `delay`: Initial delay in seconds (default: 3)
- `backoff`: Multiplier for delay (default: 2)

## API Reference

::: huwise_utils_py.utils.validators
    options:
      show_root_heading: false
      show_source: true

::: huwise_utils_py.utils.decorators
    options:
      show_root_heading: false
      show_source: true
