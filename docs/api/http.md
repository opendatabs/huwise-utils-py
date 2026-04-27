# HTTP Clients

Low-level HTTP clients for making API requests.

## Overview

The library provides two HTTP clients:

- **HttpClient**: Synchronous client for simple use cases
- **AsyncHttpClient**: Asynchronous client for concurrent operations

`HttpClient` includes automatic retry with exponential backoff for transient
failures. `AsyncHttpClient` does not retry requests but raises the same
`HuwiseAutomationError` on error responses.

Both clients provide:

- Proper timeout handling
- Connection pooling (async)
- HTTP/2 support (async)

## Usage

### Synchronous Client

```python
from huwise_utils_py import HuwiseConfig, HttpClient

config = HuwiseConfig.from_env()
client = HttpClient(config)

# GET request
response = client.get("/datasets/?limit=10")
data = response.json()

# POST request
response = client.post("/datasets/da_123/publish/")

# PUT request with JSON body
response = client.put("/datasets/da_123/metadata/", json=metadata)
```

### Asynchronous Client

```python
import asyncio
from huwise_utils_py import HuwiseConfig, AsyncHttpClient

config = HuwiseConfig.from_env()
client = AsyncHttpClient(config)

async def fetch_datasets():
    async with client.session() as session:
        # Make concurrent requests
        tasks = [
            session.get(f"{config.base_url}/datasets/{dataset_id}")
            for dataset_id in ["100123", "100456", "100789"]
        ]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]

# Run async function
datasets = asyncio.run(fetch_datasets())
```

### Custom Requests

For advanced use cases, you can use the clients directly:

```python
# With query parameters
response = client.get("/datasets/", params={"limit": 100, "offset": 0})

# With custom headers (merged with auth headers)
response = client.get("/datasets/", headers={"X-Custom": "value"})
```

## Retry Logic

`HttpClient` retries only **transient** failures:

- Connection and TLS errors
- Read/write/connect timeouts
- HTTP **5xx** responses
- HTTP **429** (rate limit)

**4xx** responses (except 429) are **not** retried. On error, the client raises
`HuwiseAutomationError` (a subclass of `httpx.HTTPStatusError`) with a message
that includes a preview of the response body and, when JSON, a parsed `detail`
attribute for validation errors.

Default settings:

- 6 retry attempts
- 5 second initial delay
- Exponential backoff (delay doubles each retry)

## API Reference

::: huwise_utils_py.http.HttpClient
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - get
        - post
        - put
        - patch
        - delete

::: huwise_utils_py.http.AsyncHttpClient
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - session
        - get
        - post
        - put
