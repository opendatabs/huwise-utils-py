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

# From a dataset ID
dataset = HuwiseDataset.from_id("100123")

# With custom configuration
from huwise_utils_py import HuwiseConfig

config = HuwiseConfig(api_key="key", domain="custom.domain.com")
dataset = HuwiseDataset.from_id("100123", config=config)
```

### Reading Metadata

```python
# Basic fields
title = dataset.get_title()
description = dataset.get_description()
keywords = dataset.get_keywords()
language = dataset.get_language()
publisher = dataset.get_publisher()
theme = dataset.get_theme()
license_value = dataset.get_license()  # checks internal.license_id, falls back to default.license

# DCAT-AP-CH fields
rights = dataset.get_dcat_ap_ch_rights()
dcat_license = dataset.get_dcat_ap_ch_license()

# DCAT fields
created = dataset.get_created()
issued = dataset.get_issued()          # publication date
creator = dataset.get_creator()
contributor = dataset.get_contributor()
contact_name = dataset.get_contact_name()
contact_email = dataset.get_contact_email()
periodicity = dataset.get_accrualperiodicity()
relation = dataset.get_relation()

# Default template fields
modified = dataset.get_modified()
geo_refs = dataset.get_geographic_reference()

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

# DCAT-AP-CH fields
dataset.set_dcat_ap_ch_rights(
    "NonCommercialAllowed-CommercialAllowed-ReferenceRequired",
    publish=False,
)
dataset.set_dcat_ap_ch_license("terms_by", publish=False)

# DCAT fields
dataset.set_creator("Data Team", publish=False)
dataset.set_contributor("Open Data Basel-Stadt", publish=False)
dataset.set_contact_name("Data Office", publish=False)
dataset.set_contact_email("data@example.com", publish=False)
dataset.set_issued("2024-06-01", publish=False)
dataset.set_created("2024-06-01T10:00:00Z", publish=False)
dataset.set_accrualperiodicity(
    "http://publications.europa.eu/resource/authority/frequency/DAILY",
    publish=False,
)
dataset.set_relation("https://example.com/related", publish=False)

# Geographic reference
dataset.set_geographic_reference(["ch_40_12"], publish=False)

# Modified date with companion flags
dataset.set_modified(
    "2024-06-01T12:00:00Z",
    updates_on_metadata_change=True,
    updates_on_data_change=False,
    publish=False,
)

dataset.publish()
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
dataset = HuwiseDataset.from_id("100123")

# Chain all updates, then publish once at the end
dataset.set_title("New Title", publish=False) \
       .set_description("Updated description", publish=False) \
       .set_keywords(["python", "data", "automation"], publish=False) \
       .set_language("en", publish=False) \
       .set_publisher("Open Data Basel-Stadt", publish=False) \
       .set_theme("environment", publish=False) \
       .set_dcat_ap_ch_rights("NonCommercialAllowed-CommercialAllowed-ReferenceRequired", publish=False) \
       .set_dcat_ap_ch_license("terms_by", publish=False) \
       .set_creator("Data Team", publish=False) \
       .set_contact_email("data@example.com", publish=False) \
       .set_geographic_reference(["ch_40_12"], publish=False) \
       .publish()
```

This is more efficient than calling each setter with `publish=True` because it only makes one publish API call instead of six.

## API Reference

::: huwise_utils_py.dataset.HuwiseDataset
    options:
      show_root_heading: true
      show_source: true
      members:
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
        - get_dcat_ap_ch_rights
        - get_dcat_ap_ch_license
        - get_created
        - get_issued
        - get_creator
        - get_contributor
        - get_contact_name
        - get_contact_email
        - get_accrualperiodicity
        - get_relation
        - get_modified
        - get_geographic_reference
        - set_title
        - set_description
        - set_keywords
        - set_language
        - set_publisher
        - set_theme
        - set_license
        - set_dcat_ap_ch_rights
        - set_dcat_ap_ch_license
        - set_created
        - set_issued
        - set_creator
        - set_contributor
        - set_contact_name
        - set_contact_email
        - set_accrualperiodicity
        - set_relation
        - set_geographic_reference
        - set_modified
        - publish
        - unpublish
        - refresh
