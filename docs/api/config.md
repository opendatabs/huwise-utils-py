# HuwiseConfig

Type-safe configuration management for Huwise API access.

## Overview

`HuwiseConfig` is a Pydantic-based configuration class that provides:

- **Validation**: Ensures required fields are present
- **Type safety**: Full type hints and runtime validation
- **Dependency injection**: Pass configuration to components
- **Secure logging**: API keys are masked in string representations

## Usage

### From Environment Variables

```python
from huwise_utils_py import HuwiseConfig

# Loads from HUWISE_API_KEY, HUWISE_DOMAIN, HUWISE_API_TYPE
config = HuwiseConfig.from_env()
```

### Programmatic

```python
config = HuwiseConfig(
    api_key="your-api-key",
    domain="data.bs.ch",
    api_type="automation/v1.0",  # Optional, defaults to this
)
```

### Properties

```python
# Get the base URL for API requests
print(config.base_url)
# Output: https://data.bs.ch/api/automation/v1.0

# Get authorization headers
print(config.headers)
# Output: {"Authorization": "apikey your-api-key"}
```

### Dependency Injection

```python
from huwise_utils_py import HuwiseConfig, HuwiseDataset

# Create a custom config for testing
test_config = HuwiseConfig(
    api_key="test-key",
    domain="test.example.com",
)

# Inject into components
dataset = HuwiseDataset.from_id("100123", config=test_config)
```

## API Reference

::: huwise_utils_py.config.HuwiseConfig
    options:
      show_root_heading: true
      show_source: true
      members:
        - api_key
        - domain
        - api_type
        - from_env
        - base_url
        - headers
