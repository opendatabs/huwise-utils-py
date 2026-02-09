# Examples

Common usage patterns and code examples.

## Basic Operations

### Fetch Dataset Information

```python
from huwise_utils_py import HuwiseDataset

# Create dataset instance from its ID
dataset = HuwiseDataset.from_id("100123")

# Get basic information
print(f"Title: {dataset.get_title()}")
print(f"Description: {dataset.get_description()}")
print(f"Keywords: {dataset.get_keywords()}")
print(f"Language: {dataset.get_language()}")
print(f"Publisher: {dataset.get_publisher()}")
```

### Update Dataset Metadata

```python
from huwise_utils_py import HuwiseDataset

dataset = HuwiseDataset.from_id("100123")

# Single update
dataset.set_title("New Title")

# Multiple updates (more efficient)
dataset.set_title("New Title", publish=False) \
       .set_description("Updated description", publish=False) \
       .set_keywords(["python", "data", "open-data"], publish=False) \
       .publish()
```

### Working with Dataset IDs

```python
from huwise_utils_py import HuwiseDataset

# Create from a dataset ID
dataset = HuwiseDataset.from_id("100123")
print(f"Title: {dataset.get_title()}")
```

## Bulk Operations

### Fetch Metadata for Multiple Datasets

```python
from huwise_utils_py import bulk_get_metadata

dataset_ids = ["100123", "100456", "100789"]
metadata = bulk_get_metadata(dataset_ids=dataset_ids)

for dataset_id, meta in metadata.items():
    default = meta.get("default", {})
    title = default.get("title", {}).get("value", "No title")
    print(f"{dataset_id}: {title}")
```

### Async Bulk Operations

```python
import asyncio
from huwise_utils_py import bulk_get_metadata_async, bulk_get_dataset_ids_async

async def fetch_all_metadata():
    # Get all dataset IDs
    ids = await bulk_get_dataset_ids_async(max_datasets=100)

    # Fetch all metadata concurrently
    metadata = await bulk_get_metadata_async(dataset_ids=ids[:50])
    return metadata

# Run
all_metadata = asyncio.run(fetch_all_metadata())
print(f"Fetched metadata for {len(all_metadata)} datasets")
```

### Bulk Update

```python
from huwise_utils_py import bulk_update_metadata

updates = [
    {"dataset_id": "100123", "title": "Title 1", "description": "Desc 1"},
    {"dataset_id": "100456", "title": "Title 2", "description": "Desc 2"},
    {"dataset_id": "100789", "title": "Title 3", "description": "Desc 3"},
]

results = bulk_update_metadata(updates, publish=True)

for dataset_id, result in results.items():
    if result["status"] == "success":
        print(f"✓ {dataset_id}: Updated {result['fields_updated']}")
    else:
        print(f"✗ {dataset_id}: {result['error']}")
```

## DCAT Metadata Operations

### Reading DCAT-AP-CH Fields

```python
from huwise_utils_py import HuwiseDataset

dataset = HuwiseDataset.from_id("100123")

# DCAT-AP-CH specific fields
rights = dataset.get_dcat_ap_ch_rights()
print(f"Rights: {rights}")
# e.g. "NonCommercialAllowed-CommercialAllowed-ReferenceNotRequired"

dcat_license = dataset.get_dcat_ap_ch_license()
print(f"DCAT-AP-CH License: {dcat_license}")
# e.g. "terms_open"
```

### Writing DCAT-AP-CH Fields

```python
from huwise_utils_py import HuwiseDataset

dataset = HuwiseDataset.from_id("100123")

dataset.set_dcat_ap_ch_rights(
    "NonCommercialAllowed-CommercialAllowed-ReferenceRequired",
    publish=False,
).set_dcat_ap_ch_license(
    "terms_by",
    publish=False,
).publish()
```

### Reading and Writing DCAT Fields

```python
from huwise_utils_py import HuwiseDataset

dataset = HuwiseDataset.from_id("100123")

# Read DCAT fields
print(f"Created: {dataset.get_created()}")
print(f"Published: {dataset.get_issued()}")
print(f"Creator: {dataset.get_creator()}")
print(f"Contributor: {dataset.get_contributor()}")
print(f"Contact: {dataset.get_contact_name()} <{dataset.get_contact_email()}>")
print(f"Periodicity: {dataset.get_accrualperiodicity()}")
print(f"Relation: {dataset.get_relation()}")

# Update multiple DCAT fields efficiently
dataset.set_creator("Data Team", publish=False) \
       .set_contributor("Open Data Office", publish=False) \
       .set_contact_name("Data Office", publish=False) \
       .set_contact_email("data@example.com", publish=False) \
       .set_accrualperiodicity(
           "http://publications.europa.eu/resource/authority/frequency/DAILY",
           publish=False,
       ) \
       .publish()
```

### Managing the Modified Date

The `set_modified` method supports optional companion flags that control whether
the modified date is automatically updated when metadata or data changes:

```python
from huwise_utils_py import HuwiseDataset

dataset = HuwiseDataset.from_id("100123")

# Set a fixed modified date and disable auto-updates
dataset.set_modified(
    "2024-06-01T12:00:00Z",
    updates_on_metadata_change=False,
    updates_on_data_change=False,
)

# Enable auto-update on data changes only
dataset.set_modified(
    "2024-06-01T12:00:00Z",
    updates_on_metadata_change=False,
    updates_on_data_change=True,
)
```

### Working with Geographic References

```python
from huwise_utils_py import HuwiseDataset

dataset = HuwiseDataset.from_id("100123")

# Read current geographic references
refs = dataset.get_geographic_reference()
print(f"Geographic references: {refs}")
# e.g. ["ch_40_12"]

# Set geographic references (list of code strings)
dataset.set_geographic_reference(["ch_40_12", "ch_80_2477"])
```

### Using the Automation API Per-Field Endpoints

For lightweight reads and writes, the Huwise Automation API also supports
per-field metadata endpoints. These are useful when you only need to read or
update a single field without fetching the full metadata:

```python
import httpx

DOMAIN = "data.bs.ch"
API_KEY = "your-api-key"
DATASET_UID = "da_tbcnel"

headers = {"Authorization": f"apikey {API_KEY}"}

# Read a single field
resp = httpx.get(
    f"https://{DOMAIN}/api/automation/v1.0/datasets/{DATASET_UID}/metadata/dcat/creator/",
    headers=headers,
)
print(resp.json())  # {"value": "DCC Data Competence Center", ...}

# Update a single field
httpx.put(
    f"https://{DOMAIN}/api/automation/v1.0/datasets/{DATASET_UID}/metadata/dcat/creator/",
    headers=headers,
    json={"value": "New Creator Name"},
)
```

See the [Huwise Automation API docs](https://help.opendatasoft.com/apis/ods-automation-v1/#tag/Dataset-metadata/operation/retrieve-template-field-dataset-metadata) for more details.

## Custom Configuration

### Multiple Environments

```python
from huwise_utils_py import HuwiseConfig, HuwiseDataset

# Production config
prod_config = HuwiseConfig(
    api_key="prod-api-key",
    domain="data.production.com",
)

# Staging config
staging_config = HuwiseConfig(
    api_key="staging-api-key",
    domain="data.staging.com",
)

# Use different configs
prod_dataset = HuwiseDataset.from_id("100123", config=prod_config)
staging_dataset = HuwiseDataset.from_id("100456", config=staging_config)
```

### Testing with Mock Config

```python
from huwise_utils_py import HuwiseConfig, HuwiseDataset
from unittest.mock import patch

# Create test config
test_config = HuwiseConfig(
    api_key="test-key",
    domain="test.example.com",
)

# Mock HTTP client for testing
# Getters call the per-template endpoint, so the mock returns the template dict
with patch("huwise_utils_py.http.HttpClient") as mock:
    mock.return_value.get.return_value.json.return_value = {
        "title": {"value": "Test"}
    }

    dataset = HuwiseDataset.from_id("100123", config=test_config)
    title = dataset.get_title()
    assert title == "Test"
```

## Logging

### Basic Logging Setup

```python
from huwise_utils_py import init_logger, get_logger

# Initialize at application startup
init_logger()

# Get logger for your module
logger = get_logger(__name__)

# Log operations
logger.info("Starting data sync")
logger.debug("Processing dataset", dataset_id="100123")
logger.warning("Rate limit approaching", remaining=10)
```

### Structured Logging Example

```python
from huwise_utils_py import init_logger, get_logger, HuwiseDataset

init_logger()
logger = get_logger(__name__)

def sync_dataset(dataset_id: str) -> None:
    logger.info("Starting sync", dataset_id=dataset_id)

    try:
        dataset = HuwiseDataset.from_id(dataset_id)
        metadata = dataset.get_metadata()

        logger.info(
            "Sync completed",
            dataset_id=dataset_id,
            title=metadata.get("default", {}).get("title", {}).get("value"),
            field_count=len(metadata),
        )
    except Exception as e:
        logger.error("Sync failed", dataset_id=dataset_id, error=str(e))
        raise

sync_dataset("100123")
```

## Error Handling

### Handling API Errors

```python
import httpx
from huwise_utils_py import HuwiseDataset

try:
    dataset = HuwiseDataset.from_id("999999")
    metadata = dataset.get_metadata()
except httpx.HTTPStatusError as e:
    if e.response.status_code == 404:
        print("Dataset not found")
    elif e.response.status_code == 403:
        print("Access denied - check your API key")
    else:
        print(f"HTTP error: {e.response.status_code}")
except httpx.ConnectError:
    print("Could not connect to API")
```

### Validation Errors

```python
from huwise_utils_py import validate_dataset_identifier

try:
    # This will raise ValueError (no identifier provided)
    validate_dataset_identifier()
except ValueError as e:
    print(f"Validation error: {e}")
```

## Integration Patterns

### Django Integration

```python
# settings.py
HUWISE_CONFIG = {
    "api_key": os.environ["HUWISE_API_KEY"],
    "domain": os.environ["HUWISE_DOMAIN"],
}

# services.py
from django.conf import settings
from huwise_utils_py import HuwiseConfig, HuwiseDataset

def get_huwise_config():
    return HuwiseConfig(**settings.HUWISE_CONFIG)

def update_dataset(dataset_id: str, title: str) -> None:
    config = get_huwise_config()
    dataset = HuwiseDataset.from_id(dataset_id, config=config)
    dataset.set_title(title)
```

### FastAPI Integration

```python
from fastapi import FastAPI, Depends
from huwise_utils_py import HuwiseConfig, HuwiseDataset

app = FastAPI()

def get_config() -> HuwiseConfig:
    return HuwiseConfig.from_env()

@app.get("/datasets/{dataset_id}")
async def get_dataset(dataset_id: str, config: HuwiseConfig = Depends(get_config)):
    dataset = HuwiseDataset.from_id(dataset_id, config=config)
    return dataset.get_metadata()
```
