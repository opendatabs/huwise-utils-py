# HuwiseDataset

Object-oriented interface for dataset operations with method chaining support.

## Overview

`HuwiseDataset` is a dataclass that represents a Huwise dataset and provides:

- **Fluent interface**: Chain method calls for cleaner code
- **Dependency injection**: Accept custom configuration
- **Type safety**: Full type hints for all methods
- **Lazy operations**: Control when changes are published

## Usage

### Creating Instances

```python
from huwise_utils_py import HuwiseDataset

# From a UID (direct)
dataset = HuwiseDataset(uid="da_abc123")

# From a numeric ID (resolves automatically)
dataset = HuwiseDataset.from_id("12345")

# With custom configuration
from huwise_utils_py import HuwiseConfig

config = HuwiseConfig(api_key="key", domain="custom.domain.com")
dataset = HuwiseDataset(uid="da_abc123", config=config)
```

### Reading Metadata

```python
# Get specific fields
title = dataset.get_title()
description = dataset.get_description()
keywords = dataset.get_keywords()
language = dataset.get_language()
publisher = dataset.get_publisher()
theme = dataset.get_theme()
license_value = dataset.get_license()  # checks internal.license_id, falls back to default.license

# Get all metadata
metadata = dataset.get_metadata()
```

### Updating Metadata

```python
# Single update (publishes automatically)
dataset.set_title("New Title")

# Update without publishing
dataset.set_title("New Title", publish=False)

# Method chaining
dataset.set_title("Title", publish=False) \
       .set_description("Description", publish=False) \
       .set_keywords(["tag1", "tag2"], publish=False) \
       .publish()
```

### Dataset Actions

```python
# Publish changes
dataset.publish()

# Unpublish dataset
dataset.unpublish()

# Refresh dataset (re-process)
dataset.refresh()
```

## Method Chaining

All setter methods return `self`, enabling fluent interfaces:

```python
dataset = HuwiseDataset(uid="da_123")

# Chain all updates, then publish once at the end
dataset.set_title("New Title", publish=False) \
       .set_description("Updated description", publish=False) \
       .set_keywords(["python", "data", "automation"], publish=False) \
       .set_language("en", publish=False) \
       .set_publisher("Open Data Basel-Stadt", publish=False) \
       .set_theme("environment", publish=False) \
       .publish()
```

This is more efficient than calling each setter with `publish=True` because it only makes one publish API call instead of six.

## API Reference

::: huwise_utils_py.dataset.HuwiseDataset
    options:
      show_root_heading: true
      show_source: true
      members:
        - uid
        - config
        - from_id
        - get_metadata
        - get_title
        - get_description
        - get_keywords
        - get_language
        - get_publisher
        - get_theme
        - get_license
        - get_custom_view
        - set_title
        - set_description
        - set_keywords
        - set_language
        - set_publisher
        - set_theme
        - set_license
        - publish
        - unpublish
        - refresh
